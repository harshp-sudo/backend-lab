#!/usr/bin/env python3
"""Check current topic publishing: whole-catalog static checks, scoped browser/PDF checks."""
import argparse
import asyncio
import functools
import importlib.util
import importlib.metadata
import json
import subprocess
import sys
import threading
import time
import traceback
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import validate_content as vc

RUNTIME = ('index.html', 'app.js', 'styles.css', 'tailwind.config.cjs', '.nojekyll')


def runtime_files(root):
    return sorted(set(RUNTIME) | {str(p.relative_to(root)) for p in (root/'assets').rglob('*') if p.is_file()})


def changed_paths(root):
    """Include staged, unstaged and untracked content, even before the first commit."""
    paths = set()
    for command in [
        ['git', 'diff', '--name-only', '-z'],
        ['git', 'diff', '--cached', '--name-only', '-z'],
        ['git', 'ls-files', '--others', '--exclude-standard', '-z'],
    ]:
        result = subprocess.run(command, cwd=root, capture_output=True)
        if result.returncode:
            raise vc.ValidationError('Change discovery needs a Git checkout; use --paths or --all instead')
        paths.update(p for p in result.stdout.decode('utf-8').split('\0') if p)
    return sorted(paths)


def select_nodes(index, paths, *, all_nodes=False, research_records=None):
    """A topic selects itself and ancestor hubs; shared runtime selects the catalog."""
    runtime = any(p in RUNTIME or p.startswith('assets/') for p in paths)
    standards = any(p == '.specify/memory/constitution.md' for p in paths)
    selected = set(index) if all_nodes or runtime or standards else set()
    explicit = set(paths)
    for route, item in index.items():
        record_suffix = '/'+item['node']['id']+'.json'
        if (item['relative_path'] in explicit or (research_records or {}).get(item['node']['id']) in explicit
                or any(p.endswith(record_suffix) for p in paths)):
            selected.add(route)
            selected.update('/'+'/'.join(n['slug'] for n in item['ancestors'][:i]) for i in range(1,len(item['ancestors'])))
    return [i for route,i in index.items() if route in selected], runtime


def apply_catalog_delta(index, selected, baseline, root):
    """Manifest-only moves, titles, new entries and hub child changes also need rendering."""
    before = vc.index_manifest(baseline,root,baseline)
    ids = {item['node']['id']:item for item in before.values()}
    routes = {item['route'] for item in selected}
    for route,item in index.items():
        old = ids.get(item['node']['id'])
        if old is None or signature(old) != signature(item):
            routes.add(route)
            routes.update('/'+'/'.join(n['slug'] for n in item['ancestors'][:i]) for i in range(1,len(item['ancestors'])))
    return [i for route,i in index.items() if route in routes]


def signature(item):
    return {'node':item['node'], 'route':item['route'], 'ancestors':[
        {k:n[k] for k in ('id','slug','title')} for n in item['ancestors'][:-1]]}


@contextmanager
def serve(root):
    """Serve the same checkout at / and /backend-lab/, owning ports and cleanup."""
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, *_): pass
        def translate_path(self, path):
            if unquote(path.split('?',1)[0]).startswith('/backend-lab/'):
                path = path[len('/backend-lab'):]
            return super().translate_path(path)
    server = ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(root)))
    thread = threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base = f'http://127.0.0.1:{server.server_port}/'
    try:
        for url in (base+'manifest.json',base+'backend-lab/manifest.json'):
            with urlopen(url,timeout=5) as response:
                if response.status != 200: raise RuntimeError('Local server did not become ready')
        yield base,base+'backend-lab/'
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)


def atomic_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');tmp.replace(path)


def fingerprint(root, item, browser):
    # No global manifest hash: an unrelated new topic does not invalidate this lesson.
    files = runtime_files(root) + ['tools/validate_content.py','tools/check_topics.py',
        'tests/dashboard/check_dashboard.py','tests/dashboard/requirements.txt','tests/content/publishing.json',
        '.specify/memory/constitution.md']
    config = vc.load_json(root/'tests/content/publishing.json')
    record = config.get('researchRecords',{}).get(item['node']['id'],config['researchDirectory']+'/'+item['node']['id']+'.json')
    files += [item['relative_path']]
    if item['node']['kind']=='topic': files.append(record)
    return vc.sha256(json.dumps({'contract':config['recallProfile'],'researchPresentation':config['researchPresentation'],'node':signature(item),'browser':browser,
        'files':{p:vc.sha256((root/p).read_bytes()) for p in files}},sort_keys=True).encode())


def reusable(row, key):
    if not isinstance(row,dict) or row.get('status')!='pass' or row.get('fingerprint')!=key: return False
    outputs = row.get('outputs',[])
    if (not isinstance(outputs,list) or len(outputs)!=2 or any(not isinstance(o,dict) for o in outputs)
            or {o.get('theme') for o in outputs} != {'light','dark'}): return False
    try:
        return all(Path(o['pdf']).is_file() and vc.sha256(Path(o['pdf']).read_bytes())==o['sha256'] for o in outputs)
    except (OSError,KeyError,TypeError): return False


def load_browser_checks():
    path = Path(__file__).resolve().parents[1]/'tests/dashboard/check_dashboard.py'
    spec = importlib.util.spec_from_file_location('dashboard_checks',path)
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


async def render_node(browser, checks, item, bases, inventory):
    """Exercise every authored card once; layout/theme checks avoid repeating state mutations."""
    node = item['node'];own=inventory['nodes'][node['id']];cases=[]
    for base,width,theme in [(bases[0],1440,'light'),(bases[1],360,'light'),(bases[1],360,'dark')]:
        context = await browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce',color_scheme=theme)
        try:
            await context.add_init_script('document.addEventListener("DOMContentLoaded",()=>{document.documentElement.style.scrollBehavior="auto";},{once:true})')
            page=await context.new_page();errors=[];requests=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
            page.on('request',lambda request:requests.append(request.url))
            await page.goto(base+'#'+item['route']);await checks.ready(page,True)
            await page.reload();await checks.ready(page,True)
            assert await page.locator('article').get_attribute('data-node-id')==node['id']
            assert await page.locator('article').get_attribute('data-enhancement')=='complete'
            assert await page.locator('html').get_attribute('data-theme')==theme
            assert await page.locator('pre.mermaid svg').count()==own['diagrams']
            assert not await page.locator('svg.flowchart foreignObject').count()
            assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            cards=page.locator('details.kb-question')
            assert await cards.count()==len(own['foundationalKeys'])+len(own['interviewKeys'])
            if width==1440:
                for card in await cards.all():
                    assert not await card.evaluate('(e)=>e.open')
                    before=await cards.evaluate_all('(els)=>els.map(e=>e.open)')
                    await card.locator('summary').focus();await page.keyboard.press('Enter')
                    assert await card.evaluate('(e)=>e.open')
                    after=await cards.evaluate_all('(els)=>els.map(e=>e.open)')
                    assert sum(a!=b for a,b in zip(before,after))==1
                    assert await card.locator('[data-host-confidence]').count()==1
                    await card.get_by_role('button',name='Good',exact=True).click()
                    await card.locator('summary').focus();await page.keyboard.press('Space')
                    assert not await card.evaluate('(e)=>e.open')
                if node['kind']=='topic':
                    assert await page.locator('#global-percent').inner_text()=='0%'
                    await page.locator('#topic-status').select_option('mastered')
                    await page.reload();await checks.ready(page,True)
                    assert await page.locator('#topic-status').input_value()=='mastered'
                    assert await page.locator('#global-percent').inner_text()==str(int(100/inventory['topicCount']+.5))+'%'
                    assert await page.locator('[data-confidence=good][aria-pressed=true]').count()==await cards.count()
            else:
                await page.locator('article details').evaluate_all('(els)=>els.forEach((e,i)=>e.open=i%2===0)')
                states=await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')
                await page.locator('#theme-toggle').click();await checks.ready(page,True)
                assert await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')==states
                assert await page.locator('pre.mermaid svg').count()==own['diagrams']
            if node['kind']=='hub':
                for child in node['children']:
                    await page.goto(base+'#'+item['route']);await checks.ready(page,True)
                    await page.locator('[data-child-links] > li > a').filter(has_text=child['title']).click()
                    await checks.ready(page,True)
                    assert await page.locator('article').get_attribute('data-node-id')==child['id']
            assert all(url.startswith(base+'topics/') for url in requests if '/topics/' in url),requests
            assert not errors,errors
            cases.append({'base':'project' if base==bases[1] else 'root','width':width,'theme':theme,'status':'pass'})
        finally:
            await context.close()
    return cases


async def bounded_checks(items, worker, limit):
    """Bound page memory; cancel unfinished siblings when one required check fails."""
    gate=asyncio.Semaphore(limit)
    async def one(item):
        async with gate:return await worker(item)
    tasks=[asyncio.create_task(one(item)) for item in items]
    try:return await asyncio.gather(*tasks)
    except BaseException:
        for task in tasks:task.cancel()
        await asyncio.gather(*tasks,return_exceptions=True)
        raise


async def browser_run(args, root, selected, report, previous):
    checks=load_browser_checks()
    from playwright.async_api import async_playwright
    version=importlib.metadata.version('playwright')
    report['playwright']=version
    report['jobs']=args.jobs
    if 'playwright=='+version not in (root/'tests/dashboard/requirements.txt').read_text().splitlines():
        raise vc.ValidationError('Install the pinned Playwright version from tests/dashboard/requirements.txt')
    inventory=checks.current_inventory(root)
    with serve(root) as bases:
        async with async_playwright() as playwright:
            browser=await playwright.chromium.launch(headless=True,args=['--no-sandbox'])
            try:
                report['browser']=browser.version
                async def verify_item(item):
                    key=fingerprint(root,item,{'chromium':browser.version,'playwright':version})
                    old=next((r for r in previous.get('nodes',[]) if r.get('nodeId')==item['node']['id']),{})
                    if not args.no_cache and reusable(old,key):
                        row={**old,'reused':True};report['nodes'].append(row)
                        print('Reused:',item['relative_path'],flush=True)
                    else:
                        started=time.monotonic()
                        row={'nodeId':item['node']['id'],'path':item['relative_path'],'fingerprint':key,'status':'pending','phase':'browser','reused':False}
                        report['nodes'].append(row)
                        atomic_json(args.report,report)
                        row['browserCases']=await render_node(browser,checks,item,bases,inventory)
                        row['phase']='print'
                        atomic_json(args.report,report)
                        pdfs=await checks.print_articles(browser,SimpleNamespace(base_url=bases[0],pdf_dir=args.pdf_dir,node_ids={item['node']['id']},inventory=inventory),root)
                        row['outputs']=[{**entry,'sha256':vc.sha256(Path(entry['pdf']).read_bytes())} for entry in pdfs['checks']]
                        row['status']='pass'
                        row['phase']='complete'
                        row['seconds']=round(time.monotonic()-started,2)
                        print('Verified:',item['relative_path'],flush=True)
                    atomic_json(args.report,report)
                await bounded_checks(selected,verify_item,args.jobs)
            finally:
                await browser.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=Path('.'))
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--paths',nargs='+',help='Changed repository-relative files, including new partials')
    group.add_argument('--changed',action='store_true',help='Discover staged, unstaged and untracked files')
    group.add_argument('--all',action='store_true')
    parser.add_argument('--baseline',type=Path,help='Pre-edit manifest snapshot; enables ID/history and manifest-delta checks')
    parser.add_argument('--report',type=Path,default=Path('.cache/topic-checks/report.json'))
    parser.add_argument('--pdf-dir',type=Path,default=Path('.cache/topic-checks/pdfs'))
    parser.add_argument('--static-only',action='store_true',help='Intrinsic validation only; never claims browser/print acceptance')
    parser.add_argument('--no-cache',action='store_true')
    parser.add_argument('--jobs',type=int,choices=[1,2],default=2,help='Bound concurrent page checks (default 2)')
    args=parser.parse_args(argv);root=args.repo_root.resolve()
    args.report=args.report.resolve();args.pdf_dir=str(args.pdf_dir.resolve())
    previous={}
    if args.report.is_file():
        try: previous=vc.load_json(args.report)
        except (OSError,ValueError): pass
    started=time.monotonic()
    report={'executionStatus':'running','result':'pending','nodes':[]}
    atomic_json(args.report,report)
    try:
        config=vc.load_json(root/'tests/content/publishing.json')
        baseline=vc.load_json(args.baseline) if args.baseline else None
        intrinsic=vc.validate(root,config,baseline);report['intrinsic']=intrinsic
        if intrinsic['result']!='pass': raise vc.ValidationError('Whole-catalog intrinsic checks failed; see report')
        index=vc.index_manifest(vc.load_json(root/'manifest.json'),root,baseline)
        paths=changed_paths(root) if args.changed else (args.paths or [])
        for path in paths:
            if path.startswith('topics/') and path.endswith('.html') and path not in {i['relative_path'] for i in index.values()}:
                raise vc.ValidationError('Changed HTML path is not in the current catalog: '+path)
            if vc.repository_path(root,path)!=root/path: raise vc.ValidationError('Changed paths must be canonical repository-relative paths')
        selected,runtime=select_nodes(index,paths,all_nodes=args.all,research_records=config.get('researchRecords'))
        if baseline is not None: selected=apply_catalog_delta(index,selected,baseline,root)
        elif 'manifest.json' in paths:
            # Without a prior manifest there is no sound way to infer the affected entries.
            selected=list(index.values())
        report['selected']=[item['relative_path'] for item in selected]
        report['broaderApplicationRegressionRequired']=runtime
        report['historyStatus']='pass' if baseline else 'pending: no prior manifest supplied'
        if args.static_only:
            report.update(executionStatus='complete',result='pending',reason='Static checks passed; browser and print not executed')
        elif not selected:
            report.update(executionStatus='complete',result='pass',reason='No affected catalog entries; whole-catalog intrinsic checks passed')
        else:
            asyncio.run(browser_run(args,root,selected,report,previous))
            report.update(executionStatus='complete',result='pass' if not runtime else 'pending')
            if runtime: report['reason']='Catalog render/print checks passed; run full dashboard behavior regressions for shared runtime changes'
    except Exception as exc:
        report.update(executionStatus='complete',result='fail',reason=f'{type(exc).__name__}: {exc}')
        report['traceback']=traceback.format_exc(limit=5)
        for row in report['nodes']:
            if row['status']=='pending': row.update(status='fail',reason=report['reason'])
        print(report['reason'],file=sys.stderr)
    finally:
        report['seconds']=round(time.monotonic()-started,2)
        atomic_json(args.report,report)
    print(f"{report['result']}: {args.report}")
    return 0 if report['result']=='pass' or (args.static_only and report.get('intrinsic',{}).get('result')=='pass' and report['result']=='pending') else 1


if __name__=='__main__': raise SystemExit(main())
