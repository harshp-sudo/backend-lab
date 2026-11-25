"""Narrow copy changes must leave technical prose and reference identities intact."""
import unittest
import tempfile
import json
from pathlib import Path
from tools import migrate_lesson_presentation as migration

NOTE='Researched 2026-11-25. Adapted production scenarios; frequency unverified.'
class CopyMigrationTests(unittest.TestCase):
    def source(self,footer=''):
        return '<article><p>Measured 2026-11-25: the research database uses 20 connections.</p><details data-recall-id="stable"><summary>Why?</summary><p>Complete answer.</p></details><aside data-interview-research><p>'+NOTE+'</p><ul><li><a href="https://example.com/a">Primary A</a></li></ul></aside>'+footer+'</article>'

    def test_narrow_and_idempotent(self):
        old=self.source();new=migration.transform(old,{NOTE},'sources')
        self.assertNotIn(NOTE,new);self.assertIn('<h4>Sources</h4>',new)
        self.assertEqual(old.replace('<p>'+NOTE+'</p>','<h4>Sources</h4>'),new)
        self.assertEqual(migration.transform(new,{NOTE},'sources'),new)

    def test_scope_composition_and_meaningful_footer(self):
        footer='<footer class="kb-references"><p>Service discovery and mesh have different duties.</p><p>Continue by comparing the related decisions:</p><ul><li><a href="#/domain/topic">Next</a></li></ul></footer>'
        old=self.source(footer);first=migration.transform(old,{NOTE},'sources');new=migration.transform(first,{NOTE},'related')
        self.assertEqual(new,migration.transform(old,{NOTE},'all'));self.assertIn('different duties.',new)
        self.assertIn('<h4>Related topics</h4>',new)

    def test_external_footer_untouched(self):
        footer='<footer><h2>Sources and further reading</h2><a href="https://example.com/ref">Read</a></footer>'
        self.assertIn(footer,migration.transform(self.source(footer),{NOTE},'all'))

    def test_unknown_or_malformed_note_rejected(self):
        for source in [self.source().replace(NOTE,'Unexpected research prose'),self.source().replace('<p>'+NOTE+'</p>','<div><p>'+NOTE+'</p></div>'),self.source().replace('</aside>','</aside><aside data-interview-research></aside>')]:
            with self.subTest(source=source):
                with self.assertRaises(ValueError):migration.transform(source,{NOTE},'sources')

    def test_inline_reference_survives(self):
        source='<article><aside data-interview-research><p>'+NOTE+'<a href="https://example.com/a">Primary A</a></p></aside></article>'
        variants={migration.parse(source).root.all('p')[0].text()}
        self.assertIn('<a href="https://example.com/a">Primary A</a>',migration.transform(source,variants,'all'))

    def test_dry_run_snapshot_and_tamper_detection(self):
        from test_topic_publishing import write_catalog
        from test_validate_content import catalog,article
        from tools import validate_content as vc
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);index=write_catalog(root,catalog());item=index['/domain/example']
            # Use the original disclosure fixture to exercise a real copy migration.
            item['path'].write_text(article(item));(root/'assets/js').mkdir(parents=True);(root/'assets/js/learning-state.js').write_text('unchanged state')
            (root/'tests/content').mkdir(parents=True);(root/'tests/content/publishing.json').write_text(json.dumps({'researchRecords':{}}))
            baseline=root/'snapshot';before=item['path'].read_bytes();preview=migration.run(root,baseline)
            self.assertEqual(item['path'].read_bytes(),before);self.assertEqual(len(preview['changed']),1)
            frozen=(baseline/'files'/item['relative_path']).read_bytes();migration.run(root,baseline,apply=True)
            self.assertEqual(migration.run(root,baseline,apply=True)['changed'],[])
            self.assertEqual((baseline/'files'/item['relative_path']).read_bytes(),frozen)
            self.assertEqual(migration.run(root,baseline,verify=True)['result'],'pass')
            item['path'].write_text(item['path'].read_text().replace('The input becomes a validated result.','Truncated!'))
            with self.assertRaisesRegex(ValueError,'Unexpected content change'):migration.run(root,baseline,verify=True)
