"""Current source presentation must preserve evidence without public boilerplate."""
import copy
import re
from test_validate_content import FixtureBase, article
from test_topic_publishing import research
from tools import validate_content as vc

def clean(source):
    return re.sub(r'(<aside\b[^>]*data-interview-research[^>]*>)\s*<p>(.*?)</p>',lambda m:m[1]+'<h4>Sources</h4><ul>'+''.join('<li>'+a+'</li>' for a in re.findall(r'<a\b.*?</a>',m[2],re.S))+'</ul>',source,flags=re.S)

class PresentationTests(FixtureBase):
    def setUp(self):
        super().setUp();self.index=vc.index_manifest(self.data,self.root);self.item=self.index['/domain/example']
        self.old=article(self.item);self.html=clean(self.old)
        self.item['path'].parent.mkdir(parents=True,exist_ok=True);self.item['path'].write_text(self.old)
        self.record=research(self.item)

    def errors(self,html=None,record=None):
        html=self.html if html is None else html
        return vc.check_article(self.item,html,self.index,research_presentation='sources-only-v1')+vc.check_research(self.record if record is None else record,html,self.item,constitution_versions=('1.3.0','2.0.0'),research_presentation='sources-only-v1')

    def test_clean_with_archived_evidence(self):
        self.assertEqual(self.errors(),[])

    def test_new_record_without_public_paragraph(self):
        r=copy.deepcopy(self.record);r.pop('publicDisclosure',None);r['constitutionVersion']='2.0.0'
        self.assertEqual(self.errors(record=r),[])

    def test_current_rejects_generic_or_disguised_intro(self):
        for text in ['Researched 2026-11-25. Adapted questions.','The research process produced these examples.','Any other generic introductory prose.']:
            with self.subTest(text=text):self.assertTrue(self.errors(self.html.replace('<h4>Sources</h4>','<h4>Sources</h4><p>'+text+'</p>')))

    def test_current_rejects_missing_hidden_or_nested_sources(self):
        for old,new in [('data-interview-research','data-other'),('<aside','<aside hidden'),('<h4>Sources</h4>',''),('<aside','<details><summary>Sources</summary><aside')]:
            with self.subTest(old=old,new=new):self.assertTrue(self.errors(self.html.replace(old,new)))

    def test_current_rejects_bad_source_and_evidence(self):
        self.assertTrue(self.errors(self.html.replace('https://example.com/source','http://example.com/source')))
        for mutate in [lambda r:r.update(sourceNoteUrls=[]),lambda r:r.update(state='bad'),lambda r:r['scenarios'][0].update(key='interview-wrong'),lambda r:r['scenarios'][0].update(supportedInterviewClaim='Most asked at Company X')]:
            r=copy.deepcopy(self.record);mutate(r);self.assertTrue(self.errors(record=r))

    def test_legacy_disclosure_remains_strict(self):
        self.assertEqual(vc.check_article(self.item,self.old,self.index,research_presentation='disclosure-v1'),[])
        self.assertEqual(vc.check_research(self.record,self.old,self.item,constitution_versions=('1.3.0',),research_presentation='disclosure-v1'),[])
        self.assertTrue(vc.check_research(self.record,self.html,self.item,constitution_versions=('1.3.0',),research_presentation='disclosure-v1'))

    def test_unknown_presentation_rejected(self):
        self.assertTrue(vc.check_article(self.item,self.html,self.index,research_presentation='unknown'))
