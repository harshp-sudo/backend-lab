/** Catalog data stays read-only. Routes and presentation indexes are derived. */
export const SECTION_KEYS=['hook-eli5','big-picture','mechanics','trade-offs','pitfalls','mastery'];
const slugPattern=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const object=value=>value!==null&&typeof value==='object'&&!Array.isArray(value);
export function indexCatalog(data){
  if(!object(data)||data.schemaVersion!==1||!Array.isArray(data.roots))throw Error('Unsupported or malformed library manifest.');
  const entries=[],topics=[],byId=new Map(),byRoute=new Map();
  function walk(nodes,chain=[]){
    const siblings=new Set();
    return nodes.map(node=>{
      if(!object(node)||typeof node.id!=='string'||!node.id||/\s/.test(node.id)||byId.has(node.id)||!['hub','topic'].includes(node.kind)||typeof node.title!=='string'||!node.title.trim()||typeof node.slug!=='string'||!slugPattern.test(node.slug)||siblings.has(node.slug))throw Error('Invalid or duplicate library node.');
      if(!chain.length&&node.kind!=='hub')throw Error('Library roots must be hubs.');
      if(node.kind==='hub'?(!Array.isArray(node.children)||!node.children.length):Object.hasOwn(node,'children'))throw Error('Hubs need children; lessons must be leaves.');
      siblings.add(node.slug);
      const ancestry=[...chain,node],route='/'+ancestry.map(n=>n.slug).join('/');
      if(byRoute.has(route))throw Error('Duplicate library route.');
      const entry={node,id:node.id,kind:node.kind,title:node.title,slug:node.slug,route,href:'#'+route,path:'./topics'+route+(node.kind==='hub'?'/_overview.html':'.html'),ancestry,index:entries.length,children:[],topicIds:[]};
      entries.push(entry);byId.set(node.id,entry);byRoute.set(route,entry);
      if(node.kind==='topic'){topics.push(entry);entry.topicIds=[node.id];}
      else{entry.children=walk(node.children,ancestry);entry.topicIds=[...new Set(entry.children.flatMap(c=>c.topicIds))];}
      return entry;
    });
  }
  const roots=walk(data.roots);
  return {entries,topics,byId,byRoute,roots,source:data};
}
export function parseHash(hash,catalog){
  if(['','#','#/'].includes(hash))return {home:true,entry:null,section:null};
  const match=/^#(\/[a-z0-9]+(?:-[a-z0-9]+)*(?:\/[a-z0-9]+(?:-[a-z0-9]+)*)*)(?:\?section=([a-z0-9-]+))?$/.exec(hash);
  if(!match)throw Error('This learning link has an invalid route or section.');
  const entry=catalog.byRoute.get(match[1]),section=match[2]||null;
  if(!entry)throw Error('This topic is not in your current library.');
  if(section&&(!SECTION_KEYS.includes(section)||entry.kind!=='topic'))throw Error('This lesson section does not exist.');
  return {home:false,entry,section};
}
const normalize=value=>value.trim().toLowerCase().replace(/\s+/g,' ');
function oneEdit(a,b){
  if(Math.abs(a.length-b.length)>1)return false;let i=0,j=0,edits=0;
  while(i<a.length&&j<b.length){if(a[i]===b[j]){i++;j++;continue;}if(++edits>1)return false;if(a.length>=b.length)i++;if(b.length>=a.length)j++;}
  return edits+(i<a.length||j<b.length?1:0)<=1;
}
export function searchCatalog(catalog,input){
  const query=normalize(input);if(!query)return catalog.entries;
  const words=query.split(' '),matches=[];
  for(const entry of catalog.entries){
    const title=normalize(entry.title),path=normalize(entry.ancestry.map(n=>n.title).join(' / ')+' '+entry.route),haystack=title+' '+path;
    let rank=Infinity;
    if(title===query)rank=0;
    else if(haystack.includes(query)||words.every(w=>haystack.includes(w)))rank=1;
    else if(query.length>=4&&[title,...title.split(/[^a-z0-9]+/)].some(t=>oneEdit(query,t)))rank=2;
    if(Number.isFinite(rank))matches.push({entry,rank});
  }
  return matches.sort((a,b)=>a.rank-b.rank||a.entry.index-b.entry.index).map(m=>m.entry);
}
