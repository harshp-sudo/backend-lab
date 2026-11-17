"""Publishing grows beyond a frozen batch without weakening current lesson contracts."""
import copy
import json
import subprocess
import sys
from pathlib import Path
from urllib.request import urlopen

from test_validate_content import FixtureBase, article, hub_article, topic, hub
from tools import validate_content as vc
from tools import check_topics as publish


def write_catalog(root, data):
    (root/'manifest.json').write_text(json.dumps(data))
    index=vc.index_manifest(data,root)
    for item in index.values():
        item['path'].parent.mkdir(parents=True,exist_ok=True)
        source=(article(item).replace(vc.INTERVIEW_START,'').replace(vc.INTERVIEW_END,'')
                if item['node']['kind']=='topic' else hub_article(item))
        item['path'].write_text(source)
    return index


def research(item):
    source=item['path'].read_text();parser=vc.parsed_article(source)
    note=next(e for e in parser.root.all() if 'data-interview-research' in e.attrs)
    return dict(topicId=item['node']['id'],title=item['node']['title'],path=item['relative_path'],
        constitutionVersion='1.3.0',researchedOn='2026-11-17',state='reviewed',
        searches=[dict(query='Fixture exact-concept question research',date='2026-11-17',result='success; frequency unverified')],
        sources=[dict(id='S1',title='Fixture primary source',url='https://example.com/source',roles=['technical-primary'],checkedOn='2026-11-17',supportRationale='Fixture source mapping')],
        scenarios=[dict(key=key,theme='Constraint '+key,basis='adapted-production',selectionSources=['S1'],technicalSources=['S1'],supportedInterviewClaim='none',assumptions='Fixture bounded assumptions',limitations='Frequency unverified',editorial={criterion:dict(status='pass',rationale='Fixture review finding') for criterion in vc.EDITORIAL_CRITERIA}) for key in vc.article_inventory(source)['interviewKeys']],
        publicDisclosure=note.all('p')[0].text(),sourceNoteUrls=['https://example.com/source'])


class PublishingTests(FixtureBase):
    def setUp(self):
        super().setUp()
        self.expected=dict(profile='topic-publishing',recallProfile=vc.CURRENT_PROFILE,researchDirectory='research/topics')
        self.index=write_catalog(self.root,self.data)
        self.records()

    def records(self):
        for item in self.index.values():
            if item['node']['kind']=='topic':
                path=self.root/'research/topics'/ (item['node']['id']+'.json')
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(json.dumps(research(item)))

    def test_new_topic_and_new_discipline_need_no_migration_files(self):
        before=copy.deepcopy(self.data)
        self.data['roots'][0]['children'].append(topic('another-topic'))
        self.data['roots'].append(hub([hub([topic('new-field')],slug='category')],slug='another-discipline'))
        self.index=write_catalog(self.root,self.data);self.records()
        result=vc.validate(self.root,self.expected,before)
        self.assertEqual(result['result'],'pass',result['checks'])
        self.assertEqual(result['counts']['batch'],{'topics':3,'hubs':3})
        self.assertFalse((self.root/'specs').exists())

    def test_scoped_new_lesson_without_preservation_markers(self):
        result=vc.validate(self.root,self.expected,lesson='topics/domain/example.html')
        self.assertEqual(result['result'],'pass',result['checks'])
        self.assertEqual(len(result['lessons']),1)

    def test_missing_or_draft_research_still_fails(self):
        item=self.index['/domain/example'];path=self.root/'research/topics'/ (item['node']['id']+'.json')
        path.unlink()
        self.assertEqual(vc.validate(self.root,self.expected)['result'],'fail')
        record=research(item);record['state']='draft';path.write_text(json.dumps(record))
        self.assertEqual(vc.validate(self.root,self.expected)['result'],'fail')

    def test_incomplete_answers_still_fail(self):
        item=self.index['/domain/example']
        item['path'].write_text(item['path'].read_text().replace('The Direct Answer &amp; Architectural Decision','Decision'))
        self.assertEqual(vc.validate(self.root,self.expected)['result'],'fail')

    def test_changed_lesson_selects_only_itself_and_ancestors(self):
        self.data['roots'][0]['children'].append(topic('unrelated'))
        self.index=write_catalog(self.root,self.data)
        selected,runtime=publish.select_nodes(self.index,['topics/domain/example.html'])
        self.assertFalse(runtime)
        self.assertEqual([i['route'] for i in selected],['/domain','/domain/example'])

    def test_manifest_delta_finds_addition_without_selecting_unrelated_lesson(self):
        before=copy.deepcopy(self.data)
        self.data['roots'][0]['children'].append(topic('new-topic'))
        self.index=write_catalog(self.root,self.data)
        selected=publish.apply_catalog_delta(self.index,[],before,self.root)
        self.assertEqual([i['route'] for i in selected],['/domain','/domain/new-topic'])

    def test_manifest_delta_finds_move_and_rename(self):
        before=copy.deepcopy(self.data)
        self.data['roots'][0]['children'][0].update(slug='renamed',title='Renamed')
        self.index=write_catalog(self.root,self.data)
        selected=publish.apply_catalog_delta(self.index,[],before,self.root)
        self.assertEqual({i['route'] for i in selected},{'/domain','/domain/renamed'})

    def test_shared_runtime_and_standard_changes_broaden_scope(self):
        for path in ['assets/js/content-renderer.js','styles.css','.specify/memory/constitution.md']:
            selected,runtime=publish.select_nodes(self.index,[path])
            self.assertEqual(len(selected),len(self.index))
            self.assertEqual(runtime,path!='.specify/memory/constitution.md')

    def test_research_changes_select_lesson(self):
        item=self.index['/domain/example'];identity=item['node']['id']
        for path,mapping in [('research/topics/'+identity+'.json',{}),('old/research.md',{identity:'old/research.md'})]:
            selected,_=publish.select_nodes(self.index,[path],research_records=mapping)
            self.assertEqual({i['route'] for i in selected},{'/domain','/domain/example'})

    def test_server_owns_root_project_paths_and_releases_port(self):
        with publish.serve(self.root) as bases:
            for base in bases:
                with urlopen(base+'manifest.json') as response:
                    self.assertEqual(json.load(response),self.data)
        with self.assertRaises(OSError):urlopen(bases[0]+'manifest.json',timeout=.5)

    def test_untracked_files_are_discovered(self):
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        self.assertIn('topics/domain/example.html',publish.changed_paths(self.root))
        self.assertIn('manifest.json',publish.changed_paths(self.root))

    def test_non_git_requires_explicit_paths(self):
        with self.assertRaises(vc.ValidationError):publish.changed_paths(self.root)

    def test_cache_requires_current_inputs_and_both_intact_pdfs(self):
        one=self.root/'light.pdf';two=self.root/'dark.pdf';one.write_bytes(b'light');two.write_bytes(b'dark')
        row=dict(status='pass',fingerprint='current',outputs=[dict(theme=t,pdf=str(p),sha256=vc.sha256(p.read_bytes())) for t,p in [('light',one),('dark',two)]])
        self.assertTrue(publish.reusable(row,'current'))
        self.assertFalse(publish.reusable(row,'changed'))
        two.write_bytes(b'tampered')
        self.assertFalse(publish.reusable(row,'current'))
        self.assertFalse(publish.reusable({**row,'outputs':[]},'current'))
        self.assertFalse(publish.reusable({**row,'status':'pending'},'current'))

    def test_cache_context_excludes_unrelated_manifest_changes(self):
        old=publish.signature(self.index['/domain/example'])
        self.data['roots'][0]['children'].append(topic('unrelated'))
        self.index=write_catalog(self.root,self.data)
        self.assertEqual(publish.signature(self.index['/domain/example']),old)
        self.data['roots'][0]['title']='Renamed domain'
        self.index=write_catalog(self.root,self.data)
        self.assertNotEqual(publish.signature(self.index['/domain/example']),old)

    def test_fingerprint_tracks_shared_inputs_without_global_manifest_invalidation(self):
        files=[*publish.RUNTIME,'tools/validate_content.py','tools/check_topics.py',
            'tests/dashboard/check_dashboard.py','tests/dashboard/requirements.txt','.specify/memory/constitution.md']
        for relative in files:
            path=self.root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('fixture dependency')
        config=self.root/'tests/content/publishing.json';config.parent.mkdir(parents=True,exist_ok=True);config.write_text(json.dumps(self.expected))
        item=self.index['/domain/example'];before=publish.fingerprint(self.root,item,'browser-one')
        self.data['roots'][0]['children'].append(topic('unrelated'))
        self.index=write_catalog(self.root,self.data)
        self.assertEqual(publish.fingerprint(self.root,self.index['/domain/example'],'browser-one'),before)
        self.assertNotEqual(publish.fingerprint(self.root,item,'browser-two'),before)
        (self.root/'styles.css').write_text('updated shared styles')
        self.assertNotEqual(publish.fingerprint(self.root,item,'browser-one'),before)
        (self.root/'styles.css').write_text('fixture dependency')
        item['path'].write_text(item['path'].read_text()+'\n')
        self.assertNotEqual(publish.fingerprint(self.root,item,'browser-one'),before)

    def test_unregistered_html_and_broken_hub_links_are_rejected(self):
        (self.root/'topics/orphan.html').write_text('<article>orphan</article>')
        self.assertEqual(vc.validate(self.root,self.expected)['result'],'fail')
        (self.root/'topics/orphan.html').unlink()
        item=self.index['/domain'];item['path'].write_text(item['path'].read_text().replace('#/domain/example','#/missing'))
        self.assertEqual(vc.validate(self.root,self.expected)['result'],'fail')
