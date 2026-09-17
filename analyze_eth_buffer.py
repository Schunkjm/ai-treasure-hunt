#!/usr/bin/env python3
"""
ETH 200-DMA Buffer Experiment
AI Treasure Hunt — first approved experiment

LOCKED DEFINITIONS (do not change after looking at percentiles):
1. Price series: daily ETH-USD close via yfinance ticker "ETH-USD".
   Crypto trades 7d/week; we use calendar daily bars as returned by Yahoo.
2. 200-day MA: simple moving average of daily Close over 200 calendar days
   (min_periods=200). Consistent with daily crypto bars.
3. Uptrend regime: consecutive days where Close > 200-day MA.
   Regimes shorter than 30 days are EXCLUDED from dip sampling (noise filter).
4. Recent high: within each regime, running maximum Close since regime start
   (inclusive).
5. Dip observation (daily): drawdown_pct = (running_peak - close) / running_peak * 100.
6. Dip episode (PRIMARY for 80% rule): within a regime, a dip episode starts
   when close falls below the running peak and ends when price makes a new
   regime peak OR the regime ends. For each completed episode, record
   max_drawdown_pct during the episode. Episodes with max_dd == 0 are not
   emitted (only days below peak start an episode).
7. Buffer = 80th percentile of episode max_drawdown_pct on the TRAIN set.
8. Holdout: chronological — train on regimes that END before 2024-01-01;
   test on regimes that START on/after 2024-01-01. If holdout has fewer than
   5 episodes, fall back to last 20% of calendar time and document.

No live trading. No optimization. No peeking at holdout to choose buffer.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent
MIN_REGIME_DAYS = 30
HOLDOUT_START = pd.Timestamp("2024-01-01")
BUFFER_PCTILE = 80.0


def fetch_eth() -> pd.DataFrame:
    import yfinance as yf

    # Max history available from Yahoo for ETH-USD
    t = yf.Ticker("ETH-USD")
    df = t.history(period="max", auto_adjust=True)
    if df is None or df.empty:
        raise RuntimeError("yfinance returned empty data for ETH-USD")
    df = df.reset_index()
    # Normalize timezone-aware index/dates to naive UTC dates for consistency
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None).dt.normalize()
    else:
        raise RuntimeError(f"Unexpected columns: {df.columns.tolist()}")
    df = df[["Date", "Close"]].dropna()
    df = df.sort_values("Date").drop_duplicates("Date").reset_index(drop=True)
    df["Close"] = df["Close"].astype(float)
    return df


def add_ma_and_regime(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ma200"] = out["Close"].rolling(window=200, min_periods=200).mean()
    out["above_ma"] = out["Close"] > out["ma200"]
    # Regime id: increment whenever above_ma flips
    # Only assign regime ids while above_ma is True
    flip = out["above_ma"] != out["above_ma"].shift(1)
    out["segment"] = flip.cumsum()
    out["regime_id"] = np.where(out["above_ma"], out["segment"], np.nan)
    # Remap regime ids to dense integers for readability
    valid = out["regime_id"].dropna().unique()
    mapping = {old: i for i, old in enumerate(sorted(valid))}
    out["regime_id"] = out["regime_id"].map(mapping)
    return out


def extract_regimes(df: pd.DataFrame) -> list[dict]:
    regimes = []
    for rid, g in df.dropna(subset=["regime_id"]).groupby("regime_id"):
        g = g.sort_values("Date")
        start = g["Date"].iloc[0]
        end = g["Date"].iloc[-1]
        n = len(g)
        regimes.append(
            {
                "regime_id": int(rid),
                "start": start,
                "end": end,
                "n_days": n,
                "include": n >= MIN_REGIME_DAYS,
            }
        )
    return regimes


def episodes_for_regime(g: pd.DataFrame) -> list[dict]:
    """
    Within a regime (sorted by Date), track running peak and emit dip episodes.
    Episode starts when close < running_peak (after peak has been set).
    Ends when a new peak is made OR regime ends.
    Record max_drawdown_pct over the episode.
    """
    g = g.sort_values("Date").reset_index(drop=True)
    episodes = []
    running_peak = None
    in_dip = False
    ep_max_dd = 0.0
    ep_start = None
    ep_peak_at_start = None
    daily_dds = []

    for i, row in g.iterrows():
        close = float(row["Close"])
        date = row["Date"]
        if running_peak is None:
            running_peak = close
            daily_dds.append(0.0)
            continue

        if close > running_peak:
            # New peak — close any open dip episode
            if in_dip:
                episodes.append(
                    {
                        "start": ep_start,
                        "end": date,  # ends on the day of new peak
                        "max_drawdown_pct": ep_max_dd,
                        "peak_at_start": ep_peak_at_start,
                        "ended_by": "new_peak",
                    }
                )
                in_dip = False
                ep_max_dd = 0.0
                ep_start = None
                ep_peak_at_start = None
            running_peak = close
            daily_dds.append(0.0)
        else:
            dd = (running_peak - close) / running_peak * 100.0
            daily_dds.append(dd)
            if not in_dip:
                in_dip = True
                ep_start = date
                ep_peak_at_start = running_peak
                ep_max_dd = dd
            else:
                ep_max_dd = max(ep_max_dd, dd)

    # Regime ends — close open dip
    if in_dip:
        episodes.append(
            {
                "start": ep_start,
                "end": g["Date"].iloc[-1],
                "max_drawdown_pct": ep_max_dd,
                "peak_at_start": ep_peak_at_start,
                "ended_by": "regime_end",
            }
        )

    return episodes, daily_dds, float(g["Close"].max()), float(
        (g["Close"].cummax().iloc[-1] - g["Close"].min()) / g["Close"].cummax().max() * 100
        if False
        else np.nan
    )


def per_regime_max_dd(g: pd.DataFrame) -> float:
    """Max drawdown from running peak within the regime."""
    peak = g["Close"].cummax()
    dd = (peak - g["Close"]) / peak * 100.0
    return float(dd.max())


def main() -> int:
    print("Fetching ETH-USD from yfinance...")
    try:
        df = fetch_eth()
    except Exception as e:
        print(f"DATA FETCH FAILED: {e}", file=sys.stderr)
        report = OUT_DIR / "REPORT.md"
        report.write_text(
            f"# ETH 200-DMA Buffer Experiment — FAILED\n\n"
            f"Could not fetch ETH-USD prices: `{e}`\n\n"
            f"No invented prices. Re-run when data source is available.\n"
        )
        return 1

    print(f"Fetched {len(df)} daily bars: {df['Date'].min().date()} → {df['Date'].max().date()}")

    df = add_ma_and_regime(df)
    usable = df.dropna(subset=["ma200"])
    print(f"After 200-day MA warmup: {len(usable)} days "
          f"({usable['Date'].min().date()} → {usable['Date'].max().date()})")

    regimes_meta = extract_regimes(df)
    included = [r for r in regimes_meta if r["include"]]
    excluded = [r for r in regimes_meta if not r["include"]]
    print(f"Regimes total: {len(regimes_meta)}; "
          f">={MIN_REGIME_DAYS}d included: {len(included)}; "
          f"short excluded: {len(excluded)}")

    # Build episode table
    rows = []
    daily_rows = []
    regime_max_rows = []

    for r in included:
        rid = r["regime_id"]
        g = df[df["regime_id"] == rid].copy()
        eps, daily_dds, _, _ = episodes_for_regime(g)
        rmax = per_regime_max_dd(g)
        regime_max_rows.append(
            {
                "regime_id": rid,
                "start": r["start"],
                "end": r["end"],
                "n_days": r["n_days"],
                "max_drawdown_pct": rmax,
            }
        )
        for ep in eps:
            rows.append(
                {
                    "regime_id": rid,
                    "regime_start": r["start"],
                    "regime_end": r["end"],
                    "episode_start": ep["start"],
                    "episode_end": ep["end"],
                    "max_drawdown_pct": ep["max_drawdown_pct"],
                    "peak_at_start": ep["peak_at_start"],
                    "ended_by": ep["ended_by"],
                }
            )
        g_sorted = g.sort_values("Date").reset_index(drop=True)
        for i, dd in enumerate(daily_dds):
            daily_rows.append(
                {
                    "regime_id": rid,
                    "date": g_sorted["Date"].iloc[i],
                    "drawdown_pct": dd,
                }
            )

    ep_df = pd.DataFrame(rows)
    daily_df = pd.DataFrame(daily_rows)
    regime_max_df = pd.DataFrame(regime_max_rows)

    if ep_df.empty:
        print("No dip episodes found — aborting.", file=sys.stderr)
        return 1

    # Chronological holdout split by regime
    train_regimes = [r for r in included if r["end"] < HOLDOUT_START]
    holdout_regimes = [r for r in included if r["start"] >= HOLDOUT_START]
    # Regimes that span the boundary: exclude from both (or assign by end rule —
    # locked: train = END before, holdout = START on/after; spanning go nowhere)
    spanning = [
        r for r in included
        if not (r["end"] < HOLDOUT_START or r["start"] >= HOLDOUT_START)
    ]

    split_method = "regime_end_before_2024-01-01 / regime_start_on_or_after_2024-01-01"
    train_ids = {r["regime_id"] for r in train_regimes}
    hold_ids = {r["regime_id"] for r in holdout_regimes}

    train_ep = ep_df[ep_df["regime_id"].isin(train_ids)].copy()
    hold_ep = ep_df[ep_df["regime_id"].isin(hold_ids)].copy()

    fallback_note = ""
    if len(hold_ep) < 5:
        # Fallback: last 20% of calendar time among usable bars
        t0 = usable["Date"].min()
        t1 = usable["Date"].max()
        split_date = t0 + (t1 - t0) * 0.80
        split_method = (
            f"FALLBACK last-20% calendar (split_date={split_date.date()}) "
            f"because primary holdout had {len(hold_ep)} episodes (<5)"
        )
        fallback_note = split_method
        # Re-assign by episode_start relative to split_date for episodes in included regimes
        train_ep = ep_df[ep_df["episode_start"] < split_date].copy()
        hold_ep = ep_df[ep_df["episode_start"] >= split_date].copy()
        # Also recompute regime counts for reporting
        train_regimes = [r for r in included if r["end"] < split_date]
        holdout_regimes = [r for r in included if r["start"] >= split_date]
        spanning = [
            r for r in included
            if not (r["end"] < split_date or r["start"] >= split_date)
        ]

    # --- LOCKED: buffer from TRAIN only ---
    train_dds = train_ep["max_drawdown_pct"].values
    hold_dds = hold_ep["max_drawdown_pct"].values

    def pctiles(arr: np.ndarray) -> dict:
        if len(arr) == 0:
            return {k: float("nan") for k in ("p50", "p80", "p90", "median", "max", "mean", "n")}
        return {
            "n": len(arr),
            "median": float(np.median(arr)),
            "p50": float(np.percentile(arr, 50)),
            "p80": float(np.percentile(arr, 80)),
            "p90": float(np.percentile(arr, 90)),
            "max": float(np.max(arr)),
            "mean": float(np.mean(arr)),
            "min": float(np.min(arr)),
        }

    train_stats = pctiles(train_dds)
    hold_stats = pctiles(hold_dds)
    all_stats = pctiles(ep_df["max_drawdown_pct"].values)

    buffer = train_stats["p80"]  # THE buffer — train 80th percentile only

    if len(hold_dds) > 0:
        coverage = float(np.mean(hold_dds <= buffer) * 100.0)
    else:
        coverage = float("nan")

    # Secondary distributions for context
    daily_stats = pctiles(daily_df["drawdown_pct"].values) if not daily_df.empty else {}
    regime_max_stats = pctiles(regime_max_df["max_drawdown_pct"].values)

    # Save CSVs
    ep_df.to_csv(OUT_DIR / "episode_drawdowns.csv", index=False)
    train_ep.to_csv(OUT_DIR / "episode_drawdowns_train.csv", index=False)
    hold_ep.to_csv(OUT_DIR / "episode_drawdowns_holdout.csv", index=False)
    regime_max_df.to_csv(OUT_DIR / "regime_max_drawdowns.csv", index=False)

    # Regime summary table for report
    def fmt_regimes(regs):
        lines = []
        for r in regs:
            lines.append(
                f"| {r['regime_id']} | {r['start'].date()} | {r['end'].date()} | {r['n_days']} |"
            )
        return "\n".join(lines) if lines else "| (none) | | | |"

    # Verdict
    if np.isnan(coverage):
        verdict = "inconclusive — no holdout episodes"
        verdict_detail = "Could not evaluate holdout coverage."
    elif coverage >= 70 and coverage <= 90:
        verdict = "supports ~80% story"
        verdict_detail = (
            f"Holdout coverage of {coverage:.1f}% is near the target 80%, "
            "suggesting the train buffer roughly transfers."
        )
    elif coverage >= 60:
        verdict = "fragile"
        verdict_detail = (
            f"Holdout coverage of {coverage:.1f}% is in the ballpark but soft; "
            "with few regimes this could be noise."
        )
    else:
        verdict = "fails holdout"
        verdict_detail = (
            f"Holdout coverage of {coverage:.1f}% is well below ~80%; "
            "the train buffer did not contain most later dips."
        )

    data_start = df["Date"].min().date()
    data_end = df["Date"].max().date()
    usable_start = usable["Date"].min().date()
    usable_end = usable["Date"].max().date()

    report = f"""# ETH 200-DMA Buffer Experiment

**Research question:** During past periods when daily Ethereum closed above its 200-day moving average, how large is a “normal” drop from a recent high — and what buffer size would have contained about 80% of those dips? Hold out a slice of history to check whether ~80% coverage still roughly holds.

**Run date (box local / ET):** {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M ET")}

---

## Plain-English summary

We looked at every stretch of time when ETH’s daily close was **above** its 200-day average (an “uptrend regime”). Inside those stretches, price often dips below its recent high before making a new high. We measured how deep those dips got, found a buffer that would have covered **80% of dips in the earlier (train) period**, then checked what fraction of later (holdout) dips that same buffer would have contained.

### Headline results

| Metric | Value |
|--------|-------|
| **Train 80th-percentile buffer** | **{buffer:.2f}%** |
| **Holdout coverage** (episodes ≤ train buffer) | **{coverage:.1f}%** |
| Holdout 80th percentile (for comparison only) | {hold_stats['p80']:.2f}% |
| **Verdict** | **{verdict}** |

{verdict_detail}

---

## Data

| Item | Detail |
|------|--------|
| Source | Yahoo Finance via `yfinance`, ticker `ETH-USD` |
| Series | Daily close (auto-adjusted), calendar days (crypto 7d/week) |
| Raw date range | {data_start} → {data_end} ({len(df)} bars) |
| After 200-day MA warmup | {usable_start} → {usable_end} ({len(usable)} bars) |
| 200-day MA | Simple moving average of Close over **200 calendar days** |

---

## Locked definitions (used in code)

1. **Uptrend regime:** consecutive days with Close > 200-day MA.
2. **Short regimes:** regimes shorter than **{MIN_REGIME_DAYS} days are excluded** from dip sampling ({len(excluded)} short regimes dropped).
3. **Recent high:** running max Close since regime start.
4. **Dip episode (primary):** starts when Close falls below the running peak; ends when price makes a new regime peak **or** the regime ends. Metric = **max drawdown %** during the episode.
5. **Buffer:** 80th percentile of episode max drawdowns on **TRAIN only** (chosen before looking at holdout coverage).
6. **Holdout split:** {split_method}

Regimes that span the train/holdout boundary are excluded from both sets ({len(spanning)} spanning).

---

## Sample sizes

| Set | Regimes (included, ≥{MIN_REGIME_DAYS}d) | Dip episodes |
|-----|------------------------------------------|--------------|
| All included | {len(included)} | {len(ep_df)} |
| Train | {len(train_regimes)} | {len(train_ep)} |
| Holdout | {len(holdout_regimes)} | {len(hold_ep)} |
| Spanning (excluded from both) | {len(spanning)} | — |
| Short regimes excluded | {len(excluded)} | — |

### Included regimes

| ID | Start | End | Days |
|----|-------|-----|------|
{fmt_regimes(included)}

---

## Distribution of episode max drawdowns

### Train (buffer is locked from this column’s 80th pct)

| Stat | Train | Holdout | All episodes |
|------|-------|---------|--------------|
| N | {train_stats['n']} | {hold_stats['n']} | {all_stats['n']} |
| Median / 50th | {train_stats['median']:.2f}% | {hold_stats['median']:.2f}% | {all_stats['median']:.2f}% |
| **80th** | **{train_stats['p80']:.2f}%** ← buffer | {hold_stats['p80']:.2f}% | {all_stats['p80']:.2f}% |
| 90th | {train_stats['p90']:.2f}% | {hold_stats['p90']:.2f}% | {all_stats['p90']:.2f}% |
| Max | {train_stats['max']:.2f}% | {hold_stats['max']:.2f}% | {all_stats['max']:.2f}% |
| Mean | {train_stats['mean']:.2f}% | {hold_stats['mean']:.2f}% | {all_stats['mean']:.2f}% |

### Holdout coverage check

Of the **{hold_stats['n']}** holdout dip episodes, **{coverage:.1f}%** had max drawdown ≤ the train buffer of **{buffer:.2f}%**.

(Ideal story: ~80%. We did **not** re-fit the buffer on holdout.)

### Secondary context (not used for the buffer)

| Distribution | N | Median | 80th | 90th | Max |
|--------------|---|--------|------|------|-----|
| Daily drawdown_pct (all included regime-days) | {daily_stats.get('n', '—')} | {daily_stats.get('median', float('nan')):.2f}% | {daily_stats.get('p80', float('nan')):.2f}% | {daily_stats.get('p90', float('nan')):.2f}% | {daily_stats.get('max', float('nan')):.2f}% |
| Per-regime max drawdown | {regime_max_stats['n']} | {regime_max_stats['median']:.2f}% | {regime_max_stats['p80']:.2f}% | {regime_max_stats['p90']:.2f}% | {regime_max_stats['max']:.2f}% |

Daily drawdowns are much smaller than episode maxima (most days are near the peak). Per-regime max is a harsher “worst dip of the whole uptrend” metric — fewer observations, larger numbers.

---

## Honest caveats

- **Few regimes:** Crypto has only a handful of multi-month uptrends above the 200-DMA since ETH-USD history began. Small-N percentiles are noisy.
- **Overfit / definition risk:** Episode boundaries, the 30-day minimum, and the 200-day window are reasonable but arbitrary. Different choices would move the buffer.
- **Regime change:** ETH market structure, ETF flows, and correlation with BTC/macro have changed; train-era dip sizes may not forecast future ones.
- **Survivorship of definition:** We only study dips *while still above* the 200-DMA. Drops that break the MA end the regime and are not counted as completed “in-regime” recoveries in the same way — episodes that end because the regime ends (`ended_by=regime_end`) are still included with their max drawdown at exit.
- **No trading claim:** This is a historical distribution study, not a trading system. No position sizing, fees, or live signals.
- **Data vendor:** Yahoo/`yfinance` closes can be revised; results should be re-run for audit.

{("**Fallback split used:** " + fallback_note) if fallback_note else ""}

---

## Verdict

**{verdict}**

{verdict_detail}

A round “~{buffer:.0f}% buffer above a recent high while ETH is above its 200-DMA” is the train-set 80% story. Holdout coverage was **{coverage:.1f}%**.

---

## Files

| File | Purpose |
|------|---------|
| `analyze_eth_buffer.py` | Reproducible script |
| `episode_drawdowns.csv` | All dip episodes |
| `episode_drawdowns_train.csv` | Train episodes |
| `episode_drawdowns_holdout.csv` | Holdout episodes |
| `regime_max_drawdowns.csv` | Per-regime max drawdown |
| `REPORT.md` | This report |

Re-run:

```bash
/workspace/eth-200dma-buffer/.venv/bin/python /workspace/eth-200dma-buffer/analyze_eth_buffer.py
```
"""

    (OUT_DIR / "REPORT.md").write_text(report)
    print("\n=== RESULTS ===")
    print(f"Train episodes: {train_stats['n']}")
    print(f"Holdout episodes: {hold_stats['n']}")
    print(f"Train 80th-pct buffer: {buffer:.4f}%")
    print(f"Holdout coverage: {coverage:.2f}%")
    print(f"Holdout 80th pct: {hold_stats['p80']:.4f}%")
    print(f"Verdict: {verdict}")
    print(f"Wrote {OUT_DIR / 'REPORT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
