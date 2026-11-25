import {indexCatalog,parseHash,searchCatalog} from './assets/js/catalog.js';
import {createStore,progress,topicRecord,reviewQueue,continueLearning,markStatus,rateQuestion,startReview,completeReview,scheduledReviews,exportBackup,parseBackup,setTheme} from './assets/js/learning-state.js';
import {loadArticle,enhanceArticle} from './assets/js/content-renderer.js';

const appBase=new URL('./',import.meta.url);
const $=selector=>document.querySelector(selector);
const main=$('#main-content'),status=$('#route-status');
const labelStatus={'not-started':'Not Started','in-progress':'In Progress',mastered:'Mastered'};
const symbolStatus={'not-started':'○','in-progress':'◔',mastered:'✓'};
let catalog,current=null,routeSerial=0,controller,themeSerial=0,dueTimer;
let searchResults=[],searchIndex=0,pendingImport=null;
const dialogOpeners=new WeakMap();
const expanded=new Set(),navLinks=new Map(),badges=new Map(),branches=new Map();
function h(tag,attributes={},...children){
  const node=document.createElement(tag);
  for(const [key,value] of Object.entries(attributes)){if(value!==null&&value!==false)node.setAttribute(key,value===true?'':String(value));}
  node.append(...children.flat(Infinity).filter(v=>v!==null&&v!==undefined));return node;
}
function heading(text){return h('h1',{tabindex:'-1'},text);}
function focusHeading(target=main.querySelector('h1')){if(target){target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}}
function action(text,name,attrs={}){return h('button',{class:'quiet-button',type:'button','data-action':name,...attrs},text);}
function closeDialogs(navigating=false){for(const dialog of document.querySelectorAll('dialog[open]'))dialog.close(navigating?'navigate':'cancel');}
function openModal(dialog,focusTarget){
  if(!dialog.open){closeDialogs();dialogOpeners.set(dialog,document.activeElement);dialog.returnValue='';dialog.showModal();}
  (focusTarget||dialog.querySelector('input,button'))?.focus();
}
for(const dialog of document.querySelectorAll('dialog')){
  dialog.addEventListener('close',()=>{if(dialog.id==='search-dialog'&&!dialog.open)$('#search-input').setAttribute('aria-expanded','false');if(dialog.id==='import-dialog'&&!dialog.open)pendingImport=null;const opener=dialogOpeners.get(dialog);if(dialog.returnValue!=='navigate'&&!dialog.open&&opener?.isConnected)opener.focus();});
  dialog.addEventListener('click',event=>{const r=dialog.getBoundingClientRect();if(event.target===dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))dialog.close('cancel');});
}
function renderSearch(){
  if(!catalog)return;searchResults=searchCatalog(catalog,$('#search-input').value);searchIndex=0;
  const results=searchResults.map((entry,i)=>h('li',{id:'search-result-'+i,role:'option','aria-selected':String(i===0)},h('a',{href:entry.href,tabindex:'-1'},h('span',{},h('strong',{},entry.title),h('small',{},pathLabel(entry))),h('span',{class:'search-kind'},entry.kind==='hub'?'Overview':'Lesson'))));
  $('#search-results').setAttribute('role','listbox');$('#search-results').replaceChildren(...results);$('#search-count').textContent=results.length?`${results.length} idea${results.length===1?'':'s'} to explore`:'No concepts found. Try a different word.';updateSearchSelection();
}
function updateSearchSelection(){
  const input=$('#search-input');input.setAttribute('role','combobox');input.setAttribute('aria-autocomplete','list');input.setAttribute('aria-expanded','true');
  for(const [i,li] of [...$('#search-results').children].entries())li.setAttribute('aria-selected',String(i===searchIndex));
  if(searchResults.length){input.setAttribute('aria-activedescendant','search-result-'+searchIndex);$('#search-results').children[searchIndex]?.scrollIntoView({block:'nearest',behavior:'instant'});}else input.removeAttribute('aria-activedescendant');
}
function openSearch(){if(!catalog)return;renderSearch();openModal($('#search-dialog'),$('#search-input'));}
let storage;
try{storage=window.localStorage;}catch{storage={getItem(){throw Error('Storage blocked');},setItem(){throw Error('Storage blocked');}};}
const store=createStore(storage);
const deviceTheme=matchMedia('(prefers-color-scheme: dark)');
function applyTheme(){
  const value=store.state.preferences.theme||(deviceTheme.matches?'dark':'light'),changed=document.documentElement.dataset.theme!==value;
  document.documentElement.dataset.theme=value;const label=value==='dark'?'Switch to light theme':'Switch to dark theme';$('#theme-toggle').setAttribute('aria-label',label);$('#theme-toggle').title=label;
  if(changed&&current&&main.querySelector('article'))void enhanceCurrent(main.querySelector('article'),current.entry);
}
deviceTheme.addEventListener('change',()=>{if(store.state.preferences.theme===null)applyTheme();});
const desktopMedia=matchMedia('(min-width: 64rem)');
function syncSidebar(){
  const sidebar=$('#sidebar'),dialog=$('#drawer-dialog');
  if(desktopMedia.matches){if(dialog.open)dialog.close('cancel');$('#desktop-sidebar').append(sidebar);}
  else $('#mobile-sidebar').append(sidebar);
}
desktopMedia.addEventListener('change',syncSidebar);
$('#drawer-open').addEventListener('click',()=>openModal($('#drawer-dialog'),$('#sidebar a')));
$('#theme-toggle').addEventListener('click',()=>store.update(s=>setTheme(s,document.documentElement.dataset.theme==='dark'?'light':'dark',new Date().toISOString())));
$('#export-progress').addEventListener('click',()=>{
  const backup=exportBackup(store.state),blob=new Blob([JSON.stringify(backup,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob);
  const link=h('a',{href:url,download:'backend-lab-progress-'+backup.exportedAt.slice(0,10)+'.json'});document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='Your complete learning backup has been exported.';
});
$('#import-progress').addEventListener('click',()=>$('#import-file').click());
let importSerial=0;
$('#import-file').addEventListener('change',async event=>{
  const file=event.target.files[0];if(!file)return;const serial=++importSerial;
  pendingImport=null;$('#confirm-import').disabled=true;$('#import-error').textContent='';
  try{
    const text=await file.text();if(serial!==importSerial)return;const candidate=parseBackup(text),ids=Object.keys(candidate.topics),matched=ids.filter(id=>catalog?.byId.get(id)?.kind==='topic').length;
    $('#import-summary').replaceChildren(h('p',{},`${matched} current topic record${matched===1?'':'s'} · ${ids.length-matched} unmatched record${ids.length-matched===1?'':'s'}.`),h('p',{class:'muted'},'This replaces your saved learning record and theme. Unmatched topics and questions stay in the backup for when they return to your library.'),h('p',{class:'muted'},'Saved workspace: '+dateLabel(candidate.updatedAt)));
    openModal($('#import-dialog'),$('#confirm-import'));pendingImport=candidate;$('#confirm-import').disabled=false;
  }catch(error){$('#import-summary').replaceChildren(h('p',{},'Your current learning record has not changed.'));$('#import-error').textContent=error.message;openModal($('#import-dialog'));}
  finally{event.target.value='';}
});
$('#confirm-import').addEventListener('click',()=>{
  if(!pendingImport)return;
  try{store.replace(pendingImport);$('#import-dialog').close('restored');status.textContent='Your learning backup has been restored.';}
  catch(error){$('#import-error').textContent='Restore failed; your existing record is unchanged. '+error.message;}
});
function persistence(){const notice=$('#persistence-notice');notice.hidden=!store.warning;notice.textContent=store.warning;}
function updateBadges(){
  if(!catalog)return;
  for(const entry of catalog.entries){
    const badge=badges.get(entry.id);if(!badge)continue;
    if(entry.kind==='topic'){
      const value=topicRecord(store.state,entry.id).status;badge.textContent=symbolStatus[value];badge.setAttribute('aria-label',labelStatus[value]);badge.title=labelStatus[value];
    }else{const p=progress(catalog,store.state,entry.topicIds);badge.textContent=`${p.mastered}/${p.total}`;badge.setAttribute('aria-label',`${p.percent}% mastered, ${p.mastered} of ${p.total} lessons`);}
  }
}
function renderSidebar(){
  navLinks.clear();badges.clear();branches.clear();
  function list(entries,depth=0){
    const ul=h('ul',{class:'nav-list'});
    for(const entry of entries){
      const row=h('div',{class:'nav-row'}),li=h('li',{},row),badge=h('span',{class:'nav-badge'});
      const link=h('a',{class:'nav-link',href:entry.href},h('span',{},entry.title),badge);navLinks.set(entry.id,link);badges.set(entry.id,badge);
      if(entry.kind==='hub'){
        const childList=list(entry.children,depth+1),id='branch-'+entry.index;
        childList.id=id;childList.hidden=!expanded.has(entry.id);
        const button=action(expanded.has(entry.id)?'⌄':'›','toggle-branch',{class:'branch-toggle','aria-label':`${expanded.has(entry.id)?'Collapse':'Expand'} ${entry.title}`,'aria-expanded':String(expanded.has(entry.id)),'aria-controls':id,'data-id':entry.id});
        row.append(button,link);li.append(childList);branches.set(entry.id,{list:childList,button});
      }else row.append(h('span',{class:'nav-topic-symbol','aria-hidden':'true'},'·'),link);
      ul.append(li);
    }
    return ul;
  }
  $('#library-nav').replaceChildren(list(catalog.roots));updateBadges();
}
function activeNavigation(entry){
  for(const link of navLinks.values())link.removeAttribute('aria-current');
  if(entry){navLinks.get(entry.id)?.setAttribute('aria-current','page');for(const node of entry.ancestry){const branch=branches.get(node.id);if(branch){expanded.add(node.id);branch.list.hidden=false;branch.button.textContent='⌄';branch.button.setAttribute('aria-expanded','true');branch.button.setAttribute('aria-label','Collapse '+node.title);}}}
}
function breadcrumbs(entry=null,error=false){
  const nodes=[h('a',{href:'#/'},'Dashboard')];
  if(entry)entry.ancestry.forEach((node,i)=>{const parent=catalog.byId.get(node.id);nodes.push(h('span',{class:'crumb-separator','aria-hidden':'true'},'/'),i===entry.ancestry.length-1?h('span',{'aria-current':'page'},node.title):h('a',{href:parent.href},node.title));});
  if(error)nodes.push(h('span',{},'/ Link unavailable'));
  $('#breadcrumbs').replaceChildren(...nodes);
}
function pathLabel(entry){return entry.ancestry.slice(0,-1).map(n=>n.title).join(' / ');}
function dateLabel(value){return new Intl.DateTimeFormat(undefined,{month:'short',day:'numeric',year:'numeric'}).format(new Date(value));}
function renderHome(){
  const p=progress(catalog,store.state),due=reviewQueue(catalog,store.state),next=continueLearning(catalog,store.state);
  const inProgress=catalog.topics.filter(e=>topicRecord(store.state,e.id).status==='in-progress').length;
  const ring=h('div',{class:'mastery-ring','aria-label':`${p.percent}% mastered`},h('div',{},h('strong',{id:'mastery-value'},p.percent+'%'),h('span',{},'MASTERED')));ring.style.setProperty('--mastery',p.percent+'%');
  const hero=h('section',{class:'dashboard-hero'},h('div',{},h('p',{class:'eyebrow'},'YOUR PERSONAL LEARNING SPACE'),heading('Keep your curiosity moving.'),h('p',{class:'hero-description'},'Connect the ideas. Understand the why. Build knowledge that stays with you.'),h('p',{class:'hero-footnote'},'One clear concept at a time.')),
    h('div',{class:'mastery-card'},ring,h('div',{},h('p',{class:'eyebrow'},'THE BIG PICTURE'),h('h2',{},p.total&&p.mastered===p.total?'A foundation worth revisiting.':'Small steps. Lasting understanding.'),h('p',{class:'muted'},`${p.mastered} of ${p.total} concepts mastered. Every connection counts.`))));
  const stats=h('div',{class:'stats-grid'},...[[p.mastered,'Concepts mastered','✓'],[inProgress,'In progress','◔'],[due.length,'Ready for a refresh','↻']].map(([value,label,icon])=>h('div',{class:'stat-card surface'},h('span',{class:'stat-icon','aria-hidden':'true'},icon),h('div',{},h('strong',{},String(value)),h('span',{},label)))));
  const resume=h('section',{class:'continue-card surface'},h('div',{class:'card-heading'},h('span',{class:'eyebrow'},'YOUR NEXT CONNECTION'),h('span',{'aria-hidden':'true'},'↗')),h('h2',{},next?(next.kind==='continue'?'Right where you left off.':next.kind==='start'?'A good place to begin.':next.kind==='due'?'Keep that knowledge fresh.':'You’ve explored the whole library.'):'Your library is ready to grow.'));
  if(next)resume.append(h('p',{class:'muted topic-path'},pathLabel(next.entry)),h('h3',{},next.entry.title),h('p',{class:'muted'},next.kind==='scheduled'?`Next review: ${dateLabel(next.dueAt)}.`:'Start with an intuitive idea. Leave with a deeper understanding.'),h('a',{class:'primary-button',id:'continue-learning',href:next.entry.href},next.kind==='continue'?'Continue learning →':next.kind==='start'?'Start learning →':'Revisit concept →'));
  else resume.append(h('p',{class:'muted'},'Add a topic to your manifest and its lesson will appear here. Your learning journey can start anywhere.'));
  const dueList=h('ul',{id:'due-list',class:'due-list'},due.map(({entry,dueAt})=>h('li',{},h('a',{href:entry.href},h('span',{},h('strong',{},entry.title),h('small',{},pathLabel(entry))),h('span',{class:'due-date'},dateLabel(dueAt)+' ↗')))));
  const review=h('section',{class:'review-card surface'},h('div',{class:'card-heading'},h('h2',{},'A little refresh'),h('span',{class:'count-pill'},String(due.length))),h('p',{class:'muted'},'Revisit a familiar idea. Make it stick.'),due.length?dueList:h('div',{class:'review-empty'},h('span',{'aria-hidden':'true'},'✧'),h('strong',{},'You’re all caught up.'),h('p',{},'Master a concept and we’ll bring it back\nwhen it’s time for a quick review.')));
  const cards=catalog.roots.flatMap(root=>{const hubs=root.children.filter(e=>e.kind==='hub');return hubs.length?hubs:[root];});
  const grid=h('div',{class:'category-grid'},cards.map(entry=>{
    const rollup=progress(catalog,store.state,entry.topicIds),bar=h('progress',{max:100,value:rollup.percent,'aria-label':entry.title+' mastery'},rollup.percent+'%');
    return h('section',{class:'category-card surface'},h('div',{class:'card-heading'},h('span',{class:'category-icon','aria-hidden':'true'},'⌘'),h('span',{class:'muted'},`${rollup.total} concepts`)),h('p',{class:'eyebrow'},pathLabel(entry)||'LIBRARY'),h('a',{class:'category-title',href:entry.href},entry.title+' ↗'),h('div',{class:'category-children'},entry.children.filter(e=>e.kind==='hub').map(child=>h('a',{href:child.href},child.title))),h('div',{class:'category-progress'},h('span',{},`${rollup.mastered} / ${rollup.total} mastered`),h('strong',{},rollup.percent+'%')),bar);
  }));
  const library=h('section',{class:'library-section'},h('div',{class:'section-heading'},h('div',{},h('p',{class:'eyebrow'},'FIND YOUR NEXT WHY'),h('h2',{},'Explore your knowledge')),h('span',{class:'muted'},`${catalog.topics.length} concepts · ${catalog.roots.length} learning domain${catalog.roots.length===1?'':'s'}`)),grid);
  main.replaceChildren(h('div',{class:'home-view'},hero,stats,h('div',{class:'learning-grid'},resume,review),library));
  scheduleDueRefresh();
}
function scheduleDueRefresh(){
  clearTimeout(dueTimer);if(!catalog||!['','#','#/'].includes(location.hash))return;
  const now=Date.now(),next=scheduledReviews(catalog,store.state).find(r=>r.dueAt>now);
  if(next)dueTimer=setTimeout(()=>{if(['','#','#/'].includes(location.hash))renderHome();},Math.min(2147483647,Math.max(1,next.dueAt-now)));
}
function updateProgress(){
  if(!catalog)return;const p=progress(catalog,store.state);$('#global-percent').textContent=p.percent+'%';$('#global-progress').value=p.percent;$('#global-progress').textContent=p.percent+'%';$('#global-progress').setAttribute('aria-label',`${p.mastered} of ${p.total} concepts mastered`);updateBadges();
}
function learningControls(article,entry){
  if(entry.kind!=='topic')return;
  const select=h('select',{id:'topic-status','aria-label':'Progress'});
  for(const [value,label] of Object.entries(labelStatus))select.append(h('option',{value},label));
  const toolbar=h('div',{class:'lesson-toolbar','data-host-controls':''},h('div',{class:'progress-status'},h('label',{for:'topic-status'},'Progress'),select),h('div',{class:'review-controls',hidden:true}));
  article.querySelector('h1').after(toolbar);
  for(const question of article.querySelectorAll('details.kb-question')){
    const group=h('div',{class:'confidence-controls',role:'group','aria-label':'How confidently could you answer?','data-host-confidence':''},h('span',{},'How did that feel?'));
    for(const value of ['hard','good','easy'])group.append(action(value[0].toUpperCase()+value.slice(1),'confidence',{'data-key':question.dataset.recallId,'data-confidence':value,'aria-pressed':'false'}));
    question.append(group);
  }
  refreshLearningControls();
}
function refreshLearningControls(){
  if(current?.entry.kind!=='topic')return;
  const record=topicRecord(store.state,current.entry.id),select=$('#topic-status');if(!select)return;
  if(select.value!==record.status)select.value=record.status;
  for(const button of main.querySelectorAll('[data-confidence]'))button.setAttribute('aria-pressed',String(record.confidence[button.dataset.key]?.rating===button.dataset.confidence));
  const controls=main.querySelector('.review-controls');if(!controls)return;
  const review=record.review,signature=JSON.stringify([record.status,review?.lastReviewed,review?.intervalIndex,review?.session]);
  if(controls.dataset.signature===signature)return;
  const ownedFocus=controls.contains(document.activeElement);controls.dataset.signature=signature;controls.replaceChildren();controls.hidden=record.status!=='mastered';
  if(record.status==='mastered'){
    const session=review.session,due=Date.parse(review.lastReviewed)+[3,7,14,30][review.intervalIndex]*86400000;
    const shortDate=new Intl.DateTimeFormat(undefined,{month:'short',day:'numeric'}).format(new Date(due));
    controls.append(h('time',{datetime:new Date(due).toISOString(),'aria-label':'Next review: '+dateLabel(due),class:'review-date'},'Next '+shortDate));
    if(session?.completedAt===null)controls.append(action('Complete review','complete-review',{'data-session':session.id}));
    else controls.append(action(session?.completedAt?'Start another review':'Start review','start-review'));
  }
  if(ownedFocus)(controls.querySelector('button')||select).focus({preventScroll:true});
}
async function enhanceCurrent(article,entry,serial=routeSerial){
  const generation=++themeSerial;
  const errors=await enhanceArticle(article,{theme:document.documentElement.dataset.theme||'light',isCurrent:()=>serial===routeSerial&&generation===themeSerial&&article.isConnected});
  if(serial!==routeSerial||generation!==themeSerial||!article.isConnected)return;
  main.querySelector('[data-enhancement-notice]')?.remove();
  if(errors?.length){const notice=h('div',{class:'enhancement-notice','data-enhancement-notice':'',role:'status'},h('p',{},errors.join(' ')),action('Retry diagrams and code','retry-enhancements'));article.prepend(notice);status.textContent=entry.title+' is readable; some visual enhancements are unavailable.';}
  else status.textContent=entry.title+' · diagrams and content ready.';
}
function showError(error,catalogError=false){
  const view=h('section',{class:'error-view'},heading(catalogError?'Your library could not load':'This page could not load'),h('p',{},error.message),h('div',{class:'error-actions'},action('Try again',catalogError?'retry-catalog':'retry-route'),h('a',{href:'#/',class:'quiet-button'},'Go to dashboard')));
  main.replaceChildren(view);main.setAttribute('aria-busy','false');status.textContent=error.message;breadcrumbs(null,true);focusHeading();
}
async function navigate(){
  closeDialogs(true);clearTimeout(dueTimer);const serial=++routeSerial;controller?.abort();controller=new AbortController();
  try{
    const info=parseHash(location.hash,catalog);
    if(!info.home&&current?.entry.id===info.entry.id&&main.querySelector('article')){current=info;scrollSection(info.section);return;}
    current=null;main.setAttribute('aria-busy','true');activeNavigation(info.entry);breadcrumbs(info.entry);status.textContent=info.home?'Opening your dashboard…':`Opening ${info.entry.title}…`;
    main.replaceChildren(h('section',{class:'loading-view'},heading(info.home?'Your learning library':info.entry.title),h('p',{class:'muted'},'Finding your place…')));
    if(info.home){renderHome();document.title='Learning Dashboard · Backend Lab';}
    else{
      const article=await loadArticle(info.entry,appBase,controller.signal);if(serial!==routeSerial)return;
      main.replaceChildren(article);current=info;learningControls(article,info.entry);if(info.entry.kind==='topic')store.visit(info.entry.id);document.title=info.entry.title+' · Backend Lab';void enhanceCurrent(article,info.entry,serial);
    }
    main.setAttribute('aria-busy','false');status.textContent=info.home?'Your dashboard is ready.':`${info.entry.title} is ready.`;
    scrollSection(info.section);
  }catch(error){if(serial!==routeSerial||error.name==='AbortError')return;current=null;activeNavigation(null);showError(error);}
  finally{if(serial===routeSerial)main.setAttribute('aria-busy','false');}
}
function scrollSection(section){
  const target=section?main.querySelector(`[data-section="${section}"]`):null;
  if(section&&!target)throw Error('The selected lesson section is missing.');
  if(target){for(let ancestor=target.parentElement;ancestor&&ancestor!==main;ancestor=ancestor.parentElement)if(ancestor.tagName==='DETAILS')ancestor.open=true;target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});focusHeading(target.querySelector('h2'));}
  else{focusHeading();window.scrollTo({top:0,behavior:'instant'});}
}
async function boot(){
  ++routeSerial;controller?.abort();current=null;catalog=null;clearTimeout(dueTimer);$('#library-nav').replaceChildren(h('p',{class:'muted'},'Opening your library…'));
  main.setAttribute('aria-busy','true');status.textContent='Opening your library…';
  try{const response=await fetch(new URL('./manifest.json',appBase));if(!response.ok)throw Error('Could not load the library manifest.');catalog=indexCatalog(await response.json());$('#library-count').textContent=catalog.topics.length;for(const entry of catalog.entries)if(entry.ancestry.length<=2)expanded.add(entry.id);renderSidebar();updateProgress();await navigate();}
  catch(error){showError(error,true);}
}
window.addEventListener('hashchange',()=>{if(catalog)navigate();});
document.addEventListener('click',event=>{
  const closer=event.target.closest('[data-close-dialog]');if(closer){closer.closest('dialog').close('cancel');return;}
  const button=event.target.closest('[data-action]');
  if(button){
    const name=button.dataset.action;
    if(name==='retry-catalog')boot();if(name==='retry-route')navigate();
    if(name==='retry-enhancements'&&current)void enhanceCurrent(main.querySelector('article'),current.entry);
    if(name==='confidence'&&current)store.update(s=>rateQuestion(s,current.entry.id,button.dataset.key,button.dataset.confidence,new Date().toISOString()));
    if(name==='start-review'&&current)store.update(s=>startReview(s,current.entry.id,new Date().toISOString()));
    if(name==='complete-review'&&current)store.update(s=>completeReview(s,current.entry.id,button.dataset.session,new Date().toISOString()));
    if(name==='toggle-branch'){const id=button.dataset.id,branch=branches.get(id);const open=!expanded.has(id);if(open)expanded.add(id);else expanded.delete(id);branch.list.hidden=!open;button.textContent=open?'⌄':'›';button.setAttribute('aria-expanded',String(open));button.setAttribute('aria-label',`${open?'Collapse':'Expand'} ${catalog.byId.get(id).title}`);}
  }
  const link=event.target.closest('a');if(!link||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  if(link.classList.contains('skip-link')){event.preventDefault();main.focus();return;}
  if(link.getAttribute('href')===location.hash&&link.getAttribute('href')?.startsWith('#/')){event.preventDefault();navigate();}
});
$('#search-open').addEventListener('click',openSearch);$('#search-input').addEventListener('input',renderSearch);
$('#search-input').addEventListener('keydown',event=>{
  if(['ArrowDown','ArrowUp'].includes(event.key)&&searchResults.length){event.preventDefault();searchIndex=(searchIndex+(event.key==='ArrowDown'?1:-1)+searchResults.length)%searchResults.length;updateSearchSelection();}
  if(event.key==='Enter'&&searchResults.length){event.preventDefault();const href=searchResults[searchIndex].href;closeDialogs(true);if(location.hash===href)navigate();else location.hash=href;}
});
document.addEventListener('keydown',event=>{if((event.metaKey||event.ctrlKey)&&!event.altKey&&event.key.toLowerCase()==='k'){event.preventDefault();openSearch();}});
$('#main-content').addEventListener('change',event=>{if(event.target.id==='topic-status'&&current)store.update(s=>markStatus(s,current.entry.id,event.target.value,new Date().toISOString()));});
function refreshReviewView(){if(catalog&&['','#','#/'].includes(location.hash))renderHome();}
window.addEventListener('focus',refreshReviewView);document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshReviewView();});
persistence();syncSidebar();applyTheme();store.subscribe(()=>{persistence();applyTheme();updateProgress();refreshLearningControls();if(catalog&&['','#','#/'].includes(location.hash))renderHome();});
await boot();
