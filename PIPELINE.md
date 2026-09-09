# V0/V1 pipeline: infrastructure only

**Freeze update (2026-09-08):** FROZEN_SPECIFICATION.md now governs release 1. The KO Low was mechanically corrected from Yahoo's complete one-minute session evidence; the prior quarantine described below is historical. reference/sectors.csv is fixed diagnostic metadata. Rebuild the locked snapshot without --download, using `python -m src.pipeline --output output/frozen_2026-09-08`. The completed frozen output stores corrected calculation frames under its own adjusted/ directory; the earlier snapshot/adjusted/ files remain historical. FROZEN_LOCK.json prevents unnoticed changes to source, specification, reference files, and original/evidence data. Acquisition and preparation commands are disabled after freeze. A new snapshot or methodology version requires explicit human authorization.

This stage acquires data, validates it, and creates separate signal and outcome files. It does **not** calculate performance summaries or compare hypotheses. Do not open outcome/event return fields for research interpretation until the user authorizes the next stage.

## Reproduce

Use Python 3.13 (validated with 3.13.2) and the versions in requirements.txt. From the project root:

```text
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m src.pipeline --download
```

After acquisition, rebuilding with no network request is possible using the saved snapshot and a new output directory:

```text
python -m src.pipeline --output output/rebuild
```

Completed output directories cannot be overwritten by the command. Existing vendor files are reused on acquisition resume. For an intentionally new snapshot, use a new --snapshot directory and new --output directory and record why. Do not refresh historical data after results without an explicit logged research decision. Configured dates and parameters live in src/config.py, not a performance-tuning CLI.

## Layout

- src/config.py: exact 50 tickers, SPY, frozen parameters, snapshot dates, bounded session calendar.
- src/data.py: consistent adjustment, expected dates, and OHLCV validation.
- src/signals.py: independent SMA/crossover/Wilder ATR/contraction calculations; admits only High, Low, Close.
- src/outcomes.py: separate evaluation-only next-open labels.
- src/pipeline.py: acquisition, quality gates, provenance, output files; no return-summary code.
- tests/test_pipeline.py: synthetic tests, including numerical endpoint examples.
- data/snapshot_2026-09-08/vendor/: retained Yahoo responses before dividend auto-adjustment, including Adj Close and corporate-action columns.
- data/snapshot_2026-09-08/adjusted/: consistently adjusted, session-aligned calculation inputs; bad bars remain unavailable.
- data/snapshot_2026-09-08/retrieval/: per-ticker retrieval times and SHA-256 hashes.
- output/pipeline_2026-09-08/data_quality.json: safe-to-inspect dates, coverage, exceptions, and invariant checks; no performance statistics.
- output/pipeline_2026-09-08/signals/: evaluation-window indicators and nullable V0/V1 flags.
- output/pipeline_2026-09-08/outcomes/: evaluation-only labels for each evaluation date, including pending horizons.
- output/pipeline_2026-09-08/events/: V0 events joined to V1 membership and labels for the later authorized analysis; **not inspected for performance in this stage**.
- output/pipeline_2026-09-08/manifest.json: versions, configuration, source/data/output SHA-256 hashes.

Data, generated outputs, and local caches are gitignored. Do not assume Yahoo market data is licensed for republication just because the research code will be public. The three original research records remain the chronological authority; onboarding files deferred by the user remain deferred.

## Dates and price conventions

Before downloads, fixed history request: March 8, 2025 through September 8, 2026; yfinance's exclusive end is September 9, 2026. The first expected session is March 10, 2025. Evaluation is September 8, 2025 through September 8, 2026, inclusive. Acquisition began after the September 8 regular close. Corporate-action-adjusted daily history can still be revised after retrieval.

The bounded calendar uses weekdays minus the full closures listed in the [NYSE/ICE 2025–2027 calendar announcement](https://ir.theice.com/press/news-details/2024/NYSE-Group-Announces-2025-2026-and-2027-Holiday-and-Early-Closings-Calendar/default.aspx) and checked against the [NYSE session calendar](https://www.nyse.com/trade/hours-calendars). Half days remain sessions. Every ticker and SPY must be aligned to these dates. This avoids an extra calendar dependency and prevents a missing vendor row from moving entry/exit by one session. It is not a general-purpose exchange calendar; dates must be reviewed if the snapshot range changes, including exceptional closures.

Download settings: interval='1d', auto_adjust=False, back_adjust=False, actions=True, repair=False, keepna=True, prepost=False, rounding=False. The retained Close is Yahoo's supplied non-auto-adjusted Close; it is not represented as an exchange-original, never-adjusted archive (Yahoo may already account for splits).

For each row, factor = Adj Close / Close. Independently apply this factor to Open, High, Low, and Close. This matches the price transformation of **auto_adjust=True** in the installed yfinance 0.2.66, whose local auto_adjust source was inspected. With that setting, Open/High/Low are scaled and Close is replaced by Adj Close. We request False only to retain both vendor columns and an auditable factor before making the same coherent transformation. See [yfinance download documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html) and [versioned adjustment source](https://github.com/ranaroussi/yfinance/blob/0.2.66/yfinance/utils.py).

Volume and action columns are retained without multiplying by the price factor. ATR always consumes adjusted High, adjusted Low, and adjusted current/prior Close. Both stock and SPY outcome opens use the same adjustment convention. These returns are a total-return proxy, not a separately modeled cash-dividend reinvestment portfolio. A current adjusted download does not establish what exact historical values were visible on a signal date. Calendar checks and causal formulas do not remove that limitation.

## Frozen calculations

SMA10 and SMA20 include the signal day's completed Close. V0 requires SMA10(t−1) < SMA20(t−1) AND SMA10(t) > SMA20(t). Equality is not a crossover; no bearish actions or persistent-above signals are generated.

TR(t) = max[High−Low, abs(High−prior Close), abs(Low−prior Close)]. Require a prior valid close. Seed ATR14 with the mean of 14 valid TRs; thereafter ATR14(t) = [13 × ATR14(t−1) + TR(t)] / 14. Missing history resets the seed; no backward filling or short-window substitutes.

ATR% = ATR14 / Close. The reference is ATR%.shift(1).rolling(20).max(), requiring all 20 values. V1 = V0 AND [ATR%(t) <= 0.80 × reference(t)]. Percent values are stored as ratios, not multiplied by 100. Null flags represent unavailable calculations. The initialization starts at the frozen history boundary, providing several months of warm-up before evaluation.

For signal date at session position t: entry position t+1; exit position t+11. Exactly 10 trading intervals separate them. Calculate stock and SPY open-to-open simple returns over identical dates, then subtract. Stored return fields are fractions: 0.01 would be one percentage point of excess return. No numerical historical return examples are shown here.

The final 11 signal dates cannot have a fully matured t+11 outcome at this snapshot and retain pending_horizon labels. Do not assign them zero returns or extend the data into an unavailable future. All measurable endpoints lie within the frozen evaluation window. No bearish cross or ATR stop changes an outcome horizon.

## Data-quality rules and known exception

Missing tickers, duplicate dates, or unexpected extra dates stop the build. No substitute symbols are allowed. Missing observations are recorded and reindexed to the fixed calendar. Nonpositive/nonfinite OHLC, inconsistent high/low bounds, invalid adjustment factors, or invalid volume are identified. Invalid source bars are preserved but their calculation OHLCV is quarantined as missing, with the exact ticker/date recorded. No price is guessed or automatically repaired.

**Known exception:** KO on September 8, 2026 reports Open below Low. A separate Yahoo recheck returned the same inconsistency; its response is preserved in data/recheck/KO.csv. The calculation row is unavailable. That can suppress a current signal or invalidate an earlier event whose entry/exit uses that row; it cannot silently move those dates. No ticker or outcome is excluded for unattractive performance. Review this exception before approving the first performance comparison.

Warm-up completeness is checked at the first evaluation session for each stock. Later unavailable bars remain explicitly unavailable rather than incorrectly failing the initial-history test. A successful software/invariant check is separate from a fully clean data snapshot. The quality report exposes data_exceptions_require_review.

## Verification and provenance

Synthetic tests check strict equality, SMA windows, Wilder seeding/recurrence and overnight gaps, prior-window exclusion/expiration, missing-data reset, positive V1 cases and subset membership, every-prefix causality, future-price mutations, outcome-column isolation, common SPY endpoints, exactly ten intervals, pending/missing labels, OHLC adjustment, and calendar/data-quality behavior.

The actual build also asserts prefix invariance at multiple historical cutoffs, outcome-column isolation, V1 subset membership, initial warm-up completeness, and endpoint position differences without reporting return statistics. SHA-256 reads bytes for integrity only; no outcome files are displayed or interpreted. There is no performance-comparison command in this stage.

The first restricted-network download attempt failed at the environment proxy. Authorized execution with network access restored allowed all 51 downloads. The cache is routed to .cache/yfinance inside the project. yfinance uses incidental cookie/timezone cache storage; no research database was introduced. No dependencies were added beyond the three pinned direct requirements (and yfinance's existing transitive dependencies).

The exact fixed universe is a human-selected experimental set, not a point-in-time S&P 500 universe. Selection/survivorship bias, a single recent year, dependent outcomes, approximate execution, corporate-action revisions, and omitted transaction costs remain limitations. Sector mapping is still needed for the later preregistered concentration diagnostics; none has been downloaded or guessed here.
