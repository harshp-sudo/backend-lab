#!/usr/bin/env python3
"""Audited, resumable copy-only migration; default is a nonmutating preview."""
import argparse
import itertools
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import validate_content as vc

INTRO='Continue by comparing the related decisions:'

class Spans(HTMLParser):
    def __init__(self,source):
        super().__init__(convert_charrefs=True);self.source=source
        self.lines=[0]+[i+1 for i,c in enumerate(source) if c=='\n']
        self.root=vc.Element('document');self.stack=[self.root];self.feed(source);self.close()
        if len(self.stack)!=1:raise ValueError('Unclosed source elements')
    def source_offset(self):
        row,col=self.getpos();return self.lines[row-1]+col
    def handle_starttag(self,tag,attrs):
        el=vc.Element(tag,dict(attrs));el.start=self.source_offset();el.open_end=el.start+len(self.get_starttag_text());el.end=el.open_end;el.parent=self.stack[-1];el.parent.children.append(el)
        if tag not in vc.ArticleParser.VOID:self.stack.append(el)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in vc.ArticleParser.VOID:self.stack.pop()
    def handle_endtag(self,tag):
        if len(self.stack)<2 or self.stack[-1].tag!=tag:raise ValueError('Unbalanced source '+tag)
        el=self.stack.pop();el.end=self.source.index('>',self.source_offset())+1
    def handle_data(self,data):self.stack[-1].children.append(data)

def parse(source):return Spans(source)

def transform(source,variants,scope='all'):
    if scope not in ('sources','related','all'):raise ValueError('Unknown migration scope')
    tree=parse(source);edits=[]
    if scope in ('sources','all'):
        notes=[n for n in tree.root.all() if 'data-interview-research' in n.attrs]
        if len(notes)!=1:raise ValueError('Expected exactly one source note')
        note=notes[0];children=[n for n in note.children if isinstance(n,vc.Element)]
        if not children:raise ValueError('Empty source note')
        if children[0].tag=='h4' and children[0].text()=='Sources' and not note.all('p'):
            pass
        elif children[0].tag=='p' and children[0].text() in variants and len(note.all('p'))==1:
            paragraph=children[0];inline=paragraph.all('a')
            replacement='<h4>Sources</h4>'
            if inline:replacement+='<ul>'+''.join('<li>'+source[a.start:a.end]+'</li>' for a in inline)+'</ul>'
            edits.append((paragraph.start,paragraph.end,replacement))
        else:raise ValueError('Unexpected source note shape or unaudited paragraph')
    if scope in ('related','all'):
        for p in tree.root.all('p'):
            if p.text()!=INTRO:continue
            parent=p.parent
            if parent.tag!='footer' or not any(a.attrs.get('href','').startswith('#/') for a in parent.all('a')):
                raise ValueError('Related preamble outside a related footer')
            edits.append((p.start,p.end,'<h4>Related topics</h4>'))
    for start,end,replacement in sorted(edits,reverse=True):source=source[:start]+replacement+source[end:]
    return source

def snapshot(root,directory):
    if (directory/'inventory.json').exists():return
    if directory.exists() and any(directory.iterdir()):raise ValueError('Refusing to overwrite incomplete snapshot')
    directory.mkdir(parents=True,exist_ok=True);m=(root/'manifest.json').read_bytes();(directory/'manifest.json').write_bytes(m)
    index=vc.index_manifest(vc.load_json(root/'manifest.json'),root);nodes={};variants={}
    for item in index.values():
        raw=item['path'].read_bytes();path=item['relative_path'];dest=directory/'files'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        nodes[path]={'id':item['node']['id'],'kind':item['node']['kind'],'sha256':vc.sha256(raw),'inventory':vc.article_inventory(raw.decode())}
        if item['node']['kind']=='topic':
            note=next(e for e in parse(raw.decode()).root.all() if 'data-interview-research' in e.attrs);text=note.all('p')[0].text();variants[text]=variants.get(text,0)+1
    protected={}
    for base in ['research','docs/project','specs/001-backend-architecture','specs/002-dashboard-shell','specs/003-backfill-interview-scenarios']:
        for path in (root/base).rglob('*'):
            if path.is_file():protected[str(path.relative_to(root))]=vc.sha256(path.read_bytes())
    protected['assets/js/learning-state.js']=vc.sha256((root/'assets/js/learning-state.js').read_bytes())
    for item in index.values():
        if item['node']['kind']=='hub':protected[item['relative_path']]=vc.sha256(item['path'].read_bytes())
    protected['manifest.json']=vc.sha256(m)
    (directory/'inventory.json').write_text(json.dumps({'nodes':nodes,'variants':variants,'researchMappings':vc.load_json(root/'tests/content/publishing.json').get('researchRecords',{})},indent=2)+'\n')
    (directory/'protected.json').write_text(json.dumps(protected,indent=2)+'\n')

def run(root,directory,scope='all',apply=False,verify=False):
    snapshot(root,directory);inventory=vc.load_json(directory/'inventory.json');variants=set(inventory['variants']);changes=[];count=0
    if (root/'manifest.json').read_bytes()!=(directory/'manifest.json').read_bytes():raise ValueError('Manifest differs from original snapshot')
    for path,node in inventory['nodes'].items():
        if node['kind']!='topic':continue
        count+=1;original=(directory/'files'/path).read_bytes().decode();target=root/path;current=target.read_bytes().decode()
        possibilities={transform(original,variants,s) for s in ('sources','related','all')}|{original}
        if current not in possibilities:raise ValueError('Unexpected content change: '+path)
        desired=transform(current,variants,scope)
        if verify and current!=desired:raise ValueError('Incomplete '+scope+' migration: '+path)
        if desired!=current:
            changes.append(path)
            if apply:target.write_bytes(desired.encode())
    for path,digest in vc.load_json(directory/'protected.json').items():
        if not (root/path).is_file() or vc.sha256((root/path).read_bytes())!=digest:raise ValueError('Protected file changed: '+path)
    if vc.load_json(root/'tests/content/publishing.json').get('researchRecords',{})!=inventory['researchMappings']:raise ValueError('Historical research mappings changed')
    return {'result':'pass','mode':'verify' if verify else 'apply' if apply else 'dry-run','scope':scope,'topics':count,'changed':changes,'protectedFiles':len(vc.load_json(directory/'protected.json'))}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--scope',choices=['sources','related','all'],default='all');g=p.add_mutually_exclusive_group();g.add_argument('--apply',action='store_true');g.add_argument('--verify',action='store_true');a=p.parse_args()
    try:print(json.dumps(run(Path.cwd(),a.snapshot,a.scope,a.apply,a.verify),indent=2));return 0
    except (ValueError,OSError,KeyError) as e:print(str(e),file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
