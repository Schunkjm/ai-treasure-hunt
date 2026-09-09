# Frozen research infrastructure — release 1

Frozen on 2026-09-08 by the human researcher's instruction, before any historical V0/V1 performance was examined. The freeze covers both hypotheses and their shared infrastructure. It does not authorize performance review in this stage. Any later methodological or parameter change requires explicit human authorization and a separately recorded version; never overwrite this history to improve results.

## Origin and purpose

V0 — GITHUB BASELINE derives from the [kernc/backtesting.py Quick Start](https://github.com/kernc/backtesting.py/blob/master/doc/examples/Quick%20Start%20User%20Guide.py) and [strict crossover definition](https://github.com/kernc/backtesting.py/blob/master/backtesting/lib.py). Its concept is independently implemented with pandas, with no third-party strategy code copied or engine installed. Existing AGPL licensing notes apply if source copying is later proposed.

V1 — HUMAN HYPOTHESIS adds the human researcher's ATR-contraction condition. The user chose all parameters before observing results. The experiment asks whether this additional clue improves the baseline's subsequent excess returns; failure, no difference, or inconclusive evidence are legitimate results. The AI's earlier momentum suggestion is rejected and has no role.

## Universe, benchmark, sectors

Exact fixed stocks, with no substitutions:

AAPL, MSFT, NVDA, AMZN, GOOGL, META, AVGO, AMD, ORCL, CRM, JPM, BAC, GS, MS, V, MA, XOM, CVX, COP, SLB, CAT, GE, RTX, ETN, HON, DE, WMT, COST, HD, MCD, NKE, SBUX, LLY, UNH, JNJ, ABBV, MRK, NFLX, DIS, T, VZ, TSLA, QCOM, TXN, IBM, AMAT, MU, LOW, PEP, KO.

Benchmark: SPY, not a stock-universe member. This is a human-selected experimental universe, not historical point-in-time S&P 500 membership. Selection and survivorship limitations remain.

The fixed mapping in reference/sectors.csv contains exactly one label for each stock. Source: Yahoo company profile sectors retrieved 2026-09-08; each row records the original label, normalized label, URL, and retrieval timestamp. Normalize Technology to Information Technology, Financial Services to Financials, Healthcare to Health Care, Consumer Cyclical to Consumer Discretionary, and Consumer Defensive to Consumer Staples; preserve Communication Services, Industrials, and Energy. These are broad GICS-style categories, not a licensed official GICS history. Labels are current static diagnostics, not historical membership claims. No sector information enters the signal. The pipeline appends it to event records only after calculating signals and outcomes.

## Data and evaluation window

Data vendor: Yahoo Finance through yfinance 0.2.66. Python 3.13.2, pandas 2.3.3, numpy 2.3.3 were validated. No ML, optimizer, technical-analysis dependency, trading framework, or research database is used. yfinance's incidental cookie/timezone cache is project-local and ignored by git.

Frozen history request: 2025-03-08 through 2026-09-08, with exclusive download end 2026-09-09. Original snapshot is data/snapshot_2026-09-08/vendor/. Its 377 regular trading sessions run 2025-03-10 through 2026-09-08. Use the bounded calendar of weekdays excluding the full NYSE holidays recorded in src/config.py; half days remain sessions. Every instrument is reindexed to the same calendar, not compressed to its available price rows. Calendar sources are linked in PIPELINE.md.

Evaluation: 2025-09-08 through 2026-09-08 inclusive, 252 sessions. There are 125 preceding initialization sessions. Require signal, entry, and exit to lie within this evaluation window for a measurable outcome. At the frozen as-of date, 2026-08-21 is the latest possible signal date with a matured exit; the last 11 signal dates have pending outcomes. Do not extend or shift the window based on results.

Daily retrieval settings: interval=1d, auto_adjust=False, back_adjust=False, actions=True, repair=False, keepna=True, prepost=False, rounding=False. Preserve vendor OHLCV, Adj Close, and available corporate-action columns. Let adjustment factor f(t) = vendor Adj Close(t) / vendor Close(t). Multiply all four OHLC fields by the SAME row factor; do not scale Volume. This reproduces auto_adjust=True's OHLC convention while preserving the original vendor inputs. Vendor Close may already be split-adjusted; the snapshot is not exchange-original data.

Use those consistent adjusted High/Low/Close values for ATR and adjusted Close for SMA and ATR normalization. Use adjusted Open for BOTH stock and SPY outcomes. These ratios are the agreed total-return proxy, not an explicitly modeled dividend reinvestment portfolio. A present-day revised history cannot certify exact point-in-time historical availability.

## KO resolution and missing-data policy

The original KO bar on 2026-09-08 reports Open=[HISTORICAL YAHOO VALUE NOT DISTRIBUTED], Low=[HISTORICAL YAHOO VALUE NOT DISTRIBUTED]: its Open is below its Low. All fields are finite and positive, with positive volume; Adj Close equals Close, giving factor 1. Dividends and Stock Splits are zero on that row. The contradiction exists before adjustment and is not introduced by our adjustment calculation. Repeated daily queries retain it.

Yahoo's same-day regular-session one-minute response contains all 390 expected minutes (09:30 through 15:59 Eastern), without missing/duplicate/invalid bars. Its minimum Low is [HISTORICAL YAHOO VALUE NOT DISTRIBUTED], also its first Open/Low and the reported daily Open. Apply the documented mechanical correction in reference/data_corrections.json: replace ONLY the inconsistent daily Low with that minimum, before adjustment. Preserve the original vendor file. Freeze supporting daily/minute responses and their hashes. This resolves the internal inconsistency using observed Yahoo prices; it does not claim independent exchange certification.

Minute aggregate Close and Volume differ from the daily fields, so do not rebuild the entire daily bar from minute data or change daily Close/Volume. Such aggregates can differ in session/auction coverage; no claim is made that the precise upstream cause was diagnosed. The evidence supports a Yahoo daily-field inconsistency and a narrow Low correction, not a split or dividend fix.

KO remains in the universe. No observations are quarantined after this documented correction in this snapshot. The prior output is retained for audit. Final corrected calculation frames live under the frozen output directory, not the earlier snapshot/adjusted directory. The correction must match its exact original field value; a changed source fails validation instead of receiving a blind patch.

Missing/invalid observations in general stay on the calendar and invalidate only dependent calculations; never fill or invent a price, move an entry, substitute a ticker, or drop a company based on results. Missing tickers, duplicates, unexpected dates, or changes to locked files prevent a frozen build. No subsequent data refresh or correction may silently change this frozen snapshot.

## Exact V0 formula

Let t be the current completed regular trading session and C(t) its consistent adjusted Close.

- SMA10(t) = [C(t−9) + ... + C(t)] / 10.
- SMA20(t) = [C(t−19) + ... + C(t)] / 20.
- V0(t) is true exactly when SMA10(t−1) < SMA20(t−1) AND SMA10(t) > SMA20(t).

Require 21 consecutive valid closes to evaluate both dates. Equality does not trigger. Being already above the slow average is not a fresh event. No intraday crossover, bearish trade, price filter, volume filter, minimum spread, stop, or position-sizing rule is added. A later bearish crossover does not truncate an outcome. This is an event baseline, not a full daily ranking.

## Exact ATR and V1 formulas

For valid adjusted OHLC and previous adjusted Close:

TR(t) = max[High(t)−Low(t), abs(High(t)−Close(t−1)), abs(Low(t)−Close(t−1))].

ATR14 starts with the arithmetic mean of the first 14 consecutive valid true ranges after the frozen history start. Subsequent values use Wilder recurrence: ATR14(t) = [13 × ATR14(t−1) + TR(t)] / 14. No first-row high-minus-low substitute is used without a previous close. Missing input resets initialization; require a new 14 valid TR seed. Never backward-fill or switch smoothing definitions.

A(t) = ATR14(t) / Close(t). Store as a fraction; multiplying all values by 100 is merely display formatting.

M(t) = max[A(t−20), ..., A(t−1)], requiring all 20 valid PRIOR session values and excluding today.

Contraction(t) is A(t) <= 0.80 × M(t).

V1(t) = V0(t) AND Contraction(t), on the SAME signal date. Threshold equality qualifies. No separate contraction event, minimum duration, waiting interval, additional threshold, or later confirmation is required. With all inputs valid and M(t)=0, preserve the literal inequality. V1 is necessarily contained in V0; the final validation also checks it is a proper subset in this snapshot (at least one V0 event is filtered out), without reporting counts or outcomes.

V1 has a mathematical minimum of 35 consecutive OHLC sessions for initialization; the frozen history provides substantially more. Missing indicators/flags remain unavailable, not automatically false.

## Information boundary and outcomes

Signals use only completed close-t data and prior data. Assume the signal is ready before the next open. No future prices or outcome columns enter src/signals.py; its only admitted price columns are High, Low, Close. Sector labels are excluded too. Prefix-invariance and future-mutation tests enforce calculation causality. This does not prove that a vendor's reconstructed history was unrevised at t.

Entry date: session t+1 Open. Exit measurement: session t+11 Open. Thus exactly 10 trading intervals elapse from entry to exit. The signal-to-entry overnight move is not earned. SPY uses the same entry AND exit dates; do not shift each instrument independently after dropping missing observations.

Stock return R_i(t) = adjusted Open_i(t+11) / adjusted Open_i(t+1) − 1.

Benchmark return R_SPY(t) = adjusted Open_SPY(t+11) / adjusted Open_SPY(t+1) − 1.

Excess E_i(t) = R_i(t) − R_SPY(t). Stored values are fractions; multiply by 100 when displaying excess-return percentage points. Invalid/missing endpoints yield unavailable outcomes. Unmatured horizons remain pending, not zero. Preserve the event even if its label is unavailable. These are overlapping event observations, not independently financed portfolio trades.

## Frozen evaluation framework — not executed in this stage

Primary: arithmetic average subsequent 10-interval excess return per measurable stock-signal observation, with each observation weighted equally. Mean = sum(E) / N.

Secondary: median of the same E values; hit rate = count(E > 0) / N (multiply by 100 to display a percent); number of signals/sample size. Exactly zero is not a hit. Empty groups have undefined mean/median/hit rate, not zero. Report detected, measurable, pending, and unavailable counts separately.

Compare ALL qualifying V0 events with the V1 subset, on their identical endpoint conventions. Report mean, median, hit rate, sample retention/reduction, and concentration across stocks, fixed sectors, and dates/months. If ATR availability differs, preserve all-V0 reporting and additionally disclose common-eligibility diagnostics. No stock/date/subgroup is removed because its outcome is unattractive.

Do not call V1 better because one metric improves. Discuss the mean alongside median, hit rate, sample reduction, and concentration. V1 and V0 are nested and outcomes overlap; do not treat them as independent samples. No optimization, post-result parameter change, equity-curve compounding, or statistical-proof/trading-edge claim from one year is authorized. Costs, slippage, and portfolio financing are not modeled in these gross outcome labels.

## Freeze enforcement and correspondence to implementation

The JSON block below is a machine-checkable transcription of every uppercase src/config.py setting. Tests compare it to actual code settings. Formula tests verify behavior with synthetic values. reference/sectors.csv is checked for exact universe coverage and diagnostic isolation. reference/data_corrections.json is checked against Yahoo evidence. FROZEN_LOCK.json pins source, tests, specification, reference files, dependencies, original vendor snapshot, and investigation evidence by SHA-256. A mismatch fails the build; do not regenerate the lock to bypass a discrepancy without human authorization for a new version.

The metrics are frozen definitions for a later evaluator; no metric-calculation function or performance reporting has been implemented here. A human can modify files and hashes, so this is audit/change detection rather than tamper-proof external certification.

```json
{
  "UNIVERSE": [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "AVGO",
    "AMD",
    "ORCL",
    "CRM",
    "JPM",
    "BAC",
    "GS",
    "MS",
    "V",
    "MA",
    "XOM",
    "CVX",
    "COP",
    "SLB",
    "CAT",
    "GE",
    "RTX",
    "ETN",
    "HON",
    "DE",
    "WMT",
    "COST",
    "HD",
    "MCD",
    "NKE",
    "SBUX",
    "LLY",
    "UNH",
    "JNJ",
    "ABBV",
    "MRK",
    "NFLX",
    "DIS",
    "T",
    "VZ",
    "TSLA",
    "QCOM",
    "TXN",
    "IBM",
    "AMAT",
    "MU",
    "LOW",
    "PEP",
    "KO"
  ],
  "BENCHMARK": "SPY",
  "FAST": 10,
  "SLOW": 20,
  "ATR_PERIOD": 14,
  "CONTRACTION_LOOKBACK": 20,
  "CONTRACTION_MULTIPLIER": 0.8,
  "HORIZON": 10,
  "HISTORY_START": "2025-03-08",
  "AS_OF": "2026-09-08",
  "DOWNLOAD_END_EXCLUSIVE": "2026-09-09",
  "EVALUATION_START": "2025-09-08",
  "DATA_SETTINGS": {
    "interval": "1d",
    "auto_adjust": false,
    "back_adjust": false,
    "actions": true,
    "repair": false,
    "keepna": true,
    "prepost": false,
    "rounding": false
  },
  "METRICS": {
    "primary": "arithmetic_mean_signal_excess_return",
    "secondary": [
      "median_signal_excess_return",
      "hit_rate_excess_strictly_positive",
      "signal_sample_size"
    ],
    "weighting": "equal_weight_per_measurable_stock_signal",
    "return_units": "fractions; multiply by 100 for percentage-point display",
    "comparison": "all_V0_vs_V1_subset_same_endpoints"
  },
  "HOLIDAYS": [
    "2025-04-18",
    "2025-05-26",
    "2025-06-19",
    "2025-07-04",
    "2025-09-01",
    "2025-11-27",
    "2025-12-25",
    "2026-01-01",
    "2026-01-19",
    "2026-02-16",
    "2026-04-03",
    "2026-05-25",
    "2026-06-19",
    "2026-07-03",
    "2026-09-07"
  ]
}
```

## Remaining limitations and next stage

One recent year, the chosen survivors/universe, fixed present-day sector labels, dependent outcomes, revised vendor history, the narrow Yahoo-derived repair, and approximate execution cannot be eliminated by software validation. Freeze readiness is not evidence of profitability. The next stage requires the user's explicit instruction to examine the first legitimate V0/V1 performance comparison.
