/** Trusted repository partial loading; optional enhancements never own navigation. */
export async function loadArticle(entry,appBase,signal){
  const response=await fetch(new URL(entry.path,appBase),{signal,cache:'no-cache'});
  if(!response.ok)throw Error(`Could not load ${entry.title} (${response.status}).`);
  const source=await response.text(),doc=new DOMParser().parseFromString(source,'text/html'),article=doc.body.firstElementChild;
  if(doc.body.children.length!==1||article?.tagName!=='ARTICLE'||article.dataset.nodeId!==entry.id||!article.classList.contains(entry.kind==='hub'?'kb-hub':'kb-topic')||article.querySelector('h1')?.textContent.trim()!==entry.title||doc.querySelector('script,style,link'))throw Error('The lesson file does not match its library entry.');
  for(const question of article.querySelectorAll('details.kb-question'))question.open=false;
  return article;
}

export const LIBRARY_VERSIONS={mermaid:'12.3.0',highlight:'11.11.1'};
let mermaidPromise,highlightPromise,mermaidAttempt=0,configuredTheme='',queue=Promise.resolve();
const diagramRecords=new WeakMap();
function timeout(promise){return Promise.race([promise,new Promise((_,reject)=>setTimeout(()=>reject(Error('The rendering library did not load. Check your connection and retry.')),15000))]);}
function mermaidLibrary(){
  if(!mermaidPromise){
    const suffix=mermaidAttempt++?'?retry='+mermaidAttempt:'';
    mermaidPromise=timeout(import('https://cdn.jsdelivr.net/npm/mermaid@12.3.0/dist/mermaid.esm.min.mjs'+suffix)).then(module=>module.default).catch(error=>{mermaidPromise=null;throw error;});
  }
  return mermaidPromise;
}
function highlightLibrary(){
  if(window.hljs)return Promise.resolve(window.hljs);
  if(!highlightPromise)highlightPromise=timeout(new Promise((resolve,reject)=>{
    const script=document.createElement('script');script.src='https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.11.1/highlight.min.js';script.async=true;
    script.onload=()=>window.hljs?resolve(window.hljs):reject(Error('Code highlighting is unavailable.'));
    script.onerror=()=>{script.remove();reject(Error('Code highlighting is unavailable. Check your connection and retry.'));};document.head.append(script);
  })).catch(error=>{highlightPromise=null;throw error;});
  return highlightPromise;
}
function recordsFor(article){
  if(!diagramRecords.has(article))diagramRecords.set(article,[...article.querySelectorAll('pre.mermaid')].map(element=>({element,source:element.textContent,theme:null})));
  return diagramRecords.get(article);
}
export async function enhanceArticle(article,{theme='light',isCurrent=()=>article.isConnected}={}){
  const records=recordsFor(article);article.dataset.enhancement='pending';
  const diagramJob=async()=>{
    const mermaid=await mermaidLibrary();if(!isCurrent())return;
    const job=queue.catch(()=>{}).then(async()=>{
      if(!isCurrent())return;
      if(configuredTheme!==theme){mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:theme==='dark'?'dark':'default',htmlLabels:false});configuredTheme=theme;}
      for(const record of records){
        if(!isCurrent())return;
        if(record.theme===theme&&record.element.querySelector('svg'))continue;
        const fresh=document.createElement('pre');fresh.className='mermaid';fresh.textContent=record.source;record.element.replaceWith(fresh);record.element=fresh;
        try{await mermaid.run({nodes:[fresh]});if(!fresh.querySelector('svg'))throw Error('A diagram did not render.');record.theme=theme;}
        catch(error){fresh.replaceChildren(document.createTextNode(record.source));fresh.removeAttribute('data-processed');record.theme=null;throw Error('A diagram could not render: '+error.message);}
      }
    });queue=job;await job;
  };
  const codeJob=async()=>{
    const code=[...article.querySelectorAll('pre:not(.mermaid) > code')];if(!code.length)return;
    const hljs=await highlightLibrary();if(!isCurrent())return;
    for(const element of code){if(element.dataset.highlighted)continue;const language=[...element.classList].find(c=>c.startsWith('language-'))?.slice(9);if(!language||hljs.getLanguage(language))hljs.highlightElement(element);}
  };
  const results=await Promise.allSettled([diagramJob(),codeJob()]);if(!isCurrent())return [];
  const errors=results.filter(r=>r.status==='rejected').map(r=>r.reason.message);article.dataset.enhancement=errors.length?'error':'complete';return errors;
}

let printSnapshot=null;
function preparePrint(){
  if(printSnapshot)return;printSnapshot=[...document.querySelectorAll('#main-content article details')].map(element=>[element,element.open]);
  for(const [element] of printSnapshot)element.open=true;
}
function restorePrint(){
  if(!printSnapshot)return;for(const [element,open] of printSnapshot)if(element.isConnected)element.open=open;printSnapshot=null;
}
window.addEventListener('beforeprint',preparePrint);window.addEventListener('afterprint',restorePrint);
