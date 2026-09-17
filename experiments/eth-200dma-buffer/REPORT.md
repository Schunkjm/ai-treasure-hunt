# ETH 200-DMA Buffer Experiment

**Research question:** During past periods when daily Ethereum closed above its 200-day moving average, how large is a “normal” drop from a recent high — and what buffer size would have contained about 80% of those dips? Hold out a slice of history to check whether ~80% coverage still roughly holds.

**Run date (box local / ET):** 2026-09-17 15:21 ET

---

## Plain-English summary

We looked at every stretch of time when ETH’s daily close was **above** its 200-day average (an “uptrend regime”). Inside those stretches, price often dips below its recent high before making a new high. We measured how deep those dips got, found a buffer that would have covered **80% of dips in the earlier (train) period**, then checked what fraction of later (holdout) dips that same buffer would have contained.

### Headline results

| Metric | Value |
|--------|-------|
| **Train 80th-percentile buffer** | **14.19%** |
| **Holdout coverage** (episodes ≤ train buffer) | **81.2%** |
| Holdout 80th percentile (for comparison only) | 12.45% |
| **Verdict** | **supports ~80% story** |

Holdout coverage of 81.2% is near the target 80%, suggesting the train buffer roughly transfers.

---

## Data

| Item | Detail |
|------|--------|
| Source | Yahoo Finance via `yfinance`, ticker `ETH-USD` |
| Series | Daily close (auto-adjusted), calendar days (crypto 7d/week) |
| Raw date range | 2017-11-09 → 2026-09-17 (3235 bars) |
| After 200-day MA warmup | 2018-05-27 → 2026-09-17 (3036 bars) |
| 200-day MA | Simple moving average of Close over **200 calendar days** |

---

## Locked definitions (used in code)

1. **Uptrend regime:** consecutive days with Close > 200-day MA.
2. **Short regimes:** regimes shorter than **30 days are excluded** from dip sampling (14 short regimes dropped).
3. **Recent high:** running max Close since regime start.
4. **Dip episode (primary):** starts when Close falls below the running peak; ends when price makes a new regime peak **or** the regime ends. Metric = **max drawdown %** during the episode.
5. **Buffer:** 80th percentile of episode max drawdowns on **TRAIN only** (chosen before looking at holdout coverage).
6. **Holdout split:** regime_end_before_2024-01-01 / regime_start_on_or_after_2024-01-01

Regimes that span the train/holdout boundary are excluded from both sets (1 spanning).

---

## Sample sizes

| Set | Regimes (included, ≥30d) | Dip episodes |
|-----|------------------------------------------|--------------|
| All included | 9 | 104 |
| Train | 5 | 73 |
| Holdout | 3 | 16 |
| Spanning (excluded from both) | 1 | — |
| Short regimes excluded | 14 | — |

### Included regimes

| ID | Start | End | Days |
|----|-------|-----|------|
| 0 | 2019-04-02 | 2019-08-13 | 134 |
| 3 | 2020-01-30 | 2020-03-11 | 42 |
| 5 | 2020-04-21 | 2021-06-21 | 427 |
| 8 | 2021-07-23 | 2022-01-06 | 168 |
| 10 | 2023-01-12 | 2023-08-16 | 217 |
| 12 | 2023-10-29 | 2024-07-03 | 249 |
| 15 | 2024-11-08 | 2025-02-01 | 86 |
| 18 | 2025-07-05 | 2025-11-03 | 122 |
| 22 | 2026-08-19 | 2026-09-17 | 30 |

---

## Distribution of episode max drawdowns

### Train (buffer is locked from this column’s 80th pct)

| Stat | Train | Holdout | All episodes |
|------|-------|---------|--------------|
| N | 73 | 16 | 104 |
| Median / 50th | 3.98% | 3.05% | 3.86% |
| **80th** | **14.19%** ← buffer | 12.45% | 13.12% |
| 90th | 21.49% | 18.77% | 21.16% |
| Max | 54.70% | 25.44% | 54.70% |
| Mean | 8.57% | 6.85% | 7.87% |

### Holdout coverage check

Of the **16** holdout dip episodes, **81.2%** had max drawdown ≤ the train buffer of **14.19%**.

(Ideal story: ~80%. We did **not** re-fit the buffer on holdout.)

### Secondary context (not used for the buffer)

| Distribution | N | Median | 80th | 90th | Max |
|--------------|---|--------|------|------|-----|
| Daily drawdown_pct (all included regime-days) | 1475 | 7.23% | 16.84% | 22.67% | 54.70% |
| Per-regime max drawdown | 9 | 29.15% | 35.20% | 43.62% | 54.70% |

Daily drawdowns are much smaller than episode maxima (most days are near the peak). Per-regime max is a harsher “worst dip of the whole uptrend” metric — fewer observations, larger numbers.

---

## Honest caveats

- **Few regimes:** Crypto has only a handful of multi-month uptrends above the 200-DMA since ETH-USD history began. Small-N percentiles are noisy.
- **Overfit / definition risk:** Episode boundaries, the 30-day minimum, and the 200-day window are reasonable but arbitrary. Different choices would move the buffer.
- **Regime change:** ETH market structure, ETF flows, and correlation with BTC/macro have changed; train-era dip sizes may not forecast future ones.
- **Survivorship of definition:** We only study dips *while still above* the 200-DMA. Drops that break the MA end the regime and are not counted as completed “in-regime” recoveries in the same way — episodes that end because the regime ends (`ended_by=regime_end`) are still included with their max drawdown at exit.
- **No trading claim:** This is a historical distribution study, not a trading system. No position sizing, fees, or live signals.
- **Data vendor:** Yahoo/`yfinance` closes can be revised; results should be re-run for audit.



---

## Verdict

**supports ~80% story**

Holdout coverage of 81.2% is near the target 80%, suggesting the train buffer roughly transfers.

A round “~14% buffer above a recent high while ETH is above its 200-DMA” is the train-set 80% story. Holdout coverage was **81.2%**.

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
