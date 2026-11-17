// Test-only content host. It deliberately owns no persistent learning state.
const appBase = new URL('../../', import.meta.url);
const canvas = document.querySelector('#canvas');
const status = document.querySelector('#status');
const selector = document.querySelector('#route');
const sectionKeys = ['hook-eli5','big-picture','mechanics','trade-offs','pitfalls','mastery'];
const versions = {mermaid:'12.3.0', highlight:'11.11.1'};
let index = new Map(), current = '', mountSerial = 0, mermaid, libraryPromise;
let printSnapshot = null, printPreparations = 0, printRestorations = 0;
function message(text, error=false) { status.textContent=text;status.dataset.error=String(error); }
async function libraries() {
  if (!libraryPromise) libraryPromise=(async()=>{
    mermaid=(await import('https://cdn.jsdelivr.net/npm/mermaid@12.3.0/dist/mermaid.esm.min.mjs')).default;
    if (!window.hljs) throw new Error('Pinned Highlight.js asset failed to load');
    versions.highlight=window.hljs.versionString;
  })();
  return libraryPromise;
}
function catalogIndex(data) {
  if (data.schemaVersion!==1 || !Array.isArray(data.roots)) throw new Error('Unsupported catalog');
  const ids=new Set();
  function walk(nodes, chain=[]) {
    for(const node of nodes) {
      if(!node.id||ids.has(node.id)||!['hub','topic'].includes(node.kind)||typeof node.slug!=='string'||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(node.slug)||/\s/.test(node.slug)) throw new Error('Invalid or duplicate manifest node');
      ids.add(node.id);const ancestry=[...chain,node],route='/'+ancestry.map(n=>n.slug).join('/');
      if(index.has(route)) throw new Error('Duplicate content route');
      index.set(route,{node,ancestry,path:'topics'+route+(node.kind==='hub'?'/_overview.html':'.html')});
      if(node.kind==='hub')walk(node.children,ancestry);
    }
  }
  walk(data.roots);
}
function routeInfo(input) {
  if(typeof input!=='string'||!input.startsWith('/')||input.startsWith('//'))throw new Error('Invalid content route');
  const parsed=new URL(input,'https://content.invalid');
  if(!index.has(parsed.pathname))throw new Error('Unknown content route: '+parsed.pathname);
  const entries=[...parsed.searchParams.entries()];
  if(entries.length>1||entries.some(([k,v])=>k!=='section'||!sectionKeys.includes(v)))throw new Error('Unknown section query');
  const section=parsed.searchParams.get('section');
  if(section&&index.get(parsed.pathname).node.kind!=='topic')throw new Error('Hubs have no lesson section keys');
  return {route:parsed.pathname,section,item:index.get(parsed.pathname)};
}
async function mount(input) {
  const serial=++mountSerial;
  canvas.setAttribute('aria-busy','true');
  try {
    const info=routeInfo(input);message('Loading '+info.item.node.title+'…');
    const response=await fetch(new URL(info.item.path,appBase));
    if(!response.ok)throw new Error(`${response.status} loading ${info.item.path}`);
    const source=await response.text();
    const doc=new DOMParser().parseFromString(source,'text/html');
    const article=doc.body.firstElementChild;
    if(doc.body.children.length!==1||article?.tagName!=='ARTICLE'||article.dataset.nodeId!==info.item.node.id)throw new Error('Article envelope/identity mismatch');
    const diagrams=[...article.querySelectorAll('pre.mermaid')];
    if(!diagrams.length)throw new Error('Required diagram missing');
    const originals=diagrams.map(el=>el.textContent);
    await libraries();
    if(serial!==mountSerial)return null;
    canvas.replaceChildren(article);current=input;
    mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:document.documentElement.dataset.theme==='dark'?'dark':'default',htmlLabels:false});
    await mermaid.run({nodes:diagrams});
    if(serial!==mountSerial)return null;
    if(diagrams.some(el=>!el.querySelector('svg')))throw new Error('Diagram did not render to SVG');
    for(const code of article.querySelectorAll('pre:not(.mermaid) > code')) window.hljs.highlightElement(code);
    selector.value=info.route;
    document.querySelector('#location').textContent=info.item.ancestry.map(n=>n.title).join(' → ');
    document.title=info.item.node.title+' · Content Reading Fixture';
    canvas.dataset.diagramSources=JSON.stringify(originals);
    message(`${info.item.node.title} · ${diagrams.length} diagram(s) rendered · host learning controls pending`);
    if(info.section) {
      const target=article.querySelector(`[data-section="${info.section}"]`);
      if(!target)throw new Error('Section missing from lesson');
      target.scrollIntoView({behavior:'smooth'});
    }
    return {route:info.route,nodeId:info.item.node.id,kind:info.item.node.kind,diagrams:diagrams.length};
  } catch(error) {message(error.message,true);throw error;}
  finally {if(serial===mountSerial)canvas.setAttribute('aria-busy','false');}
}
function checkRecall(article) {
  const questions=[...article.querySelectorAll('details.kb-question')];
  const foundational=questions.filter(q=>!q.dataset.recallKind||q.dataset.recallKind==='foundational');
  const interviews=questions.filter(q=>q.dataset.recallKind==='interview');
  const groups=article.querySelectorAll('[data-interview-scenarios]');
  if(foundational.length<3||foundational.length>5)throw new Error('Expected 3-5 foundational questions');
  if(interviews.length<5||interviews.length>7||groups.length!==1)throw new Error('Expected one 5-7-card interview group');
  if(foundational.length+interviews.length!==questions.length)throw new Error('Unknown question role');
  if(interviews.some(q=>q.parentElement!==groups[0]||!q.dataset.recallId?.startsWith('interview-')))throw new Error('Interview role or identity mismatch');
  const partKeys=['scenario','decision','trade-offs'];
  for(const question of interviews){
    const parts=[...question.querySelectorAll(':scope > [data-scenario-part]')];
    if(parts.length!==3||parts.some((p,i)=>p.dataset.scenarioPart!==partKeys[i]||p.querySelectorAll('p').length<2))throw new Error('Incomplete interview answer');
  }
  const keys=questions.map(q=>q.dataset.recallId);
  if(new Set(keys).size!==keys.length||keys.some(k=>!k))throw new Error('Recall keys are not unique/stable');
  if(questions.some(q=>q.open||q.hasAttribute('name')))throw new Error('Recall answers must start closed and ungrouped');
  const identity=article.dataset.nodeId;
  try {
    questions[0].open=true;questions[1].open=true;
    if(!questions[0].open||!questions[1].open)throw new Error('Recall answers are not independent');
    questions[0].open=false;
    if(!questions[1].open)throw new Error('Closing one answer closed another');
    if(article.dataset.nodeId!==identity||questions.some((q,i)=>q.dataset.recallId!==keys[i]))throw new Error('Opening answers changed identity');
  } finally {for(const q of questions)q.open=false;}
  return {questions:questions.length,foundational:foundational.length,interviews:interviews.length,initiallyClosed:true,independent:true,topicId:identity,recallKeys:keys};
}

async function checkAll() {
  const previous=current;
  const report={phase:'browser-fixture',result:'pass',totalNodes:index.size,versions:{...versions},browser:navigator.userAgent,checks:[],integrationStatus:'pending'};
  document.querySelector('#check-all').disabled=true;
  for(const route of index.keys()) {
    try {const result=await mount(route);if(!result)throw new Error('Mount was superseded');if(result.kind==='topic')result.recall=checkRecall(canvas.firstElementChild);report.checks.push({...result,status:'pass'});}
    catch(error){report.result='fail';report.checks.push({route,status:'fail',message:error.message});}
  }
  if(previous) {try {await mount(previous);}catch(error){report.result='fail';}}
  report.versions={...versions};
  window.contentFixture.lastReport=report;
  document.querySelector('#report').textContent=JSON.stringify(report,null,2);
  document.querySelector('#check-all').disabled=false;
  message(`Batch ${report.result}: ${report.checks.filter(c=>c.status==='pass').length}/${report.totalNodes} partials`,report.result!=='pass');
  return report;
}
function preparePrint() {
  if(printSnapshot)return;
  printSnapshot=[...canvas.querySelectorAll('details')].map(el=>[el,el.open]);
  for(const [el]of printSnapshot)el.open=true;
  printPreparations++;
}
function restorePrint() {
  if(!printSnapshot)return;
  for(const[el,open]of printSnapshot)el.open=open;
  printSnapshot=null;printRestorations++;
}
window.addEventListener('beforeprint',preparePrint);
window.addEventListener('afterprint',restorePrint);
window.addEventListener('hashchange',()=>mount(location.hash.slice(1)).catch(()=>{}));
selector.addEventListener('change',()=>{location.hash='#'+selector.value;});
canvas.addEventListener('click',event=>{
  const link=event.target.closest('a');
  if(!link||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  const href=link.getAttribute('href');
  if(href?.startsWith('#/')){event.preventDefault();if(location.hash===href)mount(href.slice(1)).catch(()=>{});else location.hash=href;}
});
document.querySelector('#theme').addEventListener('click',async()=>{
  const states=[...canvas.querySelectorAll('details')].map(el=>el.open);
  const next=document.documentElement.dataset.theme==='dark'?'light':'dark';
  document.documentElement.dataset.theme=next;
  document.querySelector('#theme').textContent=next==='dark'?'Use light theme':'Use dark theme';
  if(current){try{await mount(current);[...canvas.querySelectorAll('details')].forEach((el,i)=>el.open=states[i]??el.open);}catch{}}
});
document.querySelector('#print').addEventListener('click',()=>window.print());
document.querySelector('#check-all').addEventListener('click',()=>checkAll().catch(error=>message(error.message,true)));
window.contentFixture={mount,checkAll,checkRecall,get printLifecycle(){return {preparations:printPreparations,restorations:printRestorations,active:!!printSnapshot};}};
try {
  const response=await fetch(new URL('manifest.json',appBase));
  if(!response.ok)throw new Error('Could not load manifest: '+response.status);
  catalogIndex(await response.json());
  for(const[route,item]of index){const option=document.createElement('option');option.value=route;option.textContent=item.ancestry.map(n=>n.title).join(' › ');selector.append(option);}
  await mount(location.hash.slice(1)||index.keys().next().value);
} catch(error) {message(error.message,true);canvas.setAttribute('aria-busy','false');}
