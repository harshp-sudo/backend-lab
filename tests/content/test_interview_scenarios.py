"""Current-profile rejection and migration preservation tests; no editorial shortcuts."""
import copy
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import validate_content as vc
from test_validate_content import FixtureBase, article, interview_section


class ScenarioStructureTests(FixtureBase):
    def setUp(self):
        super().setUp()
        self.index = vc.index_manifest(self.data, self.root)
        self.item = self.index['/domain/example']
        self.html = article(self.item)

    def errors(self, html, **kwargs):
        return vc.check_article(self.item, html, self.index, **kwargs)

    def test_current_positive_and_bounds(self):
        for count in [5, 7]:
            source = self.html.replace(interview_section(self.item['node']['id']), interview_section(self.item['node']['id'], count))
            self.assertEqual(self.errors(source), [])

    def test_explicit_legacy_unit_fixture_only(self):
        old = article(self.item, legacy=True)
        self.assertTrue(self.errors(old))
        self.assertEqual(self.errors(old, recall_profile='legacy-1.1'), [])
        self.assertTrue(self.errors(self.html, recall_profile='unknown'))

    def test_no_total_count_waiver(self):
        old = article(self.item, legacy=True)
        self.assertTrue(self.errors(old))
        source = self.html.replace('class="kb-question" data-recall-id="question-', 'class="other" data-recall-id="question-')
        self.assertTrue(self.errors(source))

    def test_interview_count_bounds(self):
        for count in [0, 4, 8]:
            with self.subTest(count=count):
                source = self.html.replace(interview_section(self.item['node']['id']), interview_section(self.item['node']['id'], count))
                self.assertTrue(self.errors(source))

    def test_heading_wrapper_and_markers(self):
        for old, new in [('data-interview-scenarios', 'data-other'),
                         ('Tricky &amp; Most-Asked Interview Scenarios', 'Interview questions'),
                         ('<h3 ', '<h4 '),
                         ('<!-- kb-interview-scenarios:start -->', ''),
                         ('<!-- kb-interview-scenarios:end -->', '')]:
            with self.subTest(old=old): self.assertTrue(self.errors(self.html.replace(old, new)))
        block = interview_section(self.item['node']['id'])
        self.assertTrue(self.errors(self.html.replace(block, block + block)))

    def test_role_placement_and_basis(self):
        for old, new in [('data-recall-kind="interview"', 'data-recall-kind="other"'),
                         ('data-recall-kind="interview"', ''),
                         ('data-scenario-basis="adapted-production"', 'data-scenario-basis="guessed"'),
                         ('data-recall-id="interview-fixture-0"', 'data-recall-id="question-0"'),
                         ('data-recall-id="interview-fixture-0"', 'data-recall-id="unstable"')]:
            with self.subTest(old=old, new=new): self.assertTrue(self.errors(self.html.replace(old, new)))
        block = interview_section(self.item['node']['id'])
        self.assertTrue(self.errors(self.html.replace(block, '').replace('</article>', block+'</article>')))

    def test_answer_parts_and_labels(self):
        for old, new in [('data-scenario-part="decision"', 'data-scenario-part="scenario"'),
                         ('data-scenario-part="decision"', 'data-scenario-part="missing"'),
                         ('The Direct Answer &amp; Architectural Decision', 'Answer'),
                         ('Fixture prose supplies a concrete decision and its bounded assumptions.', '')]:
            with self.subTest(old=old): self.assertTrue(self.errors(self.html.replace(old, new)))
        self.assertTrue(self.errors(self.html.replace('data-scenario-part="scenario"','data-scenario-part="TEMP"').replace('data-scenario-part="decision"','data-scenario-part="scenario"').replace('data-scenario-part="TEMP"','data-scenario-part="decision"')))

    def test_disclosures_and_source_note(self):
        for old, new in [('<details class="kb-question" data-recall-kind', '<details open class="kb-question" data-recall-kind'),
                         ('data-recall-kind="interview"', 'name="exclusive" data-recall-kind="interview"'),
                         ('data-interview-research', 'data-other'),
                         ('https://example.com/source', 'http://example.com/source')]:
            with self.subTest(old=old): self.assertTrue(self.errors(self.html.replace(old, new)))
        self.assertTrue(self.errors(self.html.replace('Production request 0 times out: what will you do and why?', '')))

    def test_foundational_bounds_and_ddd_fifth_card(self):
        card=re.search(r'<details class="kb-question" data-recall-id="question-0">.*?</details>',self.html,re.S)[0]
        five=self.html.replace(card,card+card.replace('question-0','question-3')+card.replace('question-0','question-4'))
        self.assertEqual(self.errors(five),[])
        self.assertTrue(self.errors(five.replace(card,card+card.replace('question-0','question-5'))))
        self.assertTrue(self.errors(self.html.replace(card,'')))

    def test_multiple_summary_nested_recall_and_hidden_note(self):
        for old,new in [('<summary>Production request 0','<summary>Extra prompt</summary><summary>Production request 0'),
                        ('data-interview-research','hidden data-interview-research'),
                        ('<div data-scenario-part="decision">','<details class="kb-question" data-recall-id="interview-nested"><summary>Nested</summary><p>Answer</p></details><div data-scenario-part="decision">')]:
            with self.subTest(old=old):self.assertTrue(self.errors(self.html.replace(old,new)))


class PreservationTests(unittest.TestCase):


    def test_protected_drift_and_changed_allocated_key(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); data={'schemaVersion':1,'roots':[]}
            from test_validate_content import catalog
            index=vc.index_manifest(catalog(),root);item=index['/domain/example']
            old=article(item,legacy=True);source=article(item)
            inventory=vc.article_inventory(source)
            frozen={'id':item['node']['id'],'title':item['node']['title'],'path':item['relative_path'],'route':item['route'],
                    'sourceSha256':vc.sha256(old.encode()),'foundationalRecall':[{'key':k} for k in inventory['foundationalKeys']]}
            # Removing the test factory's insertion exactly reconstructs its legacy source.
            self.assertEqual(vc.strip_interview_block(source),old)
            record={'topicId':frozen['id'],'path':frozen['path'],'scenarios':[{'key':k} for k in inventory['interviewKeys']]}
            research=root/'research';research.mkdir();(research/'example.md').write_text('```json\n'+json.dumps(record)+'\n```')
            entry={'topicId':frozen['id'],'path':frozen['path'],'foundationalKeys':inventory['foundationalKeys'],'interviewKeys':inventory['interviewKeys'],'checks':{k:{'status':'pending'} for k in ['preservation','structure','editorial','browser','print']},'status':'pending'}
            def errors(html, e=entry):
                return vc.check_migration_lesson(item,html,{'lessons':[frozen]},{'lessons':[e]},{'scenarioResearchDirectory':research},root)
            self.assertEqual(errors(source),[])
            for old_text,new_text in [('A familiar model','A rewritten model'),('It makes the decision explicit.','An edited original answer.'),('https://example.com/source','https://example.com/changed')]:
                with self.subTest(text=old_text):self.assertTrue(errors(source.replace(old_text,new_text)))
            changed=copy.deepcopy(entry);changed['interviewKeys'][0]='interview-reallocated'
            self.assertTrue(errors(source,changed))

    def test_exact_insertion_and_rerun(self):
        original = 'original\n <footer>preserve every byte</footer>\n'
        block = '<!-- kb-interview-scenarios:start --><section>addition</section><!-- kb-interview-scenarios:end -->'
        migrated = original.replace('<footer>', block + '<footer>')
        self.assertEqual(vc.strip_interview_block(migrated), original)
        self.assertEqual(vc.strip_interview_block(migrated.replace(block, block)), original)
        self.assertNotEqual(hashlib.sha256(vc.strip_interview_block(migrated+' ').encode()).hexdigest(), hashlib.sha256(original.encode()).hexdigest())
        for malformed in [original, migrated+block, migrated.replace('<!-- kb-interview-scenarios:end -->','')]:
            with self.subTest(malformed=malformed):
                with self.assertRaises(vc.ValidationError): vc.strip_interview_block(malformed)

    def test_safe_reference_paths(self):
        root=Path(__file__).resolve().parents[2]
        for value in ['../outside', '/etc/passwd', 'https://example.com/file']:
            with self.subTest(value=value):
                with self.assertRaises(vc.ValidationError): vc.repository_path(root, value)


class ResearchEvidenceTests(FixtureBase):
    def setUp(self):
        super().setUp()
        from test_topic_publishing import research
        self.index=vc.index_manifest(self.data,self.root)
        self.item=self.index['/domain/example']
        self.source=article(self.item)
        self.item['path'].parent.mkdir(parents=True,exist_ok=True)
        self.item['path'].write_text(self.source)
        self.record=research(self.item)
        self.record['constitutionVersion']='1.2.0'

    def test_valid_authored_mapping(self):
        self.assertEqual(vc.check_research(self.record,self.source,self.item),[])

    def test_invalid_research_fields_and_claims(self):
        mutations=[lambda r:r.update(state='approved'),
                   lambda r:r.update(researchedOn='tomorrow'),
                   lambda r:r.update(searches=[]),
                   lambda r:r['sources'].append(copy.deepcopy(r['sources'][0])),
                   lambda r:r['sources'][0].update(url='http://example.com'),
                   lambda r:r['sources'][0].update(checkedOn=None,limitation=''),
                   lambda r:r['scenarios'][0].update(technicalSources=['missing-source']),
                   lambda r:r['scenarios'][0].update(key='interview-reallocated'),
                   lambda r:r['scenarios'][0].update(basis='reported-recurring',supportedInterviewClaim='most asked at a company'),
                   lambda r:r['scenarios'][0].update(basis='knowledge-based'),
                   lambda r:r.update(publicDisclosure='Web search was unavailable.'),
                   lambda r:r['scenarios'][0].update(editorial={})]
        for mutate in mutations:
            record=copy.deepcopy(self.record);mutate(record)
            with self.subTest(record=record.get('state')):
                self.assertTrue(vc.check_research(record,self.source,self.item))

    def test_reviewed_requires_every_editorial_disposition(self):
        record=copy.deepcopy(self.record);record['state']='reviewed'
        record['scenarios'][0]['editorial']['decision-costs']['status']='fail'
        self.assertTrue(vc.check_research(record,self.source,self.item))

    def test_malformed_evidence_rows_return_failures_not_tracebacks(self):
        for field,value in [('scenarios',['bad']*5),('sources',['bad']),('searches',['bad'])]:
            record=copy.deepcopy(self.record);record[field]=value
            with self.subTest(field=field):self.assertTrue(vc.check_research(record,self.source,self.item))


if __name__ == '__main__': unittest.main()
