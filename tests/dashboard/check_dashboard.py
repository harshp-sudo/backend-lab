"""Actual-dashboard browser acceptance. Development tooling, never a runtime dependency."""
import argparse
import asyncio
import json
import platform
import re
import subprocess
import sys
import copy
import hashlib
import time
import unicodedata
from html.parser import HTMLParser
from datetime import datetime, timezone
from pathlib import Path
from playwright.async_api import async_playwright

SCENARIOS = {}

def scenario(story):
    def register(fn):
        SCENARIOS.setdefault(story, []).append(fn)
        return fn
    return register

def catalog(root):
    result = []
    def walk(node, chain=()):
        route = '/' + '/'.join((*chain, node['slug']))
        result.append({**node, 'route': route})
        for child in node.get('children', []):
            walk(child, (*chain, node['slug']))
    for node in json.loads((root/'manifest.json').read_text())['roots']:
        walk(node)
    return result


def current_inventory(root, *, preserve=False):
    """Derive current counts; frozen preservation is an explicit migration concern."""
    sys.path.insert(0,str(root))
    from tools import validate_content as vc
    frozen={}
    if preserve:
        baseline=vc.load_json(root/'specs/003-backfill-interview-scenarios/contracts/preservation-baseline.json')
        frozen={e['id']:e for e in baseline['lessons']}
    nodes={}
    for node in catalog(root):
        relative='topics'+node['route']+('/_overview.html' if node['kind']=='hub' else '.html')
        source=(root/relative).read_bytes().decode('utf-8');value=vc.article_inventory(source)
        value.update(path=relative,sourceSha256=vc.sha256(source.encode('utf-8')))
        if node['kind']=='topic':
            assert 3<=len(value['foundationalKeys'])<=5
            assert 5<=len(value['interviewKeys'])<=7
            if node['id'] in frozen:
                assert value['foundationalKeys']==[x['key'] for x in frozen[node['id']]['foundationalRecall']]
                assert vc.sha256(vc.strip_interview_block(source).encode('utf-8'))==frozen[node['id']]['sourceSha256']
        nodes[node['id']]=value
    foundations=sum(len(v['foundationalKeys']) for v in nodes.values())
    interviews=sum(len(v['interviewKeys']) for v in nodes.values())
    return {'topicCount':sum(n['kind']=='topic' for n in catalog(root)),'nodes':nodes,'foundational':foundations,'interviews':interviews,'questions':foundations+interviews,'diagrams':sum(v['diagrams'] for v in nodes.values())}

async def ready(page, article=False):
    await page.locator('#main-content[aria-busy="false"]').wait_for()
    if article:
        await page.locator('#main-content > article').wait_for()
        await page.wait_for_function("!document.querySelector('article[data-enhancement=\"pending\"]')")

@scenario('US1')
async def navigation(browser,args,root):
    nodes=catalog(root);result=[]
    for base in [args.base_url,args.project_url]:
        context=await browser.new_context(viewport={'width':1440,'height':1000})
        page=await context.new_page();errors=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('request',lambda r:requests.append(r.url))
        await page.goto(base);await ready(page)
        for node in nodes:
            # The actual sidebar links must work, including their collapsed ancestors.
            await page.evaluate("""() => document.querySelectorAll('.branch-toggle[aria-expanded=false]').forEach(b=>b.click())""")
            await page.locator('#library-nav a').filter(has=page.locator('span')).count()
            await page.locator('#library-nav a[href="#'+node['route']+'"]').click()
            await ready(page,True)
            assert await page.locator('article').get_attribute('data-node-id')==node['id']
            assert await page.locator('article > h1').inner_text()==node['title']
            await page.reload();await ready(page,True)
            assert await page.locator('article').get_attribute('data-node-id')==node['id']
        edges=0
        for node in [n for n in nodes if n['kind']=='hub']:
            for child in node['children']:
                await page.goto(base+'#'+node['route']);await ready(page,True)
                link=page.locator('[data-child-links] > li > a').filter(has_text=child['title'])
                await link.click();await ready(page,True)
                assert await page.locator('article').get_attribute('data-node-id')==child['id'];edges+=1
        sample=next(n for n in nodes if n['slug']=='clean-architecture')
        await page.goto(base+'#'+sample['route']+'?section=mechanics');await ready(page,True)
        assert await page.locator('[data-section=mechanics] h2').evaluate('(e)=>document.activeElement===e')
        await page.goto(base+'#/unknown');await ready(page)
        assert await page.locator('.error-view').count()==1
        # Unknown routes never fetch an unindexed HTML path.
        assert not any('/unknown.html' in u for u in requests)
        local=[u for u in requests if '/topics/' in u]
        assert all(u.startswith(base+'topics/') for u in local),local
        assert not errors,errors
        result.append({'base':base,'clickedAndReloaded':len(nodes),'hubEdges':edges,'consoleErrors':errors,'contentPathsRelative':True})
        await context.close()
    return result

@scenario('US1')
async def navigation_failures_and_depth(browser,args,root):
    nodes=catalog(root);topics=[n for n in nodes if n['kind']=='topic'];details=[]
    context=await browser.new_context();page=await context.new_page();uncaught=[];page.on('pageerror',lambda e:uncaught.append(str(e)))
    await page.route('**/manifest.json',lambda r:r.fulfill(status=503,body='Unavailable'))
    await page.goto(args.base_url);await ready(page);assert await page.locator('.error-view').count()==1
    await page.unroute('**/manifest.json');await page.get_by_role('button',name='Try again').click();await ready(page);assert await page.locator('#mastery-value').count()==1
    node=topics[0];pattern='**/topics'+node['route']+'.html'
    await page.route(pattern,lambda r:r.fulfill(body='<article class="kb-topic" data-node-id="wrong"><h1>Wrong</h1></article>',content_type='text/html'))
    await page.goto(args.base_url+'#'+node['route']);await ready(page);assert await page.locator('.error-view').count()==1
    await page.unroute(pattern)
    async def slow(route):
        await asyncio.sleep(.3)
        try:await route.fulfill(body=(root/('topics'+node['route']+'.html')).read_text(),content_type='text/html')
        except Exception:pass  # Expected when the obsolete request is aborted.
    await page.route(pattern,slow)
    await page.evaluate('(h)=>location.hash=h','#'+node['route']);await page.wait_for_timeout(30)
    await page.evaluate('(h)=>location.hash=h','#'+topics[1]['route']);await page.wait_for_function('(id)=>document.querySelector("article")?.dataset.nodeId===id',arg=topics[1]['id']);await ready(page,True);await page.wait_for_timeout(350)
    assert await page.locator('article').get_attribute('data-node-id')==topics[1]['id']
    await page.unroute(pattern)
    await page.evaluate('(h)=>location.hash=h','#'+topics[2]['route']);await page.wait_for_function('(id)=>document.querySelector("article")?.dataset.nodeId===id',arg=topics[2]['id']);await ready(page,True)
    await page.go_back();await page.wait_for_function('(id)=>document.querySelector("article")?.dataset.nodeId===id',arg=topics[1]['id']);await ready(page,True)
    await page.go_forward();await page.wait_for_function('(id)=>document.querySelector("article")?.dataset.nodeId===id',arg=topics[2]['id']);await ready(page,True)
    assert 'Modular Monolith' in await page.locator('#breadcrumbs').inner_text()
    assert not uncaught,uncaught;await context.close()
    manifest=json.loads((root/'manifest.json').read_text())
    for name in ['inner','outer']:manifest={'schemaVersion':1,'roots':[{'id':'test-'+name,'kind':'hub','slug':name,'title':name.title(),'children':manifest['roots']}]}
    context=await browser.new_context();page=await context.new_page();await page.route('**/manifest.json',lambda r:r.fulfill(json=manifest))
    route='/outer/inner'+node['route'];await page.route('**/topics'+route+'.html',lambda r:r.fulfill(body=(root/('topics'+node['route']+'.html')).read_text(),content_type='text/html'))
    await page.goto(args.project_url+'#'+route);await ready(page,True)
    assert await page.locator('article').get_attribute('data-node-id')==node['id']
    assert await page.locator('#breadcrumbs a').count()==6
    await context.close();return {'manifestFailureAndRetry':'pass','identityMismatch':'pass','latestRequestWins':'pass','historyAndBreadcrumbs':'pass','recursiveLevels':6,'uncaughtErrors':uncaught}

@scenario('US2')
async def dashboard(browser,args,root):
    nodes=catalog(root);topics=[n for n in nodes if n['kind']=='topic'];example=json.loads((root/'specs/002-dashboard-shell/contracts/progress-backup.example.json').read_text())['state']
    categories=sum(max(1,sum(child['kind']=='hub' for child in node['children'])) for node in json.loads((root/'manifest.json').read_text())['roots'])
    page=await browser.new_page()
    await page.goto(args.base_url);await ready(page)
    assert await page.locator('#mastery-value').inner_text()=='0%'
    assert await page.locator('.category-card').count()==categories
    for count in [min(3,len(topics)),len(topics)]:
        state=json.loads(json.dumps(example));record=next(iter(state['topics'].values()));state['topics']={t['id']:json.loads(json.dumps(record)) for t in topics[:count]}
        await page.evaluate('(s)=>localStorage.setItem("backend-lab.learning.v1",JSON.stringify(s))',state)
        await page.reload();await ready(page)
        expected=str(int(count/len(topics)*100+.5))+'%'
        assert await page.locator('#mastery-value').inner_text()==expected
        assert await page.locator('#global-percent').inner_text()==expected
        assert await page.locator('#due-list > li').count()==count
    await page.close()
    context=await browser.new_context();empty=await context.new_page()
    await empty.route('**/manifest.json',lambda route:route.fulfill(json={'schemaVersion':1,'roots':[]}))
    await empty.goto(args.base_url);await ready(empty)
    assert await empty.locator('#mastery-value').inner_text()=='0%'
    assert 'library is ready to grow' in (await empty.locator('main').inner_text()).lower()
    await context.close()
    return {'seededCounts':[0,min(3,len(topics)),len(topics)],'emptyCatalog':'pass','categoryCards':categories}

@scenario('US3')
async def lessons(browser,args,root):
    nodes=catalog(root);results=[];inventory=current_inventory(root)
    for base in [args.base_url,args.project_url]:
        context=await browser.new_context(viewport={'width':1440,'height':1000});page=await context.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        diagrams=questions=0
        for node in nodes:
            await page.goto(base+'#'+node['route']);await ready(page,True)
            assert await page.locator('article').get_attribute('data-enhancement')=='complete',await page.locator('#route-status').inner_text()
            count=await page.locator('pre.mermaid svg').count();assert count==inventory['nodes'][node['id']]['diagrams'];diagrams+=count
            assert await page.locator('svg.flowchart foreignObject').count()==0
            for q in await page.locator('details.kb-question').all():
                assert not await q.evaluate('(e)=>e.open')
                summary=q.locator('summary');await summary.focus();await page.keyboard.press('Enter');assert await q.evaluate('(e)=>e.open')
                await q.get_by_role('button',name='Good',exact=True).click();assert await q.evaluate('(e)=>e.open')
                await summary.focus();await page.keyboard.press('Space');assert not await q.evaluate('(e)=>e.open');questions+=1
            if node['kind']=='topic':
                await page.get_by_role('button',name='Mark as Mastered',exact=True).click()
                assert await page.locator('#topic-status').input_value()=='mastered'
                await page.reload();await ready(page,True)
                assert await page.locator('#topic-status').input_value()=='mastered'
                assert await page.locator('[data-confidence=good][aria-pressed=true]').count()==await page.locator('details.kb-question').count()
        assert diagrams==inventory['diagrams'] and questions==inventory['questions'],(diagrams,questions)
        assert not errors,errors
        results.append({'base':base,'articles':len(nodes),'diagrams':diagrams,'recallQuestions':questions,'foundational':inventory['foundational'],'interviews':inventory['interviews'],'consoleErrors':errors})
        await context.close()
    return results

@scenario('US3')
async def enhancement_failures(browser,args,root):
    nodes=catalog(root)
    node=next(n for n in nodes if n['kind']=='topic' and 'language-' in (root/('topics'+n['route']+'.html')).read_text())
    results=[]
    for pattern in ['**/mermaid@12.3.0/**','**/@highlightjs/cdn-assets@11.11.1/**']:
        context=await browser.new_context();await context.route(pattern,lambda route:route.abort())
        page=await context.new_page();uncaught=[];page.on('pageerror',lambda e:uncaught.append(str(e)))
        await page.goto(args.base_url+'#'+node['route']);await ready(page,True)
        assert await page.locator('article').get_attribute('data-enhancement')=='error'
        assert await page.locator('article p').count()>15
        assert await page.locator('details.kb-question').count()>=3
        await context.unroute(pattern);await page.get_by_role('button',name='Retry diagrams and code').click()
        await page.wait_for_function('document.querySelector("article")?.dataset.enhancement==="complete"')
        assert not uncaught,uncaught
        results.append({'blocked':pattern,'completeProsePreserved':True,'retry':'pass','uncaughtErrors':uncaught});await context.close()
    return results

@scenario('US4')
async def reviews(browser,args,root):
    example=json.loads((root/'specs/002-dashboard-shell/contracts/progress-backup.example.json').read_text())['state']
    node=next(n for n in catalog(root) if n['slug']=='clean-architecture')
    context=await browser.new_context();await context.add_init_script('if(!localStorage.getItem("backend-lab.learning.v1"))localStorage.setItem("backend-lab.learning.v1",'+json.dumps(json.dumps(example))+')')
    page=await context.new_page();await page.clock.install(time=datetime(2026,11,17,6,tzinfo=timezone.utc))
    await page.goto(args.base_url);await ready(page);assert await page.locator('#due-list > li').count()==1
    await page.locator('#due-list a').click();await ready(page,True)
    before=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')
    await page.get_by_role('button',name='Start another review',exact=True).click();await page.get_by_role('button',name='Complete review',exact=True).click()
    after=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))');assert after['topics'][node['id']]['review']['intervalIndex']==2
    assert len(after['topics'][node['id']]['review']['history'])==len(before['topics'][node['id']]['review']['history'])+1
    await page.reload();await ready(page,True)
    assert await page.get_by_role('button',name='Start another review',exact=True).count()==1
    await page.locator('.brand').click();await ready(page);assert await page.locator('#due-list > li').count()==0
    await context.close()
    return {'explicitCompletion':'pass','persistedIndex':2,'completedSessionRetained':True,'queueRefresh':'pass'}

@scenario('US5')
async def search(browser,args,root):
    context=await browser.new_context();page=await context.new_page();await page.goto(args.base_url);await ready(page)
    samples=[]
    for shortcut in ['Control+k','Meta+k']:
        await page.keyboard.press(shortcut);await page.locator('#search-dialog[open]').wait_for()
        assert await page.locator('#search-input').evaluate('(e)=>e===document.activeElement')
        await page.keyboard.press('Escape');await page.locator('#search-dialog:not([open])').wait_for(state='attached')
    await page.locator('#search-open').click()
    for query in ['Clean Architecture','system design','microservces']*10:
        start=time.monotonic();await page.locator('#search-input').fill(query);await page.wait_for_function('document.querySelectorAll("#search-results li").length>0');samples.append((time.monotonic()-start)*1000)
    await page.locator('#search-input').fill('Clean Architecture');assert 'Clean Architecture' in await page.locator('#search-results li').first.inner_text()
    await page.keyboard.press('Enter');await ready(page,True);assert await page.locator('article > h1').inner_text()=='Clean Architecture'
    assert await page.locator('#search-dialog').evaluate('(e)=>!e.open')
    assert sum(v<=200 for v in samples)>=29,samples
    await context.close();return {'interactions':30,'within200ms':sum(v<=200 for v in samples),'latencyMs':samples,'shortcuts':['Control+k','Meta+k'],'keyboardResultActivation':'pass'}

@scenario('US6')
async def workspace(browser,args,root):
    context=await browser.new_context(viewport={'width':360,'height':800},color_scheme='light');page=await context.new_page()
    await page.goto(args.project_url);await ready(page)
    await page.locator('#drawer-open').click();assert await page.locator('#drawer-dialog').evaluate('(e)=>e.open')
    await page.keyboard.press('Escape');assert not await page.locator('#drawer-dialog').evaluate('(e)=>e.open')
    assert await page.locator('#drawer-open').evaluate('(e)=>e===document.activeElement')
    await page.locator('#drawer-open').click();await page.set_viewport_size({'width':1440,'height':1000});assert not await page.locator('#drawer-dialog').evaluate('(e)=>e.open')
    assert await page.locator('#desktop-sidebar #sidebar').count()==1
    await page.locator('#theme-toggle').click();assert await page.locator('html').get_attribute('data-theme')=='dark'
    await page.reload();await ready(page);assert await page.locator('html').get_attribute('data-theme')=='dark'
    before=await page.evaluate('localStorage.getItem("backend-lab.learning.v1")')
    example=root/'specs/002-dashboard-shell/contracts/progress-backup.example.json'
    await page.locator('#import-file').set_input_files(example);await page.locator('#import-dialog[open]').wait_for()
    assert '1 current' in await page.locator('#import-summary').inner_text()
    await page.get_by_role('button',name='Cancel',exact=True).click();assert await page.evaluate('localStorage.getItem("backend-lab.learning.v1")')==before
    await page.locator('#import-file').set_input_files(example);await page.locator('#confirm-import').click()
    expected=json.loads(example.read_text())['state'];actual=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))');assert actual==expected
    async with page.expect_download() as downloaded:
        await page.locator('#export-progress').click()
    download=await downloaded.value;path=await download.path();backup=json.loads(Path(path).read_text());assert backup['state']==expected
    invalid={'name':'invalid.json','mimeType':'application/json','buffer':b'{"version":2}'}
    await page.locator('#import-file').set_input_files(invalid);assert await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')==expected
    assert await page.locator('#import-error').inner_text()
    await page.keyboard.press('Escape')
    await page.set_viewport_size({'width':360,'height':800});await page.wait_for_timeout(100)
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),await page.evaluate('document.documentElement.scrollWidth')
    await page.screenshot(path='/tmp/backend-dashboard-mobile.png',full_page=True)
    api=next(n for n in catalog(root) if n['slug']=='api-gateway-pattern')
    await page.goto(args.project_url+'#'+api['route']);await ready(page,True)
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    await page.locator('article details summary').first.focus();await page.keyboard.press('Enter')
    disclosed=await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')
    await page.locator('#theme-toggle').click();await ready(page,True)
    assert await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')==disclosed
    await page.locator('#topic-status').focus();await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter')
    assert await page.locator('#topic-status').input_value()=='in-progress'
    await page.locator('#drawer-open').click();await page.locator('#library-nav a[href="#/system-design"]').click();await ready(page,True)
    assert not await page.locator('#drawer-dialog').evaluate('(e)=>e.open')
    assert await page.locator('article > h1').inner_text()=='System Design'
    await context.close()
    fresh=await browser.new_context();p=await fresh.new_page();await p.goto(args.base_url);await ready(p)
    await p.locator('#import-file').set_input_files(example);await p.locator('#confirm-import').click();assert await p.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')==expected
    await fresh.close();return {'viewport':360,'drawerAndResize':'pass','themeReload':'pass','backupRoundtrip':'pass','cancelAndInvalidUnchanged':True,'unknownRecordsRetained':True}

@scenario('US6')
async def persistence_failures(browser,args,root):
    node=next(n for n in catalog(root) if n['kind']=='topic');example=root/'specs/002-dashboard-shell/contracts/progress-backup.example.json'
    for mode in ['corrupt','quota']:
        context=await browser.new_context()
        script='if(!localStorage.getItem("backend-lab.learning.v1"))localStorage.setItem("backend-lab.learning.v1","{broken");' if mode=='corrupt' else 'Storage.prototype.setItem=function(){throw new DOMException("Quota exceeded","QuotaExceededError")};'
        await context.add_init_script(script);page=await context.new_page();await page.goto(args.base_url+'#'+node['route']);await ready(page,True)
        await page.get_by_role('button',name='Mark as Mastered',exact=True).click();assert 'not saved' in (await page.locator('#persistence-notice').inner_text()).lower()
        raw=await page.evaluate('localStorage.getItem("backend-lab.learning.v1")');assert raw==('{broken' if mode=='corrupt' else None)
        async with page.expect_download() as dl:await page.locator('#export-progress').click()
        backup=json.loads(Path(await (await dl.value).path()).read_text());assert backup['state']['topics'][node['id']]['status']=='mastered'
        await page.locator('#import-file').set_input_files(example);await page.locator('#confirm-import').click()
        if mode=='corrupt':
            assert await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')==json.loads(example.read_text())['state']
            assert await page.locator('#persistence-notice').is_hidden()
        else:
            assert 'unchanged' in await page.locator('#import-error').inner_text();assert await page.evaluate('localStorage.getItem("backend-lab.learning.v1")') is None
            await page.keyboard.press('Escape')
            async with page.expect_download() as dl2:await page.locator('#export-progress').click()
            assert json.loads(Path(await (await dl2.value).path()).read_text())['state']==backup['state']
        await context.close()
    return {'corruptBytesPreserved':'pass','quotaSessionExport':'pass','validRecovery':'pass','failedImportMemoryAndStorageUnchanged':'pass'}

class Paragraphs(HTMLParser):
    def __init__(self):super().__init__();self.values=[];self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=='p':self.current=[]
    def handle_data(self,data):
        if self.current is not None:self.current.append(data)
    def handle_endtag(self,tag):
        if tag=='p' and self.current is not None:self.values.append(''.join(self.current));self.current=None

def normalized(text):return re.sub(r'\s+','',unicodedata.normalize('NFKC',text)).replace('\u00ad','')


def source_print_texts(source):
    """Protect full prose plus prompts, labels, headings, tables and source-link text."""
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
    from tools import validate_content as vc
    parser=vc.parsed_article(source)
    tags={'p','summary','h1','h2','h3','th','td','figcaption','li','code'}
    # Decorative leading heading emoji are not reliably encoded by PDF fonts.
    return [re.sub(r'^[^\w]+','',e.text()) if e.tag in {'h1','h2','h3'} else e.text()
            for e in parser.root.all() if e.tag in tags and e.text()]


def learning_invariants(actual, original, inventories, *, rated=False):
    """Visits may update timestamps; prior status/review/confidence must not change."""
    assert set(actual['topics'])==set(original['topics'])
    for identity,old in original['topics'].items():
        current=actual['topics'][identity]
        assert current['status']==old['status'],identity
        assert current['review']==old['review'],identity
        for key,value in old['confidence'].items(): assert current['confidence'][key]==value,(identity,key)
        if not rated and identity in inventories:
            assert not set(inventories[identity]['interviewKeys']) & set(current['confidence']),identity


async def import_payload(page, payload):
    await page.locator('#import-file').set_input_files({'name':'migration-backup.json','mimeType':'application/json','buffer':json.dumps(payload).encode()})
    await page.locator('#import-dialog[open]').wait_for()
    await page.locator('#confirm-import').click()
    await page.locator('#import-dialog').wait_for(state='hidden')


@scenario('MIGRATION')
async def migration_learning(browser,args,root):
    inventory=current_inventory(root,preserve=True);topics=[n for n in catalog(root) if n['kind']=='topic'];proof={}
    example=json.loads((root/'specs/002-dashboard-shell/contracts/progress-backup.example.json').read_text())
    template=example['state']['topics'][next(n['id'] for n in topics if n['slug']=='clean-architecture')]
    old=copy.deepcopy(example['state']);old['preferences']['theme']='light';old['topics']={}
    for i,node in enumerate(topics):
        record=copy.deepcopy(template);record['status']=['not-started','in-progress','mastered'][i%3]
        if record['status']!='mastered':record['review']=None
        record['confidence']={key:{'rating':['hard','good','easy'][j%3],'ratedAt':'2026-11-17T05:00:00.000Z'} for j,key in enumerate(inventory['nodes'][node['id']]['foundationalKeys'])}
        record['confidence']['temporarily-unmatched-question']={'rating':'easy','ratedAt':'2026-11-17T05:00:00.000Z'}
        old['topics'][node['id']]=record
    old['topics']['archived-topic']=copy.deepcopy(example['state']['topics']['archived-topic'])
    expected_ratings={}
    for base in [args.base_url,args.project_url]:
        context=await browser.new_context(viewport={'width':1440,'height':1000})
        await context.add_init_script('if(!localStorage.getItem("backend-lab.learning.v1"))localStorage.setItem("backend-lab.learning.v1",'+json.dumps(json.dumps(old))+')')
        page=await context.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        await page.goto(base);await ready(page)
        expected=str(int(sum(old['topics'][n['id']]['status']=='mastered' for n in topics)/len(topics)*100+.5))+'%'
        assert await page.locator('#mastery-value').inner_text()==expected
        assert await page.locator('#global-percent').inner_text()==expected
        for node in topics:
            own=inventory['nodes'][node['id']];await page.goto(base+'#'+node['route']);await ready(page,True)
            assert await page.locator('article').get_attribute('data-enhancement')=='complete'
            current=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')
            assert not set(own['interviewKeys']) & set(current['topics'][node['id']]['confidence'])
            cards=page.locator('[data-interview-scenarios] > details.kb-question')
            assert await cards.count()==len(own['interviewKeys'])
            assert await cards.evaluate_all('(els)=>els.every(e=>!e.open&&!e.hasAttribute("name"))')
            # A real keyboard sequence proves two answers can remain open independently.
            await cards.nth(0).locator('summary').focus();await page.keyboard.press('Enter')
            await cards.nth(1).locator('summary').focus();await page.keyboard.press('Space')
            assert await cards.nth(0).evaluate('(e)=>e.open') and await cards.nth(1).evaluate('(e)=>e.open')
            await cards.nth(0).locator('summary').focus();await page.keyboard.press('Enter')
            assert not await cards.nth(0).evaluate('(e)=>e.open') and await cards.nth(1).evaluate('(e)=>e.open')
            expected_ratings[node['id']]={}
            for j,key in enumerate(own['interviewKeys']):
                card=page.locator('details[data-recall-id="'+key+'"]')
                assert await card.locator('[data-host-confidence]').count()==1
                assert await card.locator('[aria-pressed=true]').count()==0
                if not await card.evaluate('(e)=>e.open'):await card.locator('summary').click()
                rating=['hard','good','easy'][j%3]
                # Update twice to prove latest-rating semantics, not a write-once value.
                await card.get_by_role('button',name='Hard',exact=True).click()
                button=card.get_by_role('button',name=rating.title(),exact=True)
                await button.focus();await page.keyboard.press('Space')
                assert await button.get_attribute('aria-pressed')=='true'
                expected_ratings[node['id']][key]=rating
            state=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')
            learning_invariants(state,old,inventory['nodes'],rated=True)
            assert await page.locator('#global-percent').inner_text()=='33%'
            await page.reload();await ready(page,True)
            await page.goto(base+'#/system-design/backend-architecture');await ready(page,True)
            await page.goto(base+'#'+node['route']);await ready(page,True)
            for key,rating in expected_ratings[node['id']].items():
                assert await page.locator('details[data-recall-id="'+key+'"] [data-confidence="'+rating+'"]').get_attribute('aria-pressed')=='true'
            proof.setdefault(node['id'],{'topicId':node['id'],'path':own['path'],'sourceSha256':own['sourceSha256'],'status':'pass','bases':[]})['bases'].append({'base':base,'newKeys':own['interviewKeys'],'ratings':expected_ratings[node['id']],'initiallyUnrated':True,'independentKeyboardDisclosure':True,'reloadAndRevisit':True,'originalStatusReviewAndConfidence':'unchanged'})
        async with page.expect_download() as dl:await page.locator('#export-progress').click()
        expanded=json.loads(Path(await (await dl.value).path()).read_text())
        learning_invariants(expanded['state'],old,inventory['nodes'],rated=True)
        for identity,values in expected_ratings.items():
            for key,rating in values.items():assert expanded['state']['topics'][identity]['confidence'][key]['rating']==rating
        older={**example,'state':copy.deepcopy(old)}
        await import_payload(page,older)
        restored=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')
        assert restored==old
        learning_invariants(restored,old,inventory['nodes'])
        # Confirmed replacement retains the old backup's actual values, including unknown keys.
        await import_payload(page,expanded)
        assert await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')==expanded['state']
        await page.reload();await ready(page,True)
        for node in topics:
            await page.goto(base+'#'+node['route']);await ready(page,True)
            for key,rating in expected_ratings[node['id']].items():
                assert await page.locator('details[data-recall-id="'+key+'"] [data-confidence="'+rating+'"]').get_attribute('aria-pressed')=='true'
            proof[node['id']]['bases'][-1].update(oldBackupReplacement=True,newBackupRestoration=True,unknownKeysPreserved=True)
        final=await page.evaluate('JSON.parse(localStorage.getItem("backend-lab.learning.v1"))')
        learning_invariants(final,old,inventory['nodes'],rated=True)
        assert not errors,errors
        await context.close()
    return {'status':'pass','lessons':list(proof.values()),'foundational':inventory['foundational'],'interviews':inventory['interviews'],'masteryDenominator':len(topics),'seededStatuses':['not-started','in-progress','mastered'],'backupVersion':1}


@scenario('EXPANDED')
async def expanded_host(browser,args,root):
    return await check_expanded_host(browser,args,root)


async def check_expanded_host(browser,args,root):
    inventory=current_inventory(root);topics=[n for n in catalog(root) if n['kind']=='topic'];proof={}
    for base in [args.base_url,args.project_url]:
        for theme in ['light','dark']:
            context=await browser.new_context(viewport={'width':360,'height':800},color_scheme=theme)
            page=await context.new_page();errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            await page.goto(base);await ready(page)
            if await page.locator('html').get_attribute('data-theme')!=theme:await page.locator('#theme-toggle').click()
            for node in topics:
                own=inventory['nodes'][node['id']]
                await page.goto(base+'#'+node['route']);await ready(page,True)
                assert await page.locator('article').get_attribute('data-enhancement')=='complete'
                assert await page.locator('html').get_attribute('data-theme')==theme
                assert await page.locator('[data-interview-scenarios] > h3').inner_text()=='Tricky & Most-Asked Interview Scenarios'
                assert await page.locator('[data-interview-research]').is_visible()
                assert await page.locator('pre.mermaid svg').count()==own['diagrams']
                assert await page.locator('[data-host-confidence]').count()==len(own['foundationalKeys'])+len(own['interviewKeys'])
                for key in own['interviewKeys']:
                    card=page.locator('details[data-recall-id="'+key+'"]');summary=card.locator(':scope > summary')
                    assert not await card.evaluate('(e)=>e.open')
                    assert (await summary.inner_text()).strip()
                    await summary.focus();assert await summary.evaluate('(e)=>e===document.activeElement')
                    await page.keyboard.press('Enter');assert await card.evaluate('(e)=>e.open')
                    assert await card.locator(':scope > [data-scenario-part]').count()==3
                    assert await card.locator('[data-host-confidence]').count()==1
                    for rating in ['Hard','Good','Easy']:
                        assert await card.get_by_role('button',name=rating,exact=True).count()==1
                    button=card.get_by_role('button',name='Good',exact=True)
                    await button.focus();await page.keyboard.press('Space');assert await button.get_attribute('aria-pressed')=='true'
                    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(node['slug'],theme,key)
                    assert await card.locator('pre.mermaid svg').evaluate_all('(els)=>els.every(e=>{const v=e.viewBox.baseVal;return v.width>0&&v.height>0})')
                    await summary.click();assert not await card.evaluate('(e)=>e.open')
                # Re-render both themes with mixed disclosure state, preserving all controls and identities.
                await page.locator('[data-interview-scenarios] > details').nth(0).locator('summary').click()
                before=await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')
                await page.locator('#theme-toggle').click();await ready(page,True)
                assert await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')==before
                assert await page.locator('pre.mermaid svg').count()==own['diagrams']
                assert await page.locator('[data-host-confidence]').count()==len(own['foundationalKeys'])+len(own['interviewKeys'])
                await page.locator('#theme-toggle').click();await ready(page,True)
                assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                proof.setdefault(node['id'],{'topicId':node['id'],'path':own['path'],'sourceSha256':own['sourceSha256'],'status':'pass','cases':[]})['cases'].append({'base':base,'theme':theme,'viewport':360,'newKeys':own['interviewKeys'],'renderedDiagrams':own['diagrams'],'keyboardAndPointer':'pass','sourceNoteVisible':True,'pageOverflow':False,'themeRerenderPreservesDetails':True,'duplicateControls':False})
            assert not errors,errors
            print('Expanded mobile/theme complete:',base,theme,flush=True)
            await context.close()
    return {'status':'pass','lessons':list(proof.values()),'consoleErrors':[]}


@scenario('EXPANDED')
async def reading_fixture(browser,args,root):
    context=await browser.new_context();page=await context.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(args.project_url+'tests/fixtures/content-host.html')
    await page.wait_for_function('window.contentFixture && document.querySelector("#canvas[aria-busy=false] article")')
    result=await page.evaluate('window.contentFixture.checkAll()')
    assert result['result']=='pass',result
    assert len(result['checks'])==len(catalog(root))
    assert sum(c.get('recall',{}).get('interviews',0) for c in result['checks'])==current_inventory(root)['interviews']
    assert await page.evaluate('localStorage.length')==0
    assert not errors,errors
    await context.close();return {'status':'pass','report':result,'learningWrites':0,'errors':errors}

@scenario('US6')
async def print_articles(browser,args,root):
    if not args.pdf_dir:raise AssertionError('Required actual-PDF gate not executed: supply --pdf-dir')
    out=Path(args.pdf_dir);out.mkdir(parents=True,exist_ok=True);nodes=catalog(root);checks=[]
    if getattr(args,'node_ids',None) is not None:
        nodes=[n for n in nodes if n['id'] in args.node_ids]
    inventory=current_inventory(root)
    context=await browser.new_context(viewport={'width':1440,'height':1100});page=await context.new_page();await page.goto(args.base_url);await ready(page)
    for theme in ['light','dark']:
        if await page.locator('html').get_attribute('data-theme')!=theme:await page.locator('#theme-toggle').click()
        for node in nodes:
            await page.evaluate('(hash)=>location.hash=hash','#'+node['route'])
            await page.wait_for_function('(id)=>document.querySelector("article")?.dataset.nodeId===id',arg=node['id']);await ready(page,True)
            assert await page.locator('article').get_attribute('data-enhancement')=='complete'
            assert await page.locator('pre.mermaid svg').count()==inventory['nodes'][node['id']]['diagrams']
            await page.locator('article details').evaluate_all('(els)=>els.forEach((e,i)=>e.open=i%3===0)')
            states=await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')
            diagram_text=await page.locator('pre.mermaid svg text,pre.mermaid svg foreignObject').all_text_contents()
            await page.emulate_media(media='print')
            assert await page.locator('[data-host-confidence],[data-host-controls]').evaluate_all('(els)=>els.every(e=>getComputedStyle(e).display==="none")')
            assert await page.locator('.kb-diagram svg').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().height<=230*96/25.4+1)')
            # Release the override: forcing screen here makes page.pdf print navigation.
            await page.emulate_media(media='null')
            filename=out/(theme+'-'+node['id']+'.pdf');await page.pdf(path=str(filename),format='A4',print_background=True)
            assert await page.locator('article details').evaluate_all('(els)=>els.map(e=>e.open)')==states
            source=root/('topics'+node['route']+('/_overview.html' if node['kind']=='hub' else '.html'))
            expected=source_print_texts(source.read_text());text=subprocess.check_output(['pdftotext','-layout',str(filename),'-'],text=True)
            raw_text=subprocess.check_output(['pdftotext','-raw',str(filename),'-'],text=True)
            # Layout extraction interleaves wrapped table columns; raw order preserves cells.
            streams=[normalized(text),normalized(raw_text)]
            missing=[p for p in expected if normalized(p) and not any(normalized(p) in full for full in streams)]
            assert not missing,(node['slug'],theme,missing[:2])
            missing_labels=[label for label in diagram_text if normalized(label) and not any(normalized(label) in full for full in streams)]
            assert not missing_labels,(node['slug'],theme,'missing diagram labels',missing_labels[:3])
            if node['kind']=='topic':
                from tools import validate_content as vc
                for label in vc.ANSWER_PARTS.values():
                    assert max(full.count(normalized(label)) for full in streams)>=len(inventory['nodes'][node['id']]['interviewKeys'])
            assert 'How did that feel?' not in text
            assert 'Mark as Mastered' not in text
            checks.append({'nodeId':node['id'],'topicId':node['id'],'sourceSha256':inventory['nodes'][node['id']]['sourceSha256'],'kind':node['kind'],'theme':theme,'pdf':str(filename),'completeTextBlocks':len(expected),'diagramLabels':len(diagram_text),'diagrams':inventory['nodes'][node['id']]['diagrams'],'disclosuresRestored':True,'mixedDisclosureStates':True,'controlsHidden':True,'status':'pass'})
            print('PDF complete:',theme,node['slug'],flush=True)
        print('PDF theme complete:',theme,flush=True)
    await context.close();return {'pdfs':len(checks),'checks':checks}

async def run(args):
    root = Path(__file__).resolve().parents[2]
    report = {'result':'pass', 'platform':platform.platform(), 'referenceDevice':'WSL2 local headless Chromium, 1440px desktop / 360px mobile', 'dependencies':{'mermaid':'12.3.0','highlight':'11.11.1','tailwind':'3.4.17','playwright':'1.56.0'}, 'checks':[], 'bases':[args.base_url,args.project_url]}
    protected=json.loads((root/'specs/003-backfill-interview-scenarios/contracts/preservation-baseline.json').read_text())
    report['runtimeFileHashes']={path:hashlib.sha256((root/path).read_bytes()).hexdigest() for path in protected['runtimeFiles']}
    report['motionHandling']='Browser contexts request reduced motion and disable animated document scrolling only; DOM, controls, layout, diagrams and print use the real app.'
    inventory=current_inventory(root)
    report['inputFingerprint']=hashlib.sha256(json.dumps({'runtime':report['runtimeFileHashes'],'content':inventory['nodes'],'harness':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},sort_keys=True).encode()).hexdigest()
    report['executionStatus']='running'
    report['result']='pending'
    def save_checkpoint():
        target=Path(args.report);target.parent.mkdir(parents=True,exist_ok=True)
        temporary=target.with_suffix(target.suffix+'.tmp')
        temporary.write_text(json.dumps(report,indent=2)+'\n');temporary.replace(target)
    save_checkpoint()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        create_context=browser.new_context
        async def test_context(**options):
            options.setdefault('reduced_motion','reduce')
            context=await create_context(**options)
            await context.add_init_script('document.addEventListener("DOMContentLoaded",()=>{document.documentElement.style.scrollBehavior="auto";},{once:true})')
            return context
        browser.new_context=test_context
        report['browser'] = browser.version
        for story in ([args.story] if args.story else [*[f'US{i}' for i in range(1,7)],'MIGRATION','EXPANDED']):
            functions = SCENARIOS.get(story, [])
            if not functions:
                report['checks'].append({'story':story,'result':'unexecuted','reason':'No executable scenarios registered'})
                report['result']='fail'
            for fn in functions:
                start=time.monotonic()
                try:
                    detail=await fn(browser,args,root)
                    report['checks'].append({'story':story,'scenario':fn.__name__,'result':'pass','seconds':round(time.monotonic()-start,2),'details':detail})
                except Exception as exc:
                    report['result']='fail'
                    report['checks'].append({'story':story,'scenario':fn.__name__,'result':'fail','reason':str(exc),'seconds':round(time.monotonic()-start,2)})
                print(story, fn.__name__, report['checks'][-1]['result'],flush=True)
                save_checkpoint()
        await browser.close()
    report['executionStatus']='complete'
    report['result']='pass' if report['checks'] and all(c['result']=='pass' for c in report['checks']) else 'fail'
    save_checkpoint()
    return 0 if report['result']=='pass' else 1

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',required=True)
    parser.add_argument('--project-url',required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--pdf-dir')
    parser.add_argument('--story',choices=[*[f'US{i}' for i in range(1,7)],'MIGRATION','EXPANDED'])
    raise SystemExit(asyncio.run(run(parser.parse_args())))
