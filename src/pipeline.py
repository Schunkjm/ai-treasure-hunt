"""Acquire, validate, and label; deliberately no return-summary operation."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import time

import numpy as np
import pandas as pd
import yfinance as yf

from . import config
from .data import adjust_ohlc, apply_corrections, expected_sessions, validate_frame, OHLC
from .frozen import verify_freeze, load_sectors
from .signals import generate_signals
from .outcomes import forward_outcomes

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def acquire(snapshot):
    # yfinance's incidental cookie/timezone cache is not a research database.
    cache = ROOT / ".cache" / "yfinance"
    cache.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(cache))
    failures = {}
    for ticker in (*config.UNIVERSE, config.BENCHMARK):
        target = snapshot / "vendor" / f"{ticker}.csv"
        if target.exists():
            continue  # Resume only; never silently replace a saved response.
        success = False
        last_error = "empty_response"
        for attempt in range(2):
            try:
                raw = yf.Ticker(ticker).history(
                    start=config.HISTORY_START, end=config.DOWNLOAD_END_EXCLUSIVE,
                    **config.DATA_SETTINGS, raise_errors=True, timeout=15,
                )
                if raw.empty:
                    raise ValueError("Empty response")
                # Keep local exchange session date; do not shift it to UTC.
                if raw.index.tz is not None:
                    raw.index = raw.index.tz_localize(None)
                raw.index = raw.index.normalize().rename("Date")
                required = {*OHLC, "Adj Close", "Volume"}
                if not required.issubset(raw.columns):
                    raise ValueError("Missing required columns")
                target.parent.mkdir(parents=True, exist_ok=True)
                raw.to_csv(target)
                write_json(snapshot / "retrieval" / f"{ticker}.json", {
                    "ticker": ticker, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                    "sha256": digest(target), "attempts": attempt + 1,
                })
                success = True
                print(f"Downloaded {ticker}", flush=True)
                break
            except Exception as exc:
                # Avoid exposing cookies, URLs with tokens, or local paths.
                last_error = type(exc).__name__
                time.sleep(0.5)
        if not success:
            failures[ticker] = last_error
            print(f"Download failed: {ticker} ({last_error})", flush=True)
            # Systemic network failure: stop early rather than repeat 51 times.
            if len(failures) >= 3:
                break
    write_json(snapshot / "download_failures.json", failures)
    return failures


def build(snapshot, output):
    verify_freeze()
    if snapshot.resolve() != (ROOT / "data" / "snapshot_2026-09-08").resolve():
        raise ValueError("Frozen build requires the locked original snapshot")
    sectors = load_sectors()
    corrections = json.loads((ROOT / "reference" / "data_corrections.json").read_text())["corrections"]
    if (output / "manifest.json").exists():
        raise RuntimeError("Completed output exists; choose a new output folder")
    sessions = expected_sessions()
    frames, quality = {}, {}
    missing_tickers = []
    for ticker in (*config.UNIVERSE, config.BENCHMARK):
        path = snapshot / "vendor" / f"{ticker}.csv"
        if not path.exists():
            missing_tickers.append(ticker)
            continue
        raw = pd.read_csv(path, index_col="Date", parse_dates=True)
        raw_quality = validate_frame(raw, sessions)
        corrected = apply_corrections(raw, ticker, corrections)
        corrected_quality = validate_frame(corrected, sessions)
        adjusted = adjust_ohlc(corrected)
        item = validate_frame(adjusted, sessions)
        item["vendor_validation"] = raw_quality
        item["corrected_validation"] = corrected_quality
        item["corrections_applied"] = [c for c in corrections if c["ticker"] == ticker]
        factor = adjusted.adjustment_factor
        item["invalid_adjustment_factors"] = int((~np.isfinite(factor) | (factor <= 0)).sum())
        quality[ticker] = item
        # Preserve the vendor response; quarantine inconsistent bars rather
        # than guessing corrected prices or silently dropping a ticker/date.
        quarantine = sorted(set(item["invalid_dates"] + corrected_quality["invalid_dates"]))
        item["quarantined_dates"] = quarantine
        adjusted.loc[pd.to_datetime(quarantine), OHLC + ["Volume"]] = np.nan
        frames[ticker] = adjusted
    report = {"requested_stocks": len(config.UNIVERSE), "requested_benchmark": config.BENCHMARK,
              "downloaded_instruments": len(frames), "missing_tickers": missing_tickers,
              "expected_sessions": len(sessions), "tickers": quality}
    write_json(output / "data_quality.json", report)
    bad = missing_tickers or any(
        q["duplicate_dates"] or q["extra_dates"]
        for q in quality.values()
    )
    if bad:
        raise RuntimeError("Data-quality gate failed; inspect data_quality.json (no outcomes generated)")
    # Explicit reindex even after exact-calendar validation.
    frames = {k: v.reindex(sessions) for k, v in frames.items()}
    evaluation = sessions >= pd.Timestamp(config.EVALUATION_START)
    checks = {"v1_subset_v0": True, "prefix_invariance": True,
              "outcome_isolation": True, "warmup_complete": True,
              "identical_endpoint_dates": True, "ten_intervals": True}
    has_excluded_v0 = False
    for ticker in config.UNIVERSE:
        frame = frames[ticker]
        signals = generate_signals(frame)
        if not signals.loc[evaluation, ["sma20", "atr14", "prior20_atr_pct_max"]].iloc[0].notna().all():
            raise RuntimeError(f"Insufficient warm-up: {ticker}")
        assert not (signals.v1.fillna(False) & ~signals.v0.fillna(False)).any()
        has_excluded_v0 |= bool((evaluation & signals.v0.fillna(False) & signals.v1.eq(False).fillna(False)).any())
        # Check causal prefix behavior on real indicator data, not returns.
        for length in (35, len(frame) // 2, len(frame) - 11):
            pd.testing.assert_frame_equal(generate_signals(frame.iloc[:length]), signals.iloc[:length])
        contaminated = frame.assign(forward_10d_excess_return=999.0, exit_date="irrelevant")
        contaminated["sector"] = "diagnostic_metadata_must_not_affect_signals"
        pd.testing.assert_frame_equal(generate_signals(contaminated), signals)
        outcomes = forward_outcomes(frame.Open, frames[config.BENCHMARK].Open)
        mature = outcomes.exit_date.notna()
        entry_pos = sessions.get_indexer(pd.DatetimeIndex(outcomes.loc[mature, "entry_date"]))
        exit_pos = sessions.get_indexer(pd.DatetimeIndex(outcomes.loc[mature, "exit_date"]))
        assert (exit_pos - entry_pos == config.HORIZON).all()
        assert (entry_pos == np.flatnonzero(mature) + 1).all()
        for folder in ("signals", "outcomes", "events"):
            (output / folder).mkdir(parents=True, exist_ok=True)
        signals.loc[evaluation].to_csv(output / "signals" / f"{ticker}.csv")
        # Label tables include non-events but never feed the signal module.
        outcomes.loc[evaluation].to_csv(output / "outcomes" / f"{ticker}.csv")
        events = signals.join(outcomes).loc[evaluation & signals.v0.fillna(False)]
        events["sector"] = sectors[ticker]  # Diagnostic label attached AFTER signals and labels.
        events.to_csv(output / "events" / f"{ticker}.csv")
        # Never display/aggregate historical return values or compare V0/V1.
    for ticker, frame in frames.items():
        target = output / "adjusted" / f"{ticker}.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(target)
    report["usable_stocks"] = len(config.UNIVERSE)
    report["benchmark_valid"] = True
    report["complete_instruments"] = sum(not q["missing_dates"] and not q["quarantined_dates"] for q in quality.values())
    report["data_exceptions_require_review"] = report["complete_instruments"] != len(frames)
    report["checks"] = checks
    report["performance_examined"] = False
    checks["v1_proper_subset_v0"] = bool(has_excluded_v0)
    if not has_excluded_v0:
        raise RuntimeError("V1 did not exclude any observed V0 event; report before comparison")
    checks["sector_isolation"] = True
    checks["frozen_specification_matches"] = True
    write_json(output / "data_quality.json", report)
    code_files = sorted((ROOT / "src").glob("*.py")) + sorted((ROOT / "tests").glob("*.py")) + [ROOT / "requirements.txt", ROOT / "FROZEN_SPECIFICATION.md", ROOT / "FROZEN_LOCK.json"] + sorted((ROOT / "reference").glob("*"))
    hashes = {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p) for p in code_files}
    snapshot_hashes = {str(p.relative_to(snapshot)).replace("\\", "/"): digest(p) for p in sorted(snapshot.rglob("*.csv"))}
    output_hashes = {str(p.relative_to(output)).replace("\\", "/"): digest(p) for p in sorted(output.rglob("*.csv"))}
    write_json(output / "manifest.json", {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "versions": {name: importlib.metadata.version(name) for name in ("yfinance", "pandas", "numpy")},
        "configuration": {k: v for k, v in vars(config).items() if k.isupper()},
        "source_sha256": hashes, "data_sha256": snapshot_hashes, "output_sha256": output_hashes,
        "performance_examined": False,
    })
    print(json.dumps({"usable_stocks": len(config.UNIVERSE), "benchmark": "SPY",
                      "sessions": len(sessions), "checks": checks, "performance_examined": False}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Acquire/resume the frozen snapshot")
    parser.add_argument("--snapshot", default="data/snapshot_2026-09-08")
    parser.add_argument("--output", default="output/pipeline_2026-09-08")
    args = parser.parse_args()
    if args.download and (ROOT / "FROZEN_LOCK.json").exists():
        raise RuntimeError("Frozen snapshot cannot be refreshed; rebuild without --download")
    snapshot, output = ROOT / args.snapshot, ROOT / args.output
    if (output / "manifest.json").exists():
        raise RuntimeError("Completed output exists; choose a new output folder")
    snapshot.mkdir(parents=True, exist_ok=True)
    if args.download:
        acquire(snapshot)
    build(snapshot, output)


if __name__ == "__main__":
    main()
