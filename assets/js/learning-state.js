/** Stable-ID learning records. No DOM or implicit completion side effects. */
export const STORAGE_KEY='backend-lab.learning.v1';
export const INTERVALS=[3,7,14,30];
export const DAY=86400000;
const statuses=['not-started','in-progress','mastered'];
const ratings=['hard','good','easy'];
const tokenPattern=/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const keyPattern=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const isObject=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
function requireValue(condition,message){if(!condition)throw Error(message);}
function shape(value,keys,label){
  requireValue(isObject(value)&&Object.keys(value).length===keys.length&&keys.every(k=>Object.hasOwn(value,k)),`Invalid ${label} fields.`);
}
function timestamp(value){
  requireValue(typeof value==='string'&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value)&&Number.isFinite(Date.parse(value))&&new Date(value).toISOString()===value,'Invalid UTC calendar timestamp.');
}
const positive=v=>Number.isSafeInteger(v)&&v>0;
const interval=v=>Number.isInteger(v)&&v>=0&&v<=3;
const isToken=v=>typeof v==='string'&&tokenPattern.test(v);
export function emptyState(now=new Date().toISOString()){
  return {format:'backend-lab.learning',version:1,updatedAt:now,preferences:{theme:null},topics:{}};
}
export function defaultTopic(){return {status:'not-started',lastVisitedAt:null,confidence:{},review:null};}
export function topicRecord(state,id){return Object.hasOwn(state.topics,id)?state.topics[id]:defaultTopic();}
export function validateState(state){
  shape(state,['format','version','updatedAt','preferences','topics'],'workspace');
  requireValue(state.format==='backend-lab.learning'&&state.version===1,'Unsupported workspace version.');timestamp(state.updatedAt);
  shape(state.preferences,['theme'],'preferences');requireValue([null,'light','dark'].includes(state.preferences.theme),'Invalid theme.');
  requireValue(isObject(state.topics),'Invalid topic dictionary.');
  for(const [id,topic] of Object.entries(state.topics)){
    requireValue(id.length>0&&!/\s/.test(id),'Invalid topic identity.');
    shape(topic,['status','lastVisitedAt','confidence','review'],'topic');requireValue(statuses.includes(topic.status),'Invalid topic status.');
    if(topic.lastVisitedAt!==null)timestamp(topic.lastVisitedAt);
    requireValue(isObject(topic.confidence),'Invalid confidence dictionary.');
    for(const [key,confidence] of Object.entries(topic.confidence)){
      requireValue(keyPattern.test(key),'Invalid recall key.');shape(confidence,['rating','ratedAt'],'confidence');requireValue(ratings.includes(confidence.rating),'Invalid confidence rating.');timestamp(confidence.ratedAt);
    }
    requireValue(topic.status!=='mastered'||topic.review!==null,'Mastered topics require review state.');
    if(topic.review===null)continue;
    const r=topic.review;shape(r,['cycle','lastReviewed','intervalIndex','history','session'],'review');
    requireValue(positive(r.cycle)&&interval(r.intervalIndex)&&Array.isArray(r.history)&&r.history.length>0,'Invalid review cycle or history.');timestamp(r.lastReviewed);
    let cycle=0,index=0;const sessions=new Map();
    for(const event of r.history){
      shape(event,['cycle','kind','sessionId','reviewedAt','intervalIndex'],'review event');timestamp(event.reviewedAt);
      requireValue(positive(event.cycle)&&interval(event.intervalIndex),'Invalid review event values.');
      if(event.kind==='mastered'){
        requireValue(event.cycle===cycle+1&&event.intervalIndex===0&&event.sessionId===null,'Invalid mastery cycle sequence.');cycle=event.cycle;index=0;
      }else{
        requireValue(event.kind==='review'&&cycle>0&&event.cycle===cycle&&event.intervalIndex===Math.min(index+1,3)&&isToken(event.sessionId)&&!sessions.has(event.sessionId),'Invalid or duplicate review session event.');
        index=event.intervalIndex;sessions.set(event.sessionId,event);
      }
    }
    const latest=r.history.at(-1);
    requireValue(r.cycle===cycle&&r.intervalIndex===index&&r.lastReviewed===latest.reviewedAt,'Review cache does not match history.');
    if(r.session!==null){
      const s=r.session;shape(s,['id','cycle','startedAt','completedAt'],'session');timestamp(s.startedAt);
      requireValue(topic.status==='mastered'&&isToken(s.id)&&s.cycle===cycle,'Invalid active review session.');
      if(s.completedAt===null)requireValue(!sessions.has(s.id),'Completed review cannot be replayed.');
      else{
        timestamp(s.completedAt);const event=sessions.get(s.id);
        requireValue(s.completedAt>=s.startedAt&&event&&event.cycle===cycle&&event.reviewedAt===s.completedAt&&latest===event,'Session completion does not match the latest review.');
      }
    }
  }
  return state;
}
export function progress(catalog,state,ids=catalog.topics.map(t=>t.id)){
  const current=new Set(catalog.topics.map(t=>t.id));const leaves=[...new Set(ids)].filter(id=>current.has(id));
  const mastered=leaves.filter(id=>topicRecord(state,id).status==='mastered').length,total=leaves.length;
  return {mastered,total,percent:total?Math.round(mastered/total*100):0};
}
export function scheduledReviews(catalog,state){
  return catalog.topics.filter(e=>topicRecord(state,e.id).status==='mastered').map(entry=>{
    const review=topicRecord(state,entry.id).review;
    return {entry,dueAt:Date.parse(review.lastReviewed)+INTERVALS[review.intervalIndex]*DAY};
  }).sort((a,b)=>a.dueAt-b.dueAt||a.entry.index-b.entry.index);
}
export function reviewQueue(catalog,state,now=Date.now()){return scheduledReviews(catalog,state).filter(r=>r.dueAt<=now);}
export function continueLearning(catalog,state,now=Date.now()){
  const unfinished=catalog.topics.filter(e=>topicRecord(state,e.id).status!=='mastered');
  if(unfinished.length){
    const visited=unfinished.filter(e=>topicRecord(state,e.id).lastVisitedAt).sort((a,b)=>topicRecord(state,b.id).lastVisitedAt.localeCompare(topicRecord(state,a.id).lastVisitedAt)||a.index-b.index);
    return {entry:visited[0]||unfinished[0],kind:visited.length?'continue':'start'};
  }
  const next=scheduledReviews(catalog,state)[0];return next?{...next,kind:next.dueAt<=now?'due':'scheduled'}:null;
}
export function visitTopic(state,id,now){
  const next=structuredClone(state);next.topics=Object.fromEntries(Object.entries(next.topics));
  const topic=structuredClone(topicRecord(state,id));topic.lastVisitedAt=now;
  Object.defineProperty(next.topics,id,{value:topic,writable:true,configurable:true,enumerable:true});next.updatedAt=now;return next;
}
function changeTopic(state,id,now,mutate){
  const next=structuredClone(state),topic=structuredClone(topicRecord(state,id));mutate(topic);
  Object.defineProperty(next.topics,id,{value:topic,writable:true,configurable:true,enumerable:true});next.updatedAt=now;return validateState(next);
}
export function markStatus(state,id,value,now){
  requireValue(statuses.includes(value),'Invalid topic status.');if(topicRecord(state,id).status===value)return state;
  return changeTopic(state,id,now,topic=>{
    topic.status=value;
    if(value==='mastered'){
      const cycle=(topic.review?.cycle||0)+1,history=topic.review?.history||[];
      history.push({cycle,kind:'mastered',sessionId:null,reviewedAt:now,intervalIndex:0});
      topic.review={cycle,lastReviewed:now,intervalIndex:0,history,session:null};
    }else if(topic.review)topic.review.session=null;
  });
}
export function rateQuestion(state,id,key,rating,now){
  requireValue(typeof key==='string'&&keyPattern.test(key)&&ratings.includes(rating),'Invalid recall confidence.');
  return changeTopic(state,id,now,topic=>{topic.confidence[key]={rating,ratedAt:now};});
}
export function startReview(state,id,now,token=globalThis.crypto.randomUUID()){
  const record=topicRecord(state,id);requireValue(record.status==='mastered','Master this topic before starting a review.');
  if(record.review.session&&record.review.session.completedAt===null)return state;
  requireValue(isToken(token),'Invalid review session identity.');
  return changeTopic(state,id,now,topic=>{topic.review.session={id:token,cycle:topic.review.cycle,startedAt:now,completedAt:null};});
}
export function completeReview(state,id,token,now){
  const r=topicRecord(state,id);const session=r.review?.session;
  if(r.status!=='mastered'||!session||session.id!==token||session.completedAt!==null||session.cycle!==r.review.cycle)return state;
  return changeTopic(state,id,now,topic=>{
    const review=topic.review;review.intervalIndex=Math.min(review.intervalIndex+1,3);review.lastReviewed=now;review.session.completedAt=now;
    review.history.push({cycle:review.cycle,kind:'review',sessionId:token,reviewedAt:now,intervalIndex:review.intervalIndex});
  });
}
export function exportBackup(state,now=new Date().toISOString()){
  validateState(state);timestamp(now);return {format:'backend-lab.progress-backup',version:1,exportedAt:now,state:structuredClone(state)};
}
export function parseBackup(input){
  let backup;try{backup=JSON.parse(input);}catch{throw Error('This file is not valid JSON.');}
  shape(backup,['format','version','exportedAt','state'],'backup');
  requireValue(backup.format==='backend-lab.progress-backup'&&backup.version===1,'Unsupported backup format or version.');timestamp(backup.exportedAt);return validateState(backup.state);
}
export function setTheme(state,value,now){
  requireValue([null,'light','dark'].includes(value),'Invalid theme preference.');if(state.preferences.theme===value)return state;
  const next=structuredClone(state);next.preferences.theme=value;next.updatedAt=now;return validateState(next);
}
export function createStore(storage,{now=()=>new Date().toISOString()}={}){
  let state=emptyState(now()),warning='',blocked=false;const listeners=new Set();
  try{const raw=storage.getItem(STORAGE_KEY);if(raw!==null)state=validateState(JSON.parse(raw));}
  catch{blocked=true;warning='Changes are not saved. Existing progress could not be read and has been preserved. Export this session or import a valid backup to recover.';}
  function publish(){for(const fn of listeners)fn(state,warning);}
  return {
    get state(){return state;},get warning(){return warning;},
    subscribe(fn){listeners.add(fn);return()=>listeners.delete(fn);},
    update(fn){
      const candidate=fn(state);if(candidate===state)return;validateState(candidate);state=candidate;
      if(!blocked){try{storage.setItem(STORAGE_KEY,JSON.stringify(state));warning='';}catch{warning='Changes are not saved. Browser storage is unavailable or full. Export your current session to keep it.';}}
      publish();
    },
    visit(id){this.update(s=>visitTopic(s,id,now()));},
    replace(candidate){
      validateState(candidate);const serialized=JSON.stringify(candidate);
      storage.setItem(STORAGE_KEY,serialized);state=JSON.parse(serialized);warning='';blocked=false;publish();
    },
  };
}
