import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {indexCatalog,parseHash,SECTION_KEYS,searchCatalog} from '../../assets/js/catalog.js';

const manifest=JSON.parse(readFileSync(new URL('../../manifest.json',import.meta.url)));
const copy=()=>structuredClone(manifest);
const descendants=nodes=>nodes.flatMap(node=>[node,...descendants(node.children??[])]);
test('canonical catalog grows without fixed counts or rewritten metadata',()=>{
 const data=copy();data.note='retained';const before=JSON.stringify(data),c=indexCatalog(data);
 assert.equal(c.entries.length,descendants(data.roots).length);assert.equal(c.topics.length,descendants(data.roots).filter(n=>n.kind==='topic').length);assert.equal(JSON.stringify(data),before);
 assert.equal(c.entries[0].path,'./topics/'+data.roots[0].slug+'/_overview.html');
 assert.ok(c.topics.every(topic=>topic.path.startsWith('./topics/')&&topic.path.endsWith('.html')));
 assert.equal(c.entries[0].topicIds.length,descendants([data.roots[0]]).filter(n=>n.kind==='topic').length);
});
test('rejects malformed canonical nodes and duplicate identities/routes',()=>{
 for(const mutate of [x=>x.schemaVersion=2,x=>x.roots[0].kind='topic',x=>x.roots[0].children=[],x=>x.roots[0].id='has space',x=>x.roots[0].slug='../escape',x=>x.roots[0].title='  ',x=>x.roots[0].children.push(x.roots[0].children[0]),x=>descendants(x.roots).find(n=>n.kind==='topic').children=[]]){
  const m=copy();mutate(m);assert.throws(()=>indexCatalog(m));
 }
 const duplicate=copy();duplicate.roots[0].children.push({...duplicate.roots[0].children[0],id:'other'});assert.throws(()=>indexCatalog(duplicate));
});
test('opaque legacy IDs, empty initialization and six levels work',()=>{
 const m={schemaVersion:1,roots:[]};assert.equal(indexCatalog(m).entries.length,0);
 let n={id:'legacy-leaf',kind:'topic',title:'Leaf',slug:'leaf'};
 for(let i=4;i>=0;i--)n={id:'legacy-'+i,kind:'hub',title:'Level '+i,slug:'level-'+i,children:[n]};
 const c=indexCatalog({schemaVersion:1,roots:[n]});assert.equal(c.entries.length,6);assert.equal(c.topics[0].ancestry.length,6);
});
test('only known raw hashes and valid topic sections are accepted',()=>{
 const c=indexCatalog(manifest),topic=c.topics[0];
 for(const hash of ['','#','#/'])assert.equal(parseHash(hash,c).home,true);
 assert.equal(parseHash(topic.href,c).entry.id,topic.id);
 for(const key of SECTION_KEYS)assert.equal(parseHash(topic.href+'?section='+key,c).section,key);
 for(const hash of [topic.href+'/',topic.href+'?x=1',topic.href+'?section=',topic.href+'?section=unknown',topic.href+'?section=mastery&section=mastery','#/system-design?section=mechanics','#/system-design/../system-design','#/system%2ddesign','#//system-design','#/unknown','#/system-design\\oops','#/system-design?'])assert.throws(()=>parseHash(hash,c),hash);
});
test('ranked fuzzy search includes title/path, insertion, deletion and substitution',()=>{
 // Search ranking has a fixed unit fixture; unrelated new lessons may legitimately rank differently.
 const c=indexCatalog({schemaVersion:1,roots:[{id:'search-root',kind:'hub',slug:'system-design',title:'System Design',children:[
  {id:'clean',kind:'topic',slug:'clean-architecture',title:'Clean Architecture'},
  {id:'micro',kind:'topic',slug:'microservices-architecture',title:'Microservices Architecture'}
 ]}]}),clean=c.byId.get('clean');
 for(const query of ['Clean Architecture',' CLEAN   architecture ','clen architecture','cleaan architecture','cleam architecture'])assert.equal(searchCatalog(c,query)[0].id,clean.id,query);
 for(const entry of c.entries.filter(e=>e.ancestry.some(n=>n.slug==='system-design')))assert.ok(searchCatalog(c,'system design').some(match=>match.id===entry.id));assert.deepEqual(searchCatalog(c,''),c.entries);
 assert.equal(searchCatalog(c,'microservces')[0].slug,'microservices-architecture');
 assert.equal(searchCatalog(c,'unfindable zzzxyz').length,0);
 const matches=searchCatalog(c,'architecture');assert.deepEqual(matches.map(e=>e.index),matches.map(e=>e.index).sort((a,b)=>a-b));
});
