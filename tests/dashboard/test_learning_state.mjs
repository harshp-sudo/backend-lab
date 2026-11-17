import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,validateState,progress,createStore,STORAGE_KEY,reviewQueue,continueLearning,markStatus,rateQuestion,startReview,completeReview,DAY,exportBackup,parseBackup,setTheme} from '../../assets/js/learning-state.js';
import {indexCatalog} from '../../assets/js/catalog.js';
const catalog=indexCatalog(JSON.parse(readFileSync(new URL('../../manifest.json',import.meta.url))));
const example=JSON.parse(readFileSync(new URL('../../specs/002-dashboard-shell/contracts/progress-backup.example.json',import.meta.url))).state;
const total=catalog.topics.length;
const now='2026-11-17T06:00:00.000Z';
test('empty and populated states obey shape and leaf-only progress',()=>{
 const state=emptyState(now);validateState(state);assert.deepEqual(progress(catalog,state),{mastered:0,total,percent:0});
 validateState(example);const mastered=catalog.topics.filter(t=>example.topics[t.id]?.status==='mastered').length;assert.deepEqual(progress(catalog,example),{mastered,total,percent:Math.round(mastered/total*100)});
 assert.equal(progress({topics:[]},state).percent,0);
});
test('rejects invalid fields, real calendar values and review inconsistencies',()=>{
 const id=Object.keys(example.topics)[0];
 for(const mutate of [x=>x.version=2,x=>x.preferences.theme='sepia',x=>x.updatedAt='2026-02-30T06:00:00.000Z',x=>x.topics[id].status='done',x=>x.topics[id].review=null,x=>x.topics[id].review.intervalIndex=3,x=>x.topics[id].review.history[1].cycle=2,x=>x.topics[id].review.session.completedAt=null,x=>x.topics[id].confidence['dependency-direction'].rating='perfect',x=>x.extra=true]){
 const state=structuredClone(example);mutate(state);assert.throws(()=>validateState(state));
 }
});
test('corrupt bytes are retained while session visits remain usable',()=>{
 let raw='{corrupt';let writes=0;const storage={getItem:()=>raw,setItem:(k,v)=>{writes++;raw=v;}};
 const store=createStore(storage,{now:()=>now});store.visit(catalog.topics[0].id);
 assert.equal(writes,0);assert.equal(raw,'{corrupt');assert.match(store.warning,/not saved/i);assert.equal(store.state.topics[catalog.topics[0].id].status,'not-started');
});
test('whole-record save and quota failure are truthful',()=>{
 let raw=null;const store=createStore({getItem:()=>raw,setItem:(k,v)=>{assert.equal(k,STORAGE_KEY);raw=v;}},{now:()=>now});store.visit('legacy');
 assert.equal(JSON.parse(raw).topics.legacy.lastVisitedAt,now);assert.equal(store.warning,'');
 const failed=createStore({getItem:()=>null,setItem:()=>{throw Error('quota');}},{now:()=>now});failed.visit('legacy');assert.match(failed.warning,/not saved/i);assert.equal(failed.state.topics.legacy.lastVisitedAt,now);
});
test('home rollups and every next-action fallback use current leaves',()=>{
 const state=emptyState(now);for(const topic of catalog.topics.slice(0,3)){const record=structuredClone(example.topics[Object.keys(example.topics)[0]]);state.topics[topic.id]=record;}
 state.topics.unknown=structuredClone(Object.values(state.topics)[0]);
 assert.equal(progress(catalog,state).percent,Math.round(3/total*100));
 assert.equal(continueLearning(catalog,state,Date.parse(now)).entry.id,catalog.topics[3].id);
 state.topics[catalog.topics[4].id]={status:'in-progress',lastVisitedAt:now,confidence:{},review:null};
 assert.equal(continueLearning(catalog,state,Date.parse(now)).entry.id,catalog.topics[4].id);
 state.topics[catalog.topics[3].id]={...structuredClone(state.topics[catalog.topics[4].id])};
 assert.equal(continueLearning(catalog,state,Date.parse(now)).entry.id,catalog.topics[3].id);
 assert.equal(reviewQueue(catalog,state,Date.parse(now)).length,3);
 for(const topic of catalog.topics)state.topics[topic.id]=structuredClone(example.topics[Object.keys(example.topics)[0]]);
 assert.equal(progress(catalog,state).percent,100);assert.equal(continueLearning(catalog,state,Date.parse(now)).kind,'due');
 assert.equal(continueLearning(catalog,state,0).kind,'scheduled');
 assert.equal(continueLearning({topics:[]},emptyState(now),0),null);
});
test('explicit mastery and confidence retain identity without implicit completion',()=>{
 const id=catalog.topics[0].id;let state=emptyState(now);
 state=rateQuestion(state,id,'boundary','hard',now);assert.equal(state.topics[id].status,'not-started');
 state=markStatus(state,id,'in-progress',now);assert.equal(state.topics[id].review,null);
 state=markStatus(state,id,'mastered',now);validateState(state);assert.equal(state.topics[id].review.intervalIndex,0);
 assert.equal(markStatus(state,id,'mastered','2026-12-01T00:00:00.000Z'),state);
 state=markStatus(state,id,'not-started',now);state=markStatus(state,id,'mastered',now);validateState(state);assert.equal(state.topics[id].review.cycle,2);assert.equal(state.topics[id].review.history.length,2);
 const renamed=structuredClone(catalog.source);renamed.roots[0].slug='renamed';
 const renameTopic=nodes=>{for(const node of nodes){if(node.id===id)node.title='Renamed lesson';if(node.children)renameTopic(node.children);}};renameTopic(renamed.roots);
 assert.equal(progress(indexCatalog(renamed),state).mastered,1);assert.equal(state.topics[id].confidence.boundary.rating,'hard');
});
test('due boundaries, session replay, final interval and remastery are exact',()=>{
 const id=catalog.topics[0].id;let state=markStatus(emptyState(now),id,'mastered',now);let instant=Date.parse(now);
 for(const [n,days] of [3,7,14,30,30].entries()){
  const due=instant+days*DAY;assert.equal(reviewQueue(catalog,state,due-1).length,0);assert.equal(reviewQueue(catalog,state,due).length,1);assert.equal(reviewQueue(catalog,state,due+1).length,1);
  const date=new Date(due).toISOString(),token=`00000000-0000-4000-8000-${String(n).padStart(12,'0')}`;
  state=startReview(state,id,date,token);assert.equal(startReview(state,id,date),state);
  state=completeReview(state,id,token,date);validateState(state);assert.equal(completeReview(state,id,token,date),state);assert.equal(state.topics[id].review.intervalIndex,Math.min(n+1,3));
  const reloaded=JSON.parse(JSON.stringify(state));assert.equal(completeReview(reloaded,id,token,date),reloaded);instant=due;
 }
 const history=state.topics[id].review.history.length;state=markStatus(state,id,'in-progress',now);assert.equal(reviewQueue(catalog,state,Infinity).length,0);
 state=markStatus(state,id,'mastered',now);assert.equal(state.topics[id].review.cycle,2);assert.equal(state.topics[id].review.history.length,history+1);assert.equal(state.topics[id].review.intervalIndex,0);
});
test('backup preserves the entire record and refuses invalid replacements',()=>{
 const backup=exportBackup(example,now),before=JSON.stringify(example);assert.equal(backup.exportedAt,now);assert.deepEqual(parseBackup(JSON.stringify(backup)),example);assert.equal(JSON.stringify(example),before);
 for(const mutate of [x=>x.version=2,x=>x.extra=true,x=>x.exportedAt='2026-02-30T00:00:00.000Z',x=>x.state.topics[Object.keys(x.state.topics)[0]].review.history[1].intervalIndex=3]){const value=structuredClone(backup);mutate(value);assert.throws(()=>parseBackup(JSON.stringify(value)));}
 let raw=JSON.stringify(emptyState(now)),throwing=true;const store=createStore({getItem:()=>raw,setItem:(k,v)=>{if(throwing)throw Error('quota');raw=v;}},{now:()=>now});
 const original=store.state;assert.throws(()=>store.replace(example));assert.equal(store.state,original);assert.deepEqual(JSON.parse(raw),original);
 throwing=false;store.replace(example);assert.deepEqual(store.state,example);assert.deepEqual(JSON.parse(raw),example);
 const themed=setTheme(example,'light',now);assert.equal(themed.preferences.theme,'light');assert.deepEqual(themed.topics,example.topics);
 assert.equal(setTheme(themed,'light',now),themed);
});
test('opaque dictionary keys do not alter object prototypes',()=>{
 const state=emptyState(now);const store=createStore({getItem:()=>JSON.stringify(state),setItem(){}},{now:()=>now});store.visit('__proto__');
 assert.equal(Object.hasOwn(store.state.topics,'__proto__'),true);assert.equal({}.status,undefined);validateState(store.state);
});
