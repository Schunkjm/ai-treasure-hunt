import json
import shutil
import unittest
import uuid
from pathlib import Path
from src.release_integrity import ROOT, verify_runtime

class ReleaseTests(unittest.TestCase):
    def test_no_archive_checkout_and_required_code_tampering(self):
        parent=ROOT/'.release_check';parent.mkdir(exist_ok=True)
        root=parent/uuid.uuid4().hex;root.mkdir()
        try:
            lock=json.loads((ROOT/'FROZEN_LOCK.json').read_text())
            public=ROOT/'PUBLIC_RUNTIME_LOCK.json'
            names=['FROZEN_LOCK.json',*[n for n in lock['sha256'] if not n.startswith(('data/','reference/'))]]
            if public.exists(): names=['PUBLIC_RUNTIME_LOCK.json',*json.loads(public.read_text())['sha256']]
            for name in names:
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
            self.assertGreater(verify_runtime(root)['missing_archive_files'],0)
            (root/'src/signals.py').write_text('changed')
            with self.assertRaisesRegex(ValueError,'Frozen file'): verify_runtime(root)
        finally:
            assert root.resolve().parent==parent.resolve()
            shutil.rmtree(root)

if __name__=='__main__': unittest.main()
