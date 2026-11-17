"""Contract tests use disposable fixtures, never abbreviated production lessons."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import validate_content as vc


def topic(slug='example', **extra):
    return dict(id=str(uuid.uuid4()), kind='topic', title='Example', slug=slug, **extra)


def hub(children=None, slug='domain'):
    return dict(id=str(uuid.uuid4()), kind='hub', title='Domain', slug=slug,
                children=[topic()] if children is None else children)


def catalog(node=None):
    return dict(schemaVersion=1, roots=[hub() if node is None else node])


class FixtureBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = catalog()

    def invalid(self, data):
        with self.assertRaises(vc.ValidationError):
            vc.index_manifest(data, self.root)

class CatalogTests(FixtureBase):
    def test_valid_recursive_index(self):
        index = vc.index_manifest(self.data, self.root)
        self.assertEqual(set(index), {'/domain', '/domain/example'})
        self.assertEqual(index['/domain']['relative_path'], 'topics/domain/_overview.html')
        self.assertEqual(index['/domain/example']['relative_path'], 'topics/domain/example.html')

    def test_duplicate_json_keys(self):
        p = self.root / 'bad.json'
        p.write_text('{"roots": [], "roots": [1]}')
        with self.assertRaises(vc.ValidationError): vc.load_json(p)

    def test_malformed_json(self):
        p = self.root / 'bad.json'; p.write_text('{')
        with self.assertRaises(vc.ValidationError): vc.load_json(p)

    def test_required_fields(self):
        for key in ['id', 'kind', 'title', 'slug']:
            with self.subTest(key=key):
                data = copy.deepcopy(self.data); del data['roots'][0][key]; self.invalid(data)

    def test_schema_version_and_empty_roots(self):
        for value in [2, True, '1', None]:
            data = copy.deepcopy(self.data); data['schemaVersion'] = value; self.invalid(data)
        self.invalid(dict(schemaVersion=1, roots=[]))

    def test_bad_kinds_and_child_roles(self):
        self.invalid(catalog(topic()))
        self.invalid(catalog(hub([])))
        data = copy.deepcopy(self.data); data['roots'][0]['kind'] = 'category'; self.invalid(data)
        data = copy.deepcopy(self.data); data['roots'][0]['children'][0]['children'] = []; self.invalid(data)

    def test_blank_ids_labels_slugs(self):
        for key, value in [('id',' '), ('id','x\ny'), ('title',' '), ('slug','A_B'),
                           ('slug','../bad'), ('slug','good\n'), ('slug','')]:
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.data); data['roots'][0][key] = value; self.invalid(data)

    def test_duplicate_id(self):
        self.data['roots'][0]['children'].append(copy.deepcopy(self.data['roots'][0]['children'][0]))
        self.invalid(self.data)

    def test_sibling_slug_collision_across_kinds(self):
        self.data['roots'][0]['children'].append(hub(slug='example'))
        self.invalid(self.data)

    def test_deep_recursive_catalog(self):
        node = topic()
        for depth in range(12): node = hub([node], slug=f'level-{depth}')
        self.assertEqual(len(vc.index_manifest(catalog(node), self.root)), 13)

    def test_optional_metadata_is_untouched(self):
        self.data['roots'][0]['custom'] = {'labels': ['keep']}
        original = copy.deepcopy(self.data)
        vc.index_manifest(self.data, self.root)
        self.assertEqual(self.data, original)

    def test_uuid_for_additions_legacy_retention(self):
        data = copy.deepcopy(self.data); data['roots'][0]['id'] = 'legacy-id'
        self.invalid(data)
        vc.index_manifest(data, self.root, baseline=data)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 'topics').mkdir()
            (self.root / 'topics/domain').symlink_to(outside, target_is_directory=True)
            self.invalid(self.data)

    def test_cli_unreadable_input_exit_two(self):
        result = subprocess.run([sys.executable, str(Path(vc.__file__)), '--repo-root', str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)




def interview_section(identity, count=5):
    labels = [('scenario', 'The Scenario &amp; Constraint'),
              ('decision', 'The Direct Answer &amp; Architectural Decision'),
              ('trade-offs', 'Key Trade-Offs &amp; Follow-Up Traps')]
    cards = ''.join('<details class="kb-question" data-recall-kind="interview" '
                    f'data-recall-id="interview-fixture-{i}" data-scenario-basis="adapted-production">'
                    f'<summary>Production request {i} times out: what will you do and why?</summary>' +
                    ''.join(f'<div data-scenario-part="{part}"><p><strong>{label}</strong></p>'
                            '<p>Fixture prose supplies a concrete decision and its bounded assumptions.</p></div>'
                            for part, label in labels) + '</details>' for i in range(count))
    heading = f'node-{identity}-interview-scenarios'
    return ('<!-- kb-interview-scenarios:start -->' +
            f'<section data-interview-scenarios aria-labelledby="{heading}"><h3 id="{heading}">'
            'Tricky &amp; Most-Asked Interview Scenarios</h3>' + cards +
            '<aside data-interview-research><p>2026-11-17: These are adapted production variants. '
            'Interview frequency was not independently verified. '
            '<a href="https://example.com/source">Fixture primary source</a></p></aside></section>' +
            '<!-- kb-interview-scenarios:end -->')


def article(item, *, legacy=False):
    n = item['node']; identity = n['id']
    bodies = {
        'hook-eli5':'<p>A familiar model explains the problem and purpose.</p>',
        'big-picture':'<p>The picture shows how the parts connect.</p><figure class="kb-diagram"><pre class="mermaid">graph TD\n A --> B</pre><figcaption>The parts connect.</figcaption></figure>',
        'mechanics':'<details><summary>Follow the request</summary><p>The input becomes a validated result.</p></details>',
        'trade-offs':'<p>Compare the cost of each decision.</p><table><thead><tr><th>Choice</th><th>Cost</th></tr></thead><tbody><tr><td>One</td><td>Coordination</td></tr></tbody></table>',
        'pitfalls':'<p>Symptom: missing work. Root Cause: no owner. Fix/Prevention: assign ownership.</p>',
        'mastery':'<p>Summarize this in your own words</p>'+''.join(f'<details class="kb-question" data-recall-id="question-{i}"><summary>Why is choice {i} useful?</summary><p>It makes the decision explicit.</p></details>' for i in range(3))
    }
    if not legacy: bodies['mastery'] += interview_section(identity)
    sections=''.join(f'<section data-section="{key}" id="node-{identity}-{key}"><h2>{key}</h2>{bodies[key]}</section>' for key in vc.SECTIONS)
    return f'<article class="kb-topic" data-node-id="{identity}"><h1>{n["title"]}</h1>{sections}<footer><a href="https://example.com/source">Source</a></footer></article>'


class ArticleTests(FixtureBase):
    def setUp(self):
        super().setUp()
        self.index = vc.index_manifest(self.data, self.root)
        self.item = self.index['/domain/example']
        self.html = article(self.item)

    def errors(self, html): return vc.check_article(self.item, html, self.index)

    def test_valid_topic_article(self): self.assertEqual(self.errors(self.html), [])

    def test_wrong_article_identity_and_title(self):
        for source, replacement in [(self.item['node']['id'],'wrong-id'),('<h1>Example</h1>','<h1>Wrong</h1>')]:
            with self.subTest(source=source): self.assertTrue(self.errors(self.html.replace(source,replacement)))

    def test_forbidden_markup(self):
        for extra in ['<script>bad()</script>','<style>p{color:red}</style>','<p onclick="bad()">Click</p>','<p style="color:red">X</p>','<iframe src="https://example.com"></iframe>']:
            with self.subTest(extra=extra): self.assertTrue(self.errors(self.html.replace('</article>',extra+'</article>')))

    def test_missing_or_reordered_modules(self):
        self.assertTrue(self.errors(self.html.replace('data-section="mechanics"','data-section="other"')))
        self.assertTrue(self.errors(self.html.replace('data-section="hook-eli5"','data-section="big-picture"')))

    def test_missing_diagram_and_comparison(self):
        self.assertTrue(self.errors(self.html.replace('class="mermaid"','class="other"')))
        self.assertTrue(self.errors(self.html.replace('<table>','<div>').replace('</table>','</div>')))

    def test_empty_answer_or_summary(self):
        self.assertTrue(self.errors(self.html.replace('It makes the decision explicit.','')))
        self.assertTrue(self.errors(self.html.replace('Why is choice 0 useful?','')))

    def test_recall_counts_closed_and_independent(self):
        self.assertTrue(self.errors(self.html.replace('class="kb-question" data-recall-id="question-0"','class="kb-question" open data-recall-id="question-0"')))
        self.assertTrue(self.errors(self.html.replace('class="kb-question"','class="kb-question" name="shared"')))
        self.assertTrue(self.errors(self.html.replace('data-recall-id="question-1"','data-recall-id="question-0"')))
        self.assertTrue(self.errors(self.html.replace('data-recall-id="question-0"','data-other="question-0"')))

    def test_unfinished_or_unbalanced_content(self):
        self.assertTrue(self.errors(self.html.replace('A familiar model','TODO: add explanation here. A familiar model')))
        self.assertTrue(self.errors(self.html.replace('</article>','')))


def hub_article(item):
    node=item['node'];route=item['route']
    links=''.join(f'<li><a href="#{route}/{n["slug"]}">{n["title"]}</a></li>' for n in node['children'])
    return f'<article class="kb-hub" data-node-id="{node["id"]}"><h1>{node["title"]}</h1><p>Understand the domain through its child capabilities.</p><h2>Roadmap</h2><figure><pre class="mermaid">graph TD\n A --> B</pre></figure><h2>Suggested reading</h2><p>Start with the first capability and compare the alternatives.</p><ul data-child-links>{links}</ul></article>'


class HubTests(FixtureBase):
    def setUp(self):
        super().setUp();self.index=vc.index_manifest(self.data,self.root)
        self.item=self.index['/domain'];self.html=hub_article(self.item)

    def errors(self,html):return vc.check_article(self.item,html,self.index)

    def test_valid_hub(self):self.assertEqual(self.errors(self.html),[])

    def test_missing_roadmap(self):self.assertTrue(self.errors(self.html.replace('class="mermaid"','class="other"')))

    def test_missing_intro_or_guidance(self):
        self.assertTrue(self.errors(self.html.replace('Understand the domain through its child capabilities.','')))
        self.assertTrue(self.errors(self.html.replace('Start with the first capability and compare the alternatives.','')))

    def test_missing_child_list_or_duplicate_link(self):
        self.assertTrue(self.errors(self.html.replace('data-child-links','data-other')))
        self.assertTrue(self.errors(self.html.replace('</ul>','<li><a href="#/domain/example">Example</a></li></ul>')))

    def test_child_order_and_unknown_route(self):
        data=catalog(hub([topic('first'),topic('second')]))
        index=vc.index_manifest(data,self.root);item=index['/domain'];source=hub_article(item)
        bad=source.replace('#/domain/first','#/domain/TEMP').replace('#/domain/second','#/domain/first').replace('#/domain/TEMP','#/domain/second')
        self.assertTrue(vc.check_article(item,bad,index))
        self.assertTrue(self.errors(self.html.replace('#/domain/example','#/unknown')))

    def test_section_link_grammar(self):
        for href in ['#mechanics','#/domain/example?section=unknown','#/domain?section=mechanics','#/domain/example?section=mechanics&section=mastery']:
            with self.subTest(href=href):
                self.assertTrue(self.errors(self.html.replace('</article>',f'<a href="{href}">More</a></article>')))
        self.assertEqual(self.errors(self.html.replace('</article>','<a href="#/domain/example?section=mechanics">Mechanics</a></article>')),[])

    def test_source_link_scheme(self):
        self.assertTrue(self.errors(self.html.replace('</article>','<a href="javascript:alert(1)">Source</a></article>')))

    def test_missing_partial_report(self):
        expected={'profile':'small','root':{'title':'Domain','slug':'domain'},'parent':{'title':'Example parent','slug':'parent'},'groups':[]}
        data=catalog(hub([hub([topic()],slug='parent')]))
        data['roots'][0]['children'][0]['title']='Example parent'
        (self.root/'manifest.json').write_text(json.dumps(data))
        result=vc.validate(self.root,expected)
        self.assertEqual(result['result'],'fail')
        self.assertTrue(any('missing' in c['message'].lower() for c in result['checks']))


class HistoryAndReportTests(FixtureBase):
    def setUp(self):
        super().setUp()
        parent=hub([topic()],slug='parent');parent['title']='Parent'
        self.data=catalog(hub([parent]))
        self.expected={'profile':'test','root':{'title':'Domain','slug':'domain'},'parent':{'title':'Parent','slug':'parent'},'groups':[],'deliveryRecord':'delivery.md'}
        self.baseline=copy.deepcopy(self.data)
        (self.root/'delivery.md').write_text('Complete fixture bundle. Actual host integration and novice review remain pending.')
        self.materialize()

    def materialize(self):
        for file in self.root.glob('topics/**/*.html'): file.unlink()
        (self.root/'manifest.json').write_text(json.dumps(self.data))
        for item in vc.index_manifest(self.data,self.root,baseline=self.baseline).values():
            item['path'].parent.mkdir(parents=True,exist_ok=True)
            item['path'].write_text(hub_article(item) if item['node']['kind']=='hub' else article(item))

    def result(self):return vc.validate(self.root,self.expected,self.baseline)

    def history_fail(self):
        result=self.result();self.assertEqual(result['result'],'fail')
        self.assertTrue(any(c['name']=='history' and c['status']=='fail' for c in result['checks']),result)

    def test_identical_baseline_passes(self):
        result=self.result();self.assertEqual(result['result'],'pass',result)
        self.assertEqual(next(c for c in result['checks'] if c['name']=='history')['status'],'pass')

    def test_replaced_or_dropped_id_is_rejected(self):
        self.data['roots'][0]['children'][0]['children'][0]['id']=str(uuid.uuid4())
        self.materialize();self.history_fail()

    def test_node_kind_cannot_silently_change(self):
        leaf=self.data['roots'][0]['children'][0]['children'][0]
        leaf['kind']='hub';leaf['children']=[topic('child')]
        self.materialize();self.history_fail()

    def test_unrelated_optional_metadata_is_preserved(self):
        self.baseline['roots'][0]['custom']={'keep':['original']}
        self.data['roots'][0]['custom']={'keep':['changed']}
        self.materialize();self.history_fail()

    def test_rename_move_retains_identity_and_repairs_links(self):
        parent=self.data['roots'][0]['children'][0]
        leaf=parent['children'][0];identity=leaf['id']
        leaf['title']='Renamed example';leaf['slug']='renamed-example'
        parent['children']=[hub([leaf],slug='archive')]
        self.materialize();result=self.result()
        self.assertEqual(result['result'],'pass',result)
        self.assertEqual(vc.index_manifest(self.data,self.root,baseline=self.baseline)['/domain/parent/archive/renamed-example']['node']['id'],identity)

    def test_missing_delivery_record_is_failure(self):
        (self.root/'delivery.md').unlink();result=self.result()
        self.assertEqual(result['result'],'fail')
        self.assertTrue(any(c['name']=='bundle' and c['status']=='fail' for c in result['checks']))

    def test_orphan_partial_is_rejected(self):
        (self.root/'topics/orphan.html').write_text('<article>Unregistered</article>')
        result=self.result();self.assertEqual(result['result'],'fail')
        self.assertTrue(any(c['name']=='files' and c['status']=='fail' for c in result['checks']))

    def test_report_keeps_unexecuted_tiers_pending(self):
        result=self.result();self.assertEqual(result['result'],'pass',result)
        self.assertEqual(result['phase'],'intrinsic');self.assertEqual(result['integrationStatus'],'pending')
        self.assertTrue(all(set(c)=={'name','status','artifact','message'} for c in result['checks']))
        no_baseline=vc.validate(self.root,self.expected)
        self.assertEqual(next(c for c in no_baseline['checks'] if c['name']=='history')['status'],'pending')

    def test_full_cli_exit_zero_and_one_and_report_directory(self):
        expected=self.root/'expected.json';expected.write_text(json.dumps(self.expected))
        report=self.root/'reports/output.json'
        command=[sys.executable,str(Path(vc.__file__)),'--repo-root',str(self.root),'--expect',str(expected),'--report',str(report)]
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(json.loads(report.read_text())['result'],'pass')
        (self.root/'topics/domain/parent/example.html').unlink()
        self.assertEqual(subprocess.run(command,capture_output=True,text=True).returncode,1)
