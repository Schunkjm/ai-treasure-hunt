# First legitimate V0 versus V1 comparison

Observed on 2026-09-08. **Descriptive classification: MIXED.**

The ATR filter improves the average excess return, but worsens the median and hit rate, removes 82.83% of completed signals, and leaves a result sensitive to a few outcomes and sector composition. It does not establish a validated trading strategy, statistical proof, or a recommendation to trade.

## Population and integrity

Used the unchanged frozen 2025-09-08 through 2026-09-08 evaluation window and the corrected, locked Yahoo snapshot. Only complete next-open through t+11-open outcomes are included. Latest possible mature signal date is 2026-08-21. V0 has 343 detected events: 332 completed and 11 pending. V1 has 62 detected events: 57 completed and 5 pending. No missing-endpoint events and no unknown ATR classifications occur among evaluated events. Pending observations are retained in the signals file and excluded from statistics, never treated as zero or failures.

Before evaluation, verified all frozen-file hashes and saved-output hashes. Independently recomputed saved labels from the frozen adjusted stock/SPY endpoint opens and checked dates, differences, duplicates, sectors, and evaluation inclusion. Group counts/contributions reconcile to the totals, and mean excess equals mean stock minus mean benchmark. Three new synthetic reporting tests passed. Frozen parameters, sector mapping, source data, source code, tests and specification remained unchanged. This new evaluator lives separately in analysis/ and is not V2.

Additional reporting conventions were stated before the first calculation: equal weight per completed stock-signal; linear-interpolated percentiles; sample standard deviation (ddof=1); strictly positive returns for hit/positive-absolute rates; best/worst reported for both excess and stock returns. These descriptive additions were explicitly requested in this stage and do not change the frozen primary metric. matplotlib 3.10.7, already installed, was used only for the requested static charts. CSVs use the existing pandas implementation; no workbook or strategy framework was introduced.

## Complete headline results

Return columns ending in pct are percentages. Excess-return columns ending in pp are percentage points. Hit/positive-return rates are percentages. Counts are integers. Statistics below are displayed to six decimals; CSV outputs retain 15 significant digits. Blank CSV statistics mean unavailable, not zero.

| Metric | V0 | V1 |
| --- | --- | --- |
| signal_count | 332.000000 | 57.000000 |
| average_stock_return_pct | 0.356529 | 0.629587 |
| average_spy_return_pct | 0.745371 | 0.274119 |
| average_excess_return_pp | -0.388842 | 0.355467 |
| median_excess_return_pp | -0.259629 | -0.456418 |
| hit_rate_pct | 48.493976 | 47.368421 |
| positive_stock_return_pct | 50.903614 | 49.122807 |
| q25_excess_return_pp | -4.791084 | -4.609197 |
| q75_excess_return_pp | 3.626756 | 3.979292 |
| std_excess_return_pp | 7.070080 | 7.860473 |
| best_excess_return_pp | 43.096432 | 28.908575 |
| worst_excess_return_pp | -30.536809 | -18.308160 |
| best_stock_return_pct | 45.009966 | 31.048371 |
| worst_stock_return_pct | -31.060655 | -19.645297 |
| sum_excess_return_pp_not_portfolio | -129.095427 | 20.261630 |
| detected_signals | 343.000000 | 62.000000 |
| pending_signals | 11.000000 | 5.000000 |
| missing_outcome_signals | 0.000000 | 0.000000 |
| atr_classification_unavailable | 0.000000 | 0.000000 |

## V1 minus V0

| average_excess_return_pp | median_excess_return_pp | hit_rate_pct | signals_removed | signal_reduction_pct | signal_retention_pct |
| --- | --- | --- | --- | --- | --- |
| 0.744309 | -0.196789 | -1.125555 | 275 | 82.831325 | 17.168675 |

The mean improves by +0.744309 pp; the median worsens by −0.196789 pp and hit rate by −1.125555 percentage points. The filter retains 17.168675% of completed V0 signals. On detected signals including pending events, it retains 62 of 343 and removes 281 (81.924198%); the primary count comparison is based on completed outcomes only.

V1's average stock return increases only about 0.273057 pp, while its matched SPY average is about 0.471251 pp lower. SPY's two averages differ because the filter selects different stock-signal dates. These are signal-weighted benchmark returns, not SPY's return over the whole year; the difference helps explain the larger excess-return change.

## Distribution and individual outcomes

V0's middle 50% spans −4.791084 to +3.626756 pp; V1's spans −4.609197 to +3.979292 pp. Both medians are negative. V1's dispersion is larger (7.860473 versus 7.070080 pp sample standard deviation). The mean therefore does not describe a typical successful signal or a uniform distributional improvement.

| version | outcome | ticker | signal_date | entry_date | exit_date | stock_return_pct | spy_return_pct | excess_return_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V0 | best_excess | AMD | 2025-09-25 | 2025-09-26 | 2025-10-10 | 45.009966 | 1.913534 | 43.096432 |
| V0 | worst_excess | IBM | 2026-07-06 | 2026-07-07 | 2026-07-21 | -31.060655 | -0.523845 | -30.536809 |
| V0 | best_stock | AMD | 2025-09-25 | 2025-09-26 | 2025-10-10 | 45.009966 | 1.913534 | 43.096432 |
| V0 | worst_stock | IBM | 2026-07-06 | 2026-07-07 | 2026-07-21 | -31.060655 | -0.523845 | -30.536809 |
| V1 | best_excess | QCOM | 2026-04-16 | 2026-04-17 | 2026-05-01 | 31.048371 | 2.139796 | 28.908575 |
| V1 | worst_excess | MU | 2026-03-18 | 2026-03-19 | 2026-04-02 | -19.645297 | -1.337138 | -18.308160 |
| V1 | best_stock | QCOM | 2026-04-16 | 2026-04-17 | 2026-05-01 | 31.048371 | 2.139796 | 28.908575 |
| V1 | worst_stock | MU | 2026-03-18 | 2026-03-19 | 2026-04-02 | -19.645297 | -1.337138 | -18.308160 |

The best V1 event is QCOM's 2026-04-16 signal, +28.908575 pp excess return. Removing that single event from V1 as an influence diagnostic changes its mean to −0.154410 pp (56 events). The reported headline remains +0.355467 pp with all 57 events. This diagnostic does not authorize discarding the event or selecting rules around it. Large positive and negative events warrant independent data review before interpreting them as economic effects.

Excess-return empirical distributions (generated chart not distributed; local path: `output/v0_v1_distribution.png`)

The curves show cumulative shares on their full observed ranges, without a fitted distribution or tail trimming. V0 includes V1; the curves are not independent samples.

## Monthly signal cohorts

| signal_month | V0_signal_count | V0_average_excess_return_pp | V1_signal_count | V1_average_excess_return_pp |
| --- | --- | --- | --- | --- |
| 2025-09 | 17 | 3.380385 | 1 | 17.998463 |
| 2025-10 | 40 | -0.764458 | 0 | n/a |
| 2025-11 | 20 | 0.269904 | 2 | -0.713264 |
| 2025-12 | 39 | 1.524051 | 16 | 1.054244 |
| 2026-01 | 30 | 3.015318 | 7 | 0.039973 |
| 2026-02 | 18 | -2.937221 | 1 | 4.452933 |
| 2026-03 | 21 | -2.255174 | 5 | -3.702202 |
| 2026-04 | 39 | -2.520774 | 6 | 1.708864 |
| 2026-05 | 25 | -0.094103 | 3 | -0.418153 |
| 2026-06 | 23 | -0.036022 | 0 | n/a |
| 2026-07 | 30 | -2.789023 | 3 | 5.235476 |
| 2026-08 | 30 | -0.862956 | 13 | -1.854238 |
| 2026-09 | 0 | n/a | 0 | n/a |

September 2025 is a partial beginning month. August 2026 ends at the last mature signal date. September 2026 has no completed outcomes. A zero count is not a zero-return month. V1 has a higher monthly mean in only 4 of the 10 months with completed observations in both groups. Several V1 month counts are just 1–3; do not treat these as reliable monthly effects.

The largest positive V1 contribution months are September 2025 (one signal, about +17.998463 pp summed excess) and December 2025 (16 signals, about +16.867907 pp summed excess). Together their summed contribution exceeds V1's net total because other months offset it. Excluding those same two months from both groups, solely as a concentration diagnostic, leaves V1 at −0.365119 pp (40 signals) and V0 at −0.891304 pp (276 signals). Thus the positive sign of V1's mean is sensitive to these months, but its relative mean advantage persists in that diagnostic.

Removing any single month leaves V1's mean above V0's. Its positive mean becomes very small when September 2025, December 2025, or July 2026 is individually omitted. This supports caution about the level and tails, not a claim that one month alone explains the entire relative mean difference.

Monthly cohorts (generated chart not distributed; local path: `output/v0_v1_monthly.png`)

## Sector consistency

| sector | V0_signal_count | V0_average_excess_return_pp | V1_signal_count | V1_average_excess_return_pp |
| --- | --- | --- | --- | --- |
| Communication Services | 38 | -2.074835 | 7 | -1.276690 |
| Consumer Discretionary | 47 | -0.526415 | 5 | 0.632160 |
| Consumer Staples | 28 | -1.696764 | 2 | -5.938564 |
| Energy | 25 | 1.686682 | 6 | 5.394960 |
| Financials | 33 | 0.850125 | 2 | -0.187888 |
| Health Care | 35 | 0.536411 | 2 | -0.658872 |
| Industrials | 42 | -0.839305 | 6 | -4.808591 |
| Information Technology | 84 | -0.377924 | 27 | 1.336670 |

Information Technology contributes 27 of 57 V1 signals (47.368421%), compared with 84 of 332 V0 signals (25.301205%). Excluding that same sector from both groups changes the remaining means to V1 −0.527616 pp (30 signals) versus V0 −0.392540 pp (248 signals), reversing the mean ordering by −0.135076 pp. The apparent aggregate advantage is therefore sensitive to IT composition.

Energy has the strongest V1 sector mean, +5.394960 pp, from only six events. Without Energy, V1's mean becomes −0.237414 pp versus V0 −0.557858 pp: its positive sign disappears, although the relative advantage remains. Information Technology and Energy provide positive contributions that offset substantial negative contributions elsewhere, notably Industrials. V1 sector samples range from 2 to 27; even the largest is limited and dependent. All sector rows are shown, with sparse samples explicitly treated as descriptive only.

## Stock concentration

Most V0 signals: NVDA, AVGO, ETN, MRK and IBM tie at nine each. Most V1 signals: AMD, QCOM and MU tie at four each; IBM and AMAT follow at three each. Counts below include only complete outcomes.

Largest positive summed excess contributions: V0 — AMD +60.150191 pp, AMAT +30.953553 pp, QCOM +23.270164 pp, XOM +20.731276 pp, MU +17.561763 pp. V1 — QCOM +31.241333 pp, AMD +19.166693 pp, XOM +18.708027 pp, TSLA +11.803365 pp, CVX +8.316858 pp.

Largest negative summed excess contributions: V0 — IBM −46.305842 pp, ORCL −40.597093 pp, META −39.048234 pp, WMT −27.768010 pp, AVGO −26.183430 pp. V1 — RTX −15.776880 pp, NKE −10.309093 pp, META −9.151811 pp, MSFT −9.058891 pp, CAT −8.150876 pp.

These sums are additive diagnostics over overlapping events, NOT portfolio returns or compounded wealth. A stock's contribution to the overall mean is its summed excess divided by the whole strategy sample count. Removing QCOM as a diagnostic makes V1's mean −0.207164 pp; removing AMD or XOM leaves means of about +0.020659 or +0.028247 pp. These results identify influence, not stocks to drop.

The largest V1 count on any one signal date is three, occurring on 2026-01-05, 2026-08-17 and 2026-08-21. Low same-date counts do not make overlapping ten-interval outcomes independent.

The following complete stock table retains every stock, including those with no V1 signals. Zero summed contribution for an empty group is an additive identity; its mean remains unavailable.

| ticker | V0_signal_count | V1_signal_count | V0_average_excess_return_pp | V1_average_excess_return_pp | V0_sum_excess_return_pp_not_portfolio | V1_sum_excess_return_pp_not_portfolio |
| --- | --- | --- | --- | --- | --- | --- |
| AAPL | 4 | 0 | 0.295129 | n/a | 1.180517 | 0.000000 |
| MSFT | 8 | 2 | -3.029579 | -4.529445 | -24.236635 | -9.058891 |
| NVDA | 9 | 2 | -1.090017 | 1.744502 | -9.810155 | 3.489003 |
| AMZN | 7 | 2 | 1.096656 | 0.833264 | 7.676589 | 1.666527 |
| GOOGL | 5 | 1 | 0.880066 | 2.632197 | 4.400330 | 2.632197 |
| META | 8 | 2 | -4.881029 | -4.575906 | -39.048234 | -9.151811 |
| AVGO | 9 | 2 | -2.909270 | -1.534969 | -26.183430 | -3.069937 |
| AMD | 6 | 4 | 10.025032 | 4.791673 | 60.150191 | 19.166693 |
| ORCL | 7 | 2 | -5.799585 | -3.494713 | -40.597093 | -6.989427 |
| CRM | 6 | 0 | -2.471211 | n/a | -14.827266 | 0.000000 |
| JPM | 5 | 0 | -0.704174 | n/a | -3.520869 | 0.000000 |
| BAC | 5 | 0 | 1.559637 | n/a | 7.798186 | 0.000000 |
| GS | 5 | 1 | 0.701851 | 1.205253 | 3.509256 | 1.205253 |
| MS | 5 | 1 | 0.961049 | -1.581030 | 4.805243 | -1.581030 |
| V | 6 | 0 | 0.986202 | n/a | 5.917214 | 0.000000 |
| MA | 7 | 0 | 1.363587 | n/a | 9.545108 | 0.000000 |
| XOM | 5 | 2 | 4.146255 | 9.354014 | 20.731276 | 18.708027 |
| CVX | 7 | 1 | 2.102272 | 8.316858 | 14.715905 | 8.316858 |
| COP | 7 | 1 | 0.812308 | 3.182668 | 5.686155 | 3.182668 |
| SLB | 6 | 2 | 0.172287 | 1.081102 | 1.033725 | 2.162204 |
| CAT | 7 | 2 | 2.328843 | -4.075438 | 16.301900 | -8.150876 |
| GE | 6 | 0 | 0.732830 | n/a | 4.396983 | 0.000000 |
| RTX | 6 | 1 | -1.972124 | -15.776880 | -11.832742 | -15.776880 |
| ETN | 9 | 2 | -0.664587 | -2.362867 | -5.981283 | -4.725734 |
| HON | 6 | 1 | -3.993689 | -0.198058 | -23.962136 | -0.198058 |
| DE | 8 | 0 | -1.771690 | n/a | -14.173521 | 0.000000 |
| WMT | 7 | 1 | -3.966859 | -6.867589 | -27.768010 | -6.867589 |
| COST | 6 | 0 | -2.395585 | n/a | -14.373510 | 0.000000 |
| HD | 7 | 0 | -0.904310 | n/a | -6.330173 | 0.000000 |
| MCD | 7 | 0 | 0.271637 | n/a | 1.901462 | 0.000000 |
| NKE | 6 | 1 | -3.355270 | -10.309093 | -20.131617 | -10.309093 |
| SBUX | 8 | 0 | 0.976961 | n/a | 7.815685 | 0.000000 |
| LLY | 7 | 0 | 2.205997 | n/a | 15.441982 | 0.000000 |
| UNH | 5 | 1 | 3.485818 | 4.452933 | 17.429090 | 4.452933 |
| JNJ | 7 | 0 | -0.502225 | n/a | -3.515574 | 0.000000 |
| ABBV | 7 | 1 | -2.691253 | -5.770677 | -18.838769 | -5.770677 |
| MRK | 9 | 0 | 0.917517 | n/a | 8.257653 | 0.000000 |
| NFLX | 7 | 0 | -3.631147 | n/a | -25.418032 | 0.000000 |
| DIS | 7 | 1 | -0.785737 | 4.139613 | -5.500158 | 4.139613 |
| T | 5 | 2 | -3.269342 | -3.282805 | -16.346711 | -6.565611 |
| VZ | 6 | 1 | 0.511515 | 0.008786 | 3.069089 | 0.008786 |
| TSLA | 5 | 2 | -1.189628 | 5.901682 | -5.948140 | 11.803365 |
| QCOM | 6 | 4 | 3.878361 | 7.810333 | 23.270164 | 31.241333 |
| TXN | 7 | 1 | -0.414481 | -6.334127 | -2.901365 | -6.334127 |
| IBM | 9 | 3 | -5.145094 | -0.587377 | -46.305842 | -1.762132 |
| AMAT | 7 | 3 | 4.421936 | 1.977574 | 30.953553 | 5.932721 |
| MU | 6 | 4 | 2.926961 | 0.868715 | 17.561763 | 3.474859 |
| LOW | 7 | 0 | -1.389330 | n/a | -9.725311 | 0.000000 |
| PEP | 8 | 1 | -0.582262 | -5.009539 | -4.658094 | -5.009539 |
| KO | 7 | 0 | -0.101396 | n/a | -0.709773 | 0.000000 |

## Classification and limits

**MIXED.** The primary mean improves, but the median, hit rate, absolute-positive rate and sample size move unfavorably, while dispersion increases. The favorable mean depends on influential events and sector composition. No numerical economic-materiality threshold or statistical test was preregistered, so neither significance nor a validated edge is claimed.

The experiment uses one recent year, a selected fixed universe, retrospective Yahoo prices, one documented source repair, static sector labels, idealized opening prints, and gross outcomes without execution costs. V1 is a nested subset of V0 and events overlap. The 57 V1 signals are not 57 independent trials. The same period is now observed and must not later be described as untouched out-of-sample evidence.

Next proposed stage, not run here: independently audit influential price events, then challenge whether the relative result survives comparisons that account for sector/date composition and dependence. Keep the frozen signal unchanged. No V2, threshold search, parameter changes, or recommendation to trade.

## Reproducibility and output files

Evaluator: analysis/first_comparison.py. Synthetic reporting tests: analysis/test_first_comparison.py. Existing first-pass outputs cannot be overwritten by its command. Primary CSVs: output/v0_v1_summary.csv, output/v0_v1_monthly.csv, output/v0_v1_sector.csv, output/v0_v1_signals.csv. Additional diagnostics: output/v0_v1_difference.csv, output/v0_v1_stocks.csv, output/v0_v1_dates.csv, output/v0_v1_extremes.csv, output/v0_v1_influence.csv. The signals file retains pending events, membership flags, inclusion flags, and original fractional return columns. Aggregated CSV return units are explicitly pct/pp.

The evaluation manifest records the timestamp, frozen manifest/lock hashes, evaluator hash, percentile/dispersion conventions, and verification status. FIRST_PASS_RESULTS.md and the appended research-log entry provide a public-safe narrative and complete stock/month/sector results; vendor and generated data files remain gitignored under the existing publication policy.
