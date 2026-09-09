# First live frozen-engine run — 2026-09-08

Command: `python -m src.run_signal_engine`. Successful run ID: 20260908T234600_a319c2a9. Recorded at 2026-09-08 23:46:06.796072 UTC (19:46:06.796072 America/New_York). Latest completed market-data date: **2026-09-08**. Yahoo supplied that completed session for all 50 stocks and SPY; no fallback to an earlier day was necessary. This is a live source acquisition, not a new performance test.

## Current signals

**V0: NVDA, GS, UNH (3). V1: GS, UNH (2).** V1 membership overlaps V0; there are three distinct stock-date signals, not five independent events. Prices and SMAs below use the frozen adjusted convention. ATR ratios are displayed as percentages; saved engine CSVs retain fractions.

| Ticker | Sector | Close | SMA10 | SMA20 | ATR% | Prior-20 max ATR% | Contraction | Membership |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GS | Financials | 1036.5300 | 1029.4806 | 1029.4500 | 2.4378% | 3.2856% | Yes | V0 + V1 |
| UNH | Health Care | 400.8400 | 396.9890 | 396.5170 | 2.2397% | 2.8578% | Yes | V0 + V1 |
| NVDA | Information Technology | 225.7300 | 221.5410 | 220.4910 | 3.3165% | 3.5224% | No | V0 only |

## Educational Top 10 watchlist

Ordering follows the human request only: current V1, then V0-only, then usable inactive stocks with SMA10 at or below SMA20, closest from below. Within active categories use alphabetical ticker order. Signed gap = 100 × (SMA10/SMA20 − 1); inactive candidates are sorted from zero downward, with alphabetical ties. Already-above noncrossovers are not represented as approaching a bullish cross. No new predictive score, signal rule or journal membership is created. A near signal may never cross, and equality does not satisfy the frozen prior-day strictly-below rule.

| Order | Ticker | Status | Signed SMA gap |
| --- | --- | --- | --- |
| 1 | GS | ACTIVE V1 (also V0) | +0.002976% |
| 2 | UNH | ACTIVE V1 (also V0) | +0.119037% |
| 3 | NVDA | ACTIVE V0 ONLY | +0.476210% |
| 4 | MS | NEAR SIGNAL — NOT ACTIVE | -0.148770% |
| 5 | IBM | NEAR SIGNAL — NOT ACTIVE | -0.167662% |
| 6 | PEP | NEAR SIGNAL — NOT ACTIVE | -0.168784% |
| 7 | SBUX | NEAR SIGNAL — NOT ACTIVE | -0.292845% |
| 8 | JPM | NEAR SIGNAL — NOT ACTIVE | -0.387258% |
| 9 | XOM | NEAR SIGNAL — NOT ACTIVE | -0.535893% |
| 10 | GOOGL | NEAR SIGNAL — NOT ACTIVE | -0.563873% |

## Journal and prospective boundary

Before this run the production journal was empty. The engine appended **five version-level records**: NVDA/V0, GS/V0, GS/V1, UNH/V0 and UNH/V1. **Genuinely prospective additions: zero.** All are explicitly RETROSPECTIVE because the signal date is inside the already-examined research period ending September 8, even though the engine was run after close and before the next open. The classification is unchanged engine behavior; this live acquisition is not fresh out-of-sample evidence.

Only current-day signals were recorded; no older missed signal dates were backfilled. Pending: five version records (three stock-date events). Complete: zero. Entry and outcome fields remain blank. Duplicates prevented in this first run: zero, since the journal was empty; five unique IDs and no duplicates were verified. No additional live run was performed merely to increment a duplicate counter. Prior tests establish repeat-run deduplication.

## Operational checks

- Successful network-enabled run: 51/51 source series available and validated; 50/50 current stock rows usable. No failed downloads, stale tickers, missing sessions, extra dates, duplicate dates, zero-volume bars or remaining invalid prices were reported.
- Reapplied only the already-frozen KO September 8 correction: Low [HISTORICAL YAHOO VALUE NOT DISTRIBUTED] to [HISTORICAL YAHOO VALUE NOT DISTRIBUTED], using the earlier documented complete Yahoo minute-bar evidence. The original response is retained; no new repair was inferred.
- No calendar or journal integrity issue was reported on the successful run. The calendar selected the completed September 8 session. Source snapshots remain retrospective vendor data and can be revised later.
- An initial sandboxed attempt was interrupted before completing acquisition or publishing outputs; the interrupted process had exited, and its leftover lock was removed before retrying the unchanged command with network access. Its incomplete run directory is retained. This operational retry did not alter methodology or add journal records.
- Frozen research and prior first-pass/robustness/trend outputs remain hash-identical. No historical performance was recalculated or reinterpreted.

## Saved outputs and interpretation

Updated output/current_signal_scan.csv, output/current_signals_only.csv and output/prospective_signal_journal.csv. Created output/current_watchlist_top10.csv. The journal ledger and per-run raw data/manifest preserve provenance. The watchlist is educational monitoring only and its seven inactive rows do not enter the signal journal.

We started with an idea, tested it, discovered that it was not robust, refused to overfit it, and built a system capable of recording new evidence prospectively. This first live snapshot demonstrates operation, not a validated trading edge or investment recommendation. Decision D remains in force. The next packaging task is to make the complete experiment inspectable and reproducible; no public README/START_HERE package was created in this run.
