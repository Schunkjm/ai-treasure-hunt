"""Read-only enforcement of the human-authorized infrastructure freeze."""
import hashlib
import json
from pathlib import Path
import pandas as pd
from . import config

ROOT = Path(__file__).resolve().parents[1]


def specification_settings(root=ROOT):
    content = (root / "FROZEN_SPECIFICATION.md").read_text(encoding="utf-8")
    return json.loads(content.split("```json\n", 1)[1].split("```", 1)[0])


def load_sectors(root=ROOT):
    sectors = pd.read_csv(root / "reference" / "sectors.csv", keep_default_na=False)
    if sectors.ticker.duplicated().any() or set(sectors.ticker) != set(config.UNIVERSE):
        raise ValueError("Sector mapping must contain each frozen stock exactly once")
    if (sectors.sector == "").any() or (sectors.source_url == "").any():
        raise ValueError("Sector labels require provenance")
    return sectors.set_index("ticker")["sector"]


def verify_freeze(root=ROOT):
    expected = specification_settings(root)
    actual = {k: v for k, v in vars(config).items() if k.isupper()}
    if json.loads(json.dumps(actual)) != expected:
        raise ValueError("Implementation settings differ from frozen specification")
    load_sectors(root)
    lock = json.loads((root / "FROZEN_LOCK.json").read_text(encoding="utf-8"))
    for relative, expected_hash in lock["sha256"].items():
        path = root / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            raise ValueError(f"Frozen file changed or missing: {relative}")
    return True
