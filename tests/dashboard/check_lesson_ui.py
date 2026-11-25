"""Real application acceptance for the compact lesson presentation (development only)."""
import argparse
import asyncio
import copy
import json
import sys
import time
import threading
import functools
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from datetime import datetime,timezone,timedelta
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools import validate_content as vc
from tools import migrate_lesson_presentation as migration
from tools.check_topics import serve,load_browser_checks,atomic_json,fingerprint,reusable,runtime_files
from playwright.async_api import async_playwright

NOW=datetime(2026,11,25,12,tzinfo=timezone.utc);STAMP='2026-11-25T12:00:00.000Z'

async def source_cases(browser,bases,baseline):
    inventory=vc.load_json(baseline/'inventory.json');index=vc.index_manifest(vc.load_json(ROOT/'manifest.json'),ROOT);rows=[]
    representatives={}
    for item in index.values():
        if item['node']['kind']!='topic':continue
        original=(baseline/'files'/item['relative_path']).read_text()
        note=next(n for n in vc.parsed_article(original).root.all() if 'data-interview-research' in n.attrs)
        representatives.setdefault(('variant',note.all('p')[0].text()),item)
        representatives.setdefault(('branch',item['route'].split('/')[2]),item)
    selected={i['node']['id']:i for i in representatives.values()}.values()
    for base in bases:
        context=await browser.new_context();page=await context.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        for item in selected:
            path=item['relative_path'];expected=inventory['nodes'][path]['sources']
            await page.goto(base+'#'+item['route'],wait_until='domcontentloaded')
            await page.locator('article[data-node-id="'+item['node']['id']+'"]').wait_for()
            note=page.locator('aside[data-interview-research]');assert await note.is_visible()
            assert await note.locator(':scope > h4').count()==1
            assert await note.locator(':scope > h4').inner_text()=='Sources'
            assert await note.locator('p').count()==0
            actual=await note.locator('a').evaluate_all('(es)=>es.map(e=>[e.getAttribute("href"),e.textContent.trim().replace(/\\s+/g," ")])')
            assert actual==[list(x) for x in expected],path
            response=await page.request.get(base+path);assert response.ok
            assert (await response.text())==(ROOT/path).read_text()
            rows.append({'base':base,'path':path,'sourceLinks':len(actual),'result':'pass'})
        assert not errors,errors;await context.close()
    return rows

async def cache_case(browser,baseline):
    checks=load_browser_checks();item=next(i for i in vc.index_manifest(vc.load_json(ROOT/'manifest.json'),ROOT).values() if i['node']['kind']=='topic')
    old=(baseline/'files'/item['relative_path']).read_bytes();new=item['path'].read_bytes();version=[0];requests=[]
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self,*_):pass
        def translate_path(self,path):
            if path.startswith('/backend-lab/'):path=path[len('/backend-lab'):]
            return super().translate_path(path)
        def do_GET(self):
            if self.path.split('?',1)[0].endswith('/'+item['relative_path']):
                requests.append({'version':version[0],'conditional':self.headers.get('If-None-Match')})
                body=old if version[0]==0 else new;self.send_response(200)
                self.send_header('Content-Type','text/html');self.send_header('Cache-Control','public,max-age=3600')
                self.send_header('ETag','"old"' if version[0]==0 else '"new"');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            else:super().do_GET()
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();rows=[]
    try:
        for suffix in ['/','/backend-lab/']:
            version[0]=0;context=await browser.new_context();page=await context.new_page();base=f'http://127.0.0.1:{server.server_port}'+suffix
            await page.goto(base);await checks.ready(page)
            text=await page.evaluate('(path)=>fetch(path,{cache:"force-cache"}).then(r=>r.text())',item['relative_path']);assert 'Researched ' in text
            count=len(requests);version[0]=1
            cached=await page.evaluate('(path)=>fetch(path,{cache:"force-cache"}).then(r=>r.text())',item['relative_path']);assert cached==text and len(requests)==count
            await page.goto(base+'#'+item['route']);await checks.ready(page,True)
            assert await page.locator('[data-interview-research] > h4').inner_text()=='Sources'
            assert await page.locator('[data-interview-research] p').count()==0 and len(requests)>count
            rows.append({'base':suffix,'warmOldCacheProved':True,'revalidatedCanonical':True,'result':'pass'});await context.close()
    finally:server.shutdown();server.server_close();thread.join(timeout=5)
    return rows

async def progress_cases(browser,bases,screenshots):
    checks=load_browser_checks();item=next(i for i in vc.index_manifest(vc.load_json(ROOT/'manifest.json'),ROOT).values() if i['node']['kind']=='topic');rows=[]
    screenshots.mkdir(parents=True,exist_ok=True)
    for bi,base in enumerate(bases):
        for width in [1024,1440,360]:
            for theme in ['light','dark']:
                context=await browser.new_context(viewport={'width':width,'height':1000},color_scheme=theme,reduced_motion='reduce');page=await context.new_page();await page.clock.set_fixed_time(NOW)
                await page.goto(base+'#'+item['route']);await checks.ready(page,True)
                if await page.locator('html').get_attribute('data-theme')!=theme:await page.locator('#theme-toggle').click();await checks.ready(page,True)
                assert await page.get_by_label('Progress',exact=True).count()==1
                select=page.locator('#topic-status');await select.evaluate('(e)=>e.dataset.stability="original"')
                for state in ['not-started','in-progress','mastered','active','completed']:
                    if state in ['not-started','in-progress','mastered']:
                        await select.focus();await select.select_option(state);assert await select.evaluate('(e)=>e===document.activeElement')
                    elif state=='active':
                        button=page.get_by_role('button',name='Start review',exact=True);await button.focus();await page.keyboard.press('Enter')
                        assert await page.get_by_role('button',name='Complete review',exact=True).evaluate('(e)=>e===document.activeElement')
                    else:
                        await page.get_by_role('button',name='Complete review',exact=True).focus();await page.keyboard.press('Enter');assert await page.get_by_role('button',name='Start another review',exact=True).evaluate('(e)=>e===document.activeElement')
                    assert await select.get_attribute('data-stability')=='original'
                    assert await page.locator('.lesson-toolbar').count()==1 and await page.locator('#mastery-actions,.mastery-footer').count()==0
                    geometry=await page.locator('.lesson-toolbar').evaluate('''e=>({height:e.getBoundingClientRect().height,targets:[...e.querySelectorAll('select,button')].map(x=>({w:x.getBoundingClientRect().width,h:x.getBoundingClientRect().height})),overflow:document.documentElement.scrollWidth>innerWidth+1})''')
                    assert geometry['height']<=(112 if width==360 else 56)+.5,(width,state,geometry)
                    assert not geometry['overflow'] and all(t['w']>=44 and t['h']>=44 for t in geometry['targets']),(width,state,geometry)
                    card=page.locator('details.kb-question').first
                    if not await card.evaluate('(e)=>e.open'):await card.locator('summary').click()
                    rating=card.get_by_role('button',name='Good',exact=True);await rating.focus();await page.keyboard.press('Space')
                    assert await rating.evaluate('(e)=>e===document.activeElement')
                    rows.append({'base':bi,'width':width,'theme':theme,'state':state,'geometry':geometry,'result':'pass'})
                    if bi==1 and width==360:
                        await page.locator('.lesson-toolbar').screenshot(path=str(screenshots/f'progress-row-{state}-{theme}.png'))
                        await page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                        await page.screenshot(path=str(screenshots/f'progress-{state}-{theme}.png'))
                await page.reload();await checks.ready(page,True);assert await select.input_value()=='mastered'
                assert await page.get_by_role('button',name='Start another review',exact=True).count()==1
                # Enlarged text may use more rows, but must retain readable controls and actions.
                await page.add_style_tag(content='.lesson-toolbar{font-size:26px!important}.review-date{font-size:24px!important}')
                enlarged=await page.locator('.lesson-toolbar').evaluate('''e=>({overflow:document.documentElement.scrollWidth>innerWidth+1,targets:[...e.querySelectorAll('select,button')].map(x=>({w:x.getBoundingClientRect().width,h:x.getBoundingClientRect().height,clipped:x.scrollWidth>x.clientWidth+1}))})''')
                assert not enlarged['overflow'] and all(t['w']>=44 and t['h']>=44 and not t['clipped'] for t in enlarged['targets']),(width,theme,enlarged)
                await select.focus();await page.keyboard.press('Tab');assert await page.get_by_role('button',name='Start another review',exact=True).evaluate('(e)=>e===document.activeElement')
                if bi==1 and width==360:await page.locator('.lesson-toolbar').screenshot(path=str(screenshots/f'progress-enlarged-{theme}.png'))
                rows.append({'base':bi,'width':width,'theme':theme,'state':'enlarged-text','geometry':enlarged,'result':'pass'})
                await context.close()
    return rows

async def state_cases(browser,bases):
    checks=load_browser_checks();manifest=vc.load_json(ROOT/'manifest.json');index=vc.index_manifest(manifest,ROOT)
    item=next(i for i in index.values() if i['node']['slug']=='blue-green-deployment')
    seed=vc.load_json(ROOT/'specs/002-dashboard-shell/contracts/progress-backup.example.json')['state'];seed['updatedAt']=STAMP
    for branch in manifest['roots'][0]['children']:
        old=next(i for i in index.values() if i['node']['kind']=='topic' and i['route'].startswith('/system-design/'+branch['slug']+'/'))
        key=vc.article_inventory(old['path'].read_text())['foundationalKeys'][0]
        seed['topics'][old['node']['id']]={'status':'in-progress','lastVisitedAt':STAMP,'confidence':{key:{'rating':'good','ratedAt':STAMP}},'review':None}
    seed['topics']['unknown-imported-topic']={'status':'in-progress','lastVisitedAt':STAMP,'confidence':{},'review':None}
    before=copy.deepcopy(seed);known={i['node']['id'] for i in index.values() if i['node']['kind']=='topic'};mastered=sum(k in known and r['status']=='mastered' for k,r in seed['topics'].items());rows=[]
    async def state(page):return await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')
    for base in bases:
        context=await browser.new_context(accept_downloads=True);await context.add_init_script('if(!localStorage.getItem("backend-lab.learning.v1"))localStorage.setItem("backend-lab.learning.v1",'+json.dumps(json.dumps(seed))+')')
        page=await context.new_page();await page.clock.set_fixed_time(NOW+timedelta(minutes=1));await page.goto(base+'#'+item['route']);await checks.ready(page,True)
        card=page.locator('details.kb-question').first;key=await card.get_attribute('data-recall-id');await card.locator('summary').click()
        for rating in ['Hard','Good','Easy']:await card.get_by_role('button',name=rating,exact=True).click()
        assert await page.locator('#topic-status').input_value()=='not-started' and (await state(page))['topics'][item['node']['id']]['review'] is None
        await page.locator('#topic-status').select_option('in-progress');await page.reload();await checks.ready(page,True)
        assert await page.locator('[data-recall-id="'+key+'"] [data-confidence=easy]').get_attribute('aria-pressed')=='true'
        await page.goto(base);await checks.ready(page);assert await page.locator('#continue-learning').get_attribute('href')=='#'+item['route']
        await page.locator('#continue-learning').click();await checks.ready(page,True);await page.locator('#topic-status').select_option('mastered')
        assert await page.locator('#global-percent').inner_text()==str(int((mastered+1)/len(known)*100+.5))+'%'
        await page.get_by_role('button',name='Start review',exact=True).click();active=(await state(page))['topics'][item['node']['id']]['review']['session']['id']
        await page.reload();await checks.ready(page,True);assert await page.get_by_role('button',name='Complete review',exact=True).count()==1
        card=page.locator('details.kb-question').first;await card.locator('summary').click();await card.get_by_role('button',name='Good',exact=True).click()
        current=await state(page);review=current['topics'][item['node']['id']]['review'];assert len(review['history'])==1 and review['session']['id']==active and review['session']['completedAt'] is None
        await page.get_by_role('button',name='Complete review',exact=True).click();current=await state(page);review=current['topics'][item['node']['id']]['review'];assert review['intervalIndex']==1 and len(review['history'])==2
        replay=await page.evaluate('''async x=>{const m=await import('./assets/js/learning-state.js');return m.completeReview(x.state,x.id,x.token,x.now)}''',{'state':current,'id':item['node']['id'],'token':active,'now':STAMP});assert replay==current
        for identity,record in before['topics'].items():assert current['topics'][identity]==record,identity
        async with page.expect_download() as info:await page.locator('#export-progress').click()
        backup=json.loads(Path(await (await info.value).path()).read_text());assert backup['state']==current
        await checks.import_payload(page,backup);assert await state(page)==current
        await page.reload();await checks.ready(page,True);assert await page.get_by_role('button',name='Start another review',exact=True).count()==1
        await page.locator('#topic-status').select_option('in-progress');left=await state(page);assert left['topics'][item['node']['id']]['review']['session'] is None
        await page.locator('#topic-status').select_option('in-progress');assert await state(page)==left
        await page.locator('#topic-status').select_option('mastered');remastered=(await state(page))['topics'][item['node']['id']]['review'];assert remastered['cycle']==2 and remastered['intervalIndex']==0 and len(remastered['history'])==3
        rows.append({'base':base,'seededBranches':len(manifest['roots'][0]['children']),'unknownRecordsPreserved':True,'confidenceAndExplicitReview':True,'reloadAndBackup':True,'staleCompletionNoop':True,'remastery':True,'result':'pass'});await context.close()
    intervals=[]
    for interval,days in enumerate([3,7,14,30]):
        fixture=copy.deepcopy(seed);history=[{'cycle':1,'kind':'mastered' if j==0 else 'review','sessionId':None if j==0 else '10000000-0000-4000-8000-00000000000'+str(j),'reviewedAt':STAMP,'intervalIndex':j} for j in range(interval+1)]
        fixture['topics'][item['node']['id']]={'status':'mastered','lastVisitedAt':STAMP,'confidence':{},'review':{'cycle':1,'lastReviewed':STAMP,'intervalIndex':interval,'history':history,'session':None}}
        context=await browser.new_context();await context.add_init_script('if(!localStorage.getItem("backend-lab.learning.v1"))localStorage.setItem("backend-lab.learning.v1",'+json.dumps(json.dumps(fixture))+')');page=await context.new_page()
        for due,offset in [(False,timedelta(days=days,milliseconds=-1)),(True,timedelta(days=days))]:
            await page.clock.set_fixed_time(NOW+offset);await page.goto(bases[1]);await checks.ready(page)
            assert bool(await page.locator('#due-list a[href="#'+item['route']+'"]').count())==due,(interval,due)
        intervals.append({'days':days,'beforeDue':False,'atDue':True,'result':'pass'});await context.close()
    return {'bases':rows,'intervals':intervals}

async def related_cases(browser,bases,baseline):
    inventory=vc.load_json(baseline/'inventory.json');index=vc.index_manifest(vc.load_json(ROOT/'manifest.json'),ROOT);rows=[]
    for bi,base in enumerate(bases):
        context=await browser.new_context(viewport={'width':360,'height':900});page=await context.new_page()
        for item in index.values():
            if item['node']['kind']!='topic':continue
            path=item['relative_path'];old=vc.parsed_article((baseline/'files'/path).read_text());expected=[(a.attrs.get('href'),a.text()) for f in old.root.all('footer') for a in f.all('a')]
            source=item['path'].read_text();parsed=vc.parsed_article(source)
            actual=[(a.attrs.get('href'),a.text()) for f in parsed.root.all('footer') for a in f.all('a')]
            assert actual==expected and migration.INTRO not in source,path
            if not expected:continue
            # Static all-file preservation is paired with representative real navigation.
            if item['node']['slug'] not in ['distributed-system-fundamentals','container-orchestration','horizontal-pod-autoscaling','sql-vs-nosql']:continue
            await page.goto(base+'#'+item['route'],wait_until='domcontentloaded');await page.locator('article[data-node-id="'+item['node']['id']+'"]').wait_for()
            footer=page.locator('article footer');assert await footer.count()==1
            for href,_ in expected:
                if href.startswith('#/'):
                    await footer.locator('a[href="'+href+'"]').click();await page.locator('article[data-node-id="'+index[href[1:]]['node']['id']+'"]').wait_for()
                    await page.goto(base+'#'+item['route'],wait_until='domcontentloaded');await page.locator('article[data-node-id="'+item['node']['id']+'"]').wait_for()
            assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            rows.append({'base':bi,'path':path,'links':len(expected),'result':'pass'})
        await context.close()
    return rows

def verify_catalog(path):
    if path is None:raise ValueError('Final acceptance requires --catalog-report')
    report=vc.load_json(path);index=vc.index_manifest(vc.load_json(ROOT/'manifest.json'),ROOT)
    assert report['executionStatus']=='complete' and report['intrinsic']['result']=='pass'
    assert report.get('broaderApplicationRegressionRequired') is True
    assert report['result']=='pending' and report.get('reason')=='Catalog render/print checks passed; run full dashboard behavior regressions for shared runtime changes'
    assert set(report['selected'])=={i['relative_path'] for i in index.values()}
    assert len(report['nodes'])==len(index)
    for item in index.values():
        row=next(r for r in report['nodes'] if r['nodeId']==item['node']['id'])
        key=fingerprint(ROOT,item,{'chromium':report['browser'],'playwright':report['playwright']})
        assert reusable(row,key),item['relative_path']
        assert len(row['browserCases'])==3 and all(c['status']=='pass' for c in row['browserCases'])
    return {'result':'pass','report':str(path),'sha256':vc.sha256(path.read_bytes()),'nodes':len(index),'browserCases':len(index)*3,'pdfs':len(index)*2,'originalResult':'pending: broader application regression'}

async def current_journeys(browser,bases,catalog_component):
    checks=load_browser_checks();args=SimpleNamespace(base_url=bases[0],project_url=bases[1]);rows=[]
    for story in ['US1','US2','US3','US4','US5','US6']:
        for fn in checks.SCENARIOS[story]:
            if fn.__name__=='print_articles':
                rows.append({'story':story,'scenario':fn.__name__,'result':'pending','requiresFinalCatalogPdfs':True});continue
            result=await fn(browser,args,ROOT)
            rows.append({'story':story,'scenario':fn.__name__,'result':'pass','details':result})
            print('Current dashboard:',story,fn.__name__,'pass',flush=True)
    return rows

async def main(args):
    result={'result':'pending','story':args.story,'checks':{}}
    if args.story=='all':
        if args.catalog_report is None or not args.catalog_report.is_file():raise ValueError('Final acceptance requires an existing --catalog-report')
        initial=vc.load_json(args.catalog_report)
        result['checks']['catalog']=verify_catalog(args.catalog_report) if initial['executionStatus']=='complete' else {'result':'pending','report':str(args.catalog_report)}
    atomic_json(args.report,result)
    with serve(ROOT) as bases:
        async with async_playwright() as p:
            browser=await p.chromium.launch(headless=True,args=['--no-sandbox'])
            original_context=browser.new_context
            async def test_context(**options):
                options.setdefault('reduced_motion','reduce');context=await original_context(**options)
                await context.add_init_script('document.addEventListener("DOMContentLoaded",()=>document.documentElement.style.scrollBehavior="auto",{once:true})')
                return context
            browser.new_context=test_context
            try:
                if args.story=='US1':
                    result['checks']['sources']=await source_cases(browser,bases,args.baseline)
                    result['checks']['cache']=await cache_case(browser,args.baseline)
                elif args.story=='US2':
                    result['checks']['progress']=await progress_cases(browser,bases,args.screenshots)
                    result['checks']['state']=await state_cases(browser,bases)
                elif args.story=='US3':result['checks']['related']=await related_cases(browser,bases,args.baseline)
                elif args.story=='all':
                    result['checks']['sources']=await source_cases(browser,bases,args.baseline);print('Feature sources pass',flush=True)
                    result['checks']['cache']=await cache_case(browser,args.baseline);print('Feature cache pass',flush=True)
                    result['checks']['progress']=await progress_cases(browser,bases,args.screenshots);print('Feature progress pass',flush=True)
                    result['checks']['state']=await state_cases(browser,bases);print('Feature state pass',flush=True)
                    result['checks']['related']=await related_cases(browser,bases,args.baseline);print('Feature related pass',flush=True)
                    result['checks']['journeys']=await current_journeys(browser,bases,result['checks']['catalog'])
                    migration.run(ROOT,args.baseline,verify=True)
                    # Independent application checks can overlap catalog rendering. Final
                    # acceptance and print reuse must wait for its actual complete report.
                    deadline=time.monotonic()+7200
                    while vc.load_json(args.catalog_report)['executionStatus']!='complete':
                        if time.monotonic()>deadline:raise TimeoutError('Catalog acceptance did not finish')
                        atomic_json(args.report,result);await asyncio.sleep(10)
                    result['checks']['catalog']=verify_catalog(args.catalog_report)
                    for row in result['checks']['journeys']:
                        if row.get('requiresFinalCatalogPdfs'):
                            row.update(result='pass',reusedVerifiedCatalogPdfs=result['checks']['catalog']['pdfs'])
                else:raise ValueError('Story runner is not yet implemented')
                result['result']='pass'
            except Exception as e:
                result.update(result='fail',reason=f'{type(e).__name__}: {e}');raise
            finally:
                result['inputHashes']={path:vc.sha256((ROOT/path).read_bytes()) for path in runtime_files(ROOT)+['tests/dashboard/check_lesson_ui.py','tools/validate_content.py','tools/check_topics.py','tests/content/publishing.json','.specify/memory/constitution.md']}
                atomic_json(args.report,result);await browser.close()
    print('PASS',args.story,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--story',choices=['US1','US2','US3','all'],default='all');p.add_argument('--baseline',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--catalog-report',type=Path);p.add_argument('--screenshots',type=Path,default=Path('.cache/lesson-ui/visual'));asyncio.run(main(p.parse_args()))
