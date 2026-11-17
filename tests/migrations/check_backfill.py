"""Explicit integration checks for the frozen 003 migration, not general publishing."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from tools import validate_content as vc


class FrozenBackfillChecks(unittest.TestCase):
    def test_scope_detects_line_ending_only_source_drift(self):
        import tempfile
        import shutil
        root=Path(__file__).resolve().parents[2]
        expected=vc.load_json(root/'tests/content/backend-architecture.json')
        audit=vc.load_json(root/expected['preservationBaseline']);target=audit['lessons'][0]
        record='specs/003-backfill-interview-scenarios/research/'+Path(target['path']).stem+'.md'
        paths=[audit['manifest']['path'],*[e['path'] for e in audit['hubs']],*audit['runtimeFiles'],expected['preservationBaseline'],expected['completionRecord'],expected['deliveryRecord'],target['path'],record]
        if expected.get('runtimeCompatibilityRecord'):paths.append(expected['runtimeCompatibilityRecord'])
        with tempfile.TemporaryDirectory() as directory:
            temporary=Path(directory)
            for path in paths:
                destination=temporary/path;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/path,destination)
            completion=vc.load_json(temporary/expected['completionRecord'])
            for entry in completion['lessons']:
                entry['status']='pending'
                for gate in entry['checks'].values():gate['status']='pending'
            (temporary/expected['completionRecord']).write_text(json.dumps(completion))
            self.assertEqual(vc.validate(temporary,expected,lesson=target['path'])['result'],'pass')
            path=temporary/target['path'];path.write_bytes(path.read_bytes().replace(b'\n',b'\r\n'))
            result=vc.validate(temporary,expected,lesson=target['path'])
            self.assertEqual(result['result'],'fail')
            self.assertTrue(any('Protected original source changed' in c['message'] for c in result['checks']))

    def test_current_scope_is_explicit_and_not_batch(self):
        root=Path(__file__).resolve().parents[2]
        expected=vc.load_json(root/'tests/content/backend-architecture.json')
        target='topics/system-design/backend-architecture/core-system-topologies/distributed-system-fundamentals.html'
        result=vc.validate(root,expected,lesson=target)
        self.assertEqual(result['scope'],'lesson')
        self.assertEqual(result['selectedLesson'],target)
        self.assertEqual(len(result['lessons']),1)
        self.assertEqual(result['integrationStatus'],'pending')

    def test_production_rejects_legacy_expectation(self):
        root=Path(__file__).resolve().parents[2]
        expected=vc.load_json(root/'tests/content/backend-architecture.json')
        expected['recallProfile']='legacy-1.1'
        self.assertEqual(vc.validate(root, expected)['result'], 'fail')

    def test_runtime_exception_cannot_be_omitted_or_substituted(self):
        root=Path(__file__).resolve().parents[2]
        expected=vc.load_json(root/'tests/content/backend-architecture.json')
        if 'runtimeCompatibilityRecord' not in expected:self.skipTest('No runtime exception configured')
        for reference in [None,expected['preservationBaseline']]:
            changed=copy.deepcopy(expected)
            if reference is None:changed.pop('runtimeCompatibilityRecord')
            else:changed['runtimeCompatibilityRecord']=reference
            self.assertEqual(vc.validate(root,changed)['result'],'fail')

    def test_scoped_target_rejects_outside_inventory(self):
        root=Path(__file__).resolve().parents[2]
        expected=vc.load_json(root/'tests/content/backend-architecture.json')
        for path in ['../manifest.json','manifest.json','topics/system-design/_overview.html','/etc/passwd']:
            with self.subTest(path=path):
                self.assertEqual(vc.validate(root, expected, lesson=path)['result'], 'fail')



if __name__ == "__main__": unittest.main()
