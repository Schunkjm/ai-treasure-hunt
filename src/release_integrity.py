"""Verify shipped frozen methodology without requiring unpublished vendor data."""
import hashlib
import json
from pathlib import Path
from . import config
from .frozen import specification_settings

ROOT = Path(__file__).resolve().parents[1]

def verify_runtime(root=ROOT):
    actual=json.loads(json.dumps({k:v for k,v in vars(config).items() if k.isupper()}))
    if specification_settings(root)!=actual:
        raise ValueError('Runtime settings differ from frozen specification')
    lock=json.loads((root/'FROZEN_LOCK.json').read_text())
    public_lock_path=root/'PUBLIC_RUNTIME_LOCK.json'
    public_lock=json.loads(public_lock_path.read_text()) if public_lock_path.exists() else None
    if public_lock:
        for name, expected in public_lock['sha256'].items():
            path=root/name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise ValueError(f'Frozen file changed or missing in public export: {name}')
    missing_archive=0
    for name,expected in lock['sha256'].items():
        path=root/name
        if name in {'reference/sectors.csv','reference/data_corrections.json'}:
            continue
        if public_lock and name in public_lock['public_document_exceptions']:
            continue
        if name.startswith('data/') and not path.exists():
            missing_archive+=1
            continue
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Frozen file changed or missing: {name}')
    return {'missing_archive_files':missing_archive,'methodology_verified':True}

if __name__=='__main__': print(json.dumps(verify_runtime(),indent=2))
