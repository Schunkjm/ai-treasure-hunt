# V1 adversarial robustness review

Date: 2026-09-08. **Overall classification: FRAGILE.** The official first-pass classification remains **MIXED**, and its 57-event V1 mean remains +0.355467 pp, median −0.456418 pp and hit rate 47.368421%. No parameter, universe, signal, data snapshot or official result was changed. No V2 was created.

The strongest explanation for a positive mean alongside a negative median and sub-50% hit rate is the magnitude of a few right-tail outcomes. The positive sum is a small remainder after large gains and losses offset. Stress tests are descriptive, selected after viewing first-pass results, and cannot supply independent confirmation, causal explanation or corrected significance.

## Methods and data integrity

Use exactly the 57 completed official V1 events, with V0's 332 completed events for execution comparisons. Pending signals remain excluded. Rank best/worst by excess return, with stock, SPY and excess shown separately. Individual event outcomes are equally weighted. All aggregate excess units are percentage points (pp); event CSV return fields retain fractions. Contribution means arithmetic sum of event excess returns, not a compounded or investable portfolio. Percentages of the net sum can exceed 100% because negative contributions offset winners.

The saved first-pass outputs and all frozen hashes passed before and after diagnostics. The original loader independently reconciles all official stock/SPY returns to adjusted endpoint opens. V1 indicators were recomputed over the full frozen histories, and ATR% and qualifying membership checked. All execution alternatives use matching stock/SPY dates and fields. Two new overlap boundary tests and three existing reporting tests passed. This verifies internal arithmetic and provenance, not whether Yahoo's extreme price moves are economically correct; no independent feed, exchange print or event-news audit was performed. The existing KO correction is untouched and KO has zero V1 events.

## 1. Largest winners and losers

Five best and five worst V1 excess-return observations:

| Ticker | Signal | Entry | Exit | Stock % | SPY % | Excess pp |
| --- | --- | --- | --- | --- | --- | --- |
| QCOM | 2026-04-16 | 2026-04-17 | 2026-05-01 | 31.048371 | 2.139796 | 28.908575 |
| AMAT | 2025-09-15 | 2025-09-16 | 2025-09-30 | 18.497042 | 0.498579 | 17.998463 |
| MU | 2026-04-15 | 2026-04-16 | 2026-04-30 | 16.950724 | 1.935639 | 15.015085 |
| MU | 2025-12-08 | 2025-12-09 | 2025-12-23 | 12.855331 | 0.408528 | 12.446803 |
| XOM | 2026-07-14 | 2026-07-15 | 2026-07-29 | 8.704942 | -1.891973 | 10.596915 |
| ETN | 2025-12-11 | 2025-12-12 | 2025-12-29 | -7.683945 | 0.203677 | -7.887621 |
| NKE | 2026-04-27 | 2026-04-28 | 2026-05-12 | -6.787132 | 3.521961 | -10.309093 |
| AMAT | 2026-08-12 | 2026-08-13 | 2026-08-27 | -12.170901 | -0.822073 | -11.348828 |
| RTX | 2026-04-14 | 2026-04-15 | 2026-04-29 | -13.512979 | 2.263900 | -15.776880 |
| MU | 2026-03-18 | 2026-03-19 | 2026-04-02 | -19.645297 | -1.337138 | -18.308160 |

Tail conventions were stated before this diagnostic calculation: ceil(5% × 57) = 3 events (5.263% of the sample). Excluding the best/worst 5% therefore equals excluding three. Winsorization caps those three at the fourth-best/fourth-worst observed excess return. Only excess is capped; synthetic capped stock/SPY metrics are intentionally blank. Also show exclusion of five events for the requested top-five contribution context. The two sides are treated symmetrically; deleting losses predictably improves the average and is not evidence of a better strategy.

| diagnostic | signal_count | average_excess_return_pp | median_excess_return_pp | hit_rate_pct |
| --- | --- | --- | --- | --- |
| official | 57 | 0.355467 | -0.456418 | 47.368421 |
| exclude_best_1 | 56 | -0.154410 | -0.487414 | 46.428571 |
| exclude_best_3 | 54 | -0.771491 | -0.521277 | 44.444444 |
| exclude_best_5 | 52 | -1.244312 | -0.620528 | 42.307692 |
| winsorize_best_5pct_3_events | 57 | -0.075791 | -0.456418 | 47.368421 |
| exclude_worst_1 | 56 | 0.688746 | -0.327238 | 48.214286 |
| exclude_worst_3 | 54 | 1.216583 | -0.094636 | 50.000000 |
| exclude_worst_5 | 52 | 1.613312 | 0.092657 | 51.923077 |
| winsorize_worst_5pct_3_events | 57 | 0.609969 | -0.456418 | 47.368421 |

Removing the best event changes the mean by −0.509877 pp, to −0.154410 pp. Removing the best three changes it by −1.126958 pp, to −0.771491 pp. Capping the best three, rather than deleting them, also makes the mean negative (−0.075791 pp). The downside equivalents are +0.688746 pp after removing the worst one, +1.216583 pp after the worst three, and +0.609969 pp after bottom-tail capping. Tail sensitivity is substantial in both directions.

## 2. Contribution concentration

Net summed V1 excess contribution is +20.261630 pp. Shares below use that net denominator, not gross positive returns:

| best_n | sum_excess_pp | percent_of_net_sum |
| --- | --- | --- |
| 1 | 28.908575 | 142.676453 |
| 3 | 61.922124 | 305.612742 |
| 5 | 84.965842 | 419.343563 |

The best three are QCOM, AMAT and MU; two of those signals are only one session apart (April 15–16, 2026). The three best contribute +61.922124 pp while the remaining 54 contribute −41.660494 pp. One observation contributes more than the entire positive net result. This is strong descriptive evidence of dependence on a few large winners, not proof that those winners are erroneous.

## 3. Month and calendar concentration

| signal_month | signal_count | average_excess_return_pp | sum_excess_return_pp_not_portfolio |
| --- | --- | --- | --- |
| 2025-09 | 1 | 17.998463 | 17.998463 |
| 2025-10 | 0 | n/a | 0.000000 |
| 2025-11 | 2 | -0.713264 | -1.426529 |
| 2025-12 | 16 | 1.054244 | 16.867907 |
| 2026-01 | 7 | 0.039973 | 0.279809 |
| 2026-02 | 1 | 4.452933 | 4.452933 |
| 2026-03 | 5 | -3.702202 | -18.511010 |
| 2026-04 | 6 | 1.708864 | 10.253186 |
| 2026-05 | 3 | -0.418153 | -1.254460 |
| 2026-06 | 0 | n/a | 0.000000 |
| 2026-07 | 3 | 5.235476 | 15.706427 |
| 2026-08 | 13 | -1.854238 | -24.105096 |
| 2026-09 | 0 | n/a | 0.000000 |

December has the most signals (16/57, 28.07%); August has 13/57 (22.81%). Together they account for 50.88% of V1. September's single AMAT event contributes +17.998463 pp (88.83% of the net aggregate), December +16.867907 pp (83.25%), and July +15.706427 pp (77.52%). No single month exclusively supplies the positive result: removing any one month leaves V1 positive. However, removing September and December together leaves −0.365119 pp; V0 with those same months removed is −0.891304 pp. Thus the positive level is fragile while the relative mean advantage survives that particular attack. March and August supply substantial negative contributions.

Five-session windows are descriptive rolling windows, not optimized partitions. Their overlaps mean they must not be added together. Largest examples: December 29–January 5 has seven signals in seven stocks; August 12–18 has seven in seven stocks; August 17–21 has seven in six stocks. Same-date counts peak at three (January 5, August 17 and August 21). The full date and rolling-window files show membership.

The April 15 MU and April 16 QCOM winners hold for nine shared open-to-open intervals. RTX's April 14 loss overlaps those same dates. These are simultaneous exposures, and MU/QCOM share the frozen IT sector; a particular common news catalyst cannot be established from OHLCV and dates alone. Broad market and industry influences can affect several outcomes at once, even after subtracting SPY.

## 4. Sector concentration

| sector | signal_count | average_excess_return_pp | sum_excess_return_pp_not_portfolio |
| --- | --- | --- | --- |
| Communication Services | 7 | -1.276690 | -8.936827 |
| Consumer Discretionary | 5 | 0.632160 | 3.160799 |
| Consumer Staples | 2 | -5.938564 | -11.877128 |
| Energy | 6 | 5.394960 | 32.369758 |
| Financials | 2 | -0.187888 | -0.375777 |
| Health Care | 2 | -0.658872 | -1.317745 |
| Industrials | 6 | -4.808591 | -28.851547 |
| Information Technology | 27 | 1.336670 | 36.090096 |

IT supplies 27/57 events (47.37%) and +36.090096 pp, 178.12% of the net aggregate. Energy supplies six events and +32.369758 pp, 159.76% of net. All other sectors combined contribute −48.198224 pp. Removing IT leaves V1 −0.527616 pp, below V0's corresponding −0.392540 pp. Removing Energy leaves V1 −0.237414 pp, although still above corresponding V0 −0.557858 pp. There is concentration in two favorable sectors, rather than broad sector confirmation. Sector counts of 2–27 are too sparse and dependent to establish sector-specific effects.

## 5. Stock concentration

All 50 frozen stocks are retained below. Zero-event mean is unavailable; a zero sum is only an additive identity. No stock has more than four V1 signals, so every stock mean is descriptive arithmetic, not a reliable estimate of a stock-specific effect.

| ticker | signal_count | average_excess_return_pp | sum_excess_return_pp_not_portfolio |
| --- | --- | --- | --- |
| AAPL | 0 | n/a | 0.000000 |
| MSFT | 2 | -4.529445 | -9.058891 |
| NVDA | 2 | 1.744502 | 3.489003 |
| AMZN | 2 | 0.833264 | 1.666527 |
| GOOGL | 1 | 2.632197 | 2.632197 |
| META | 2 | -4.575906 | -9.151811 |
| AVGO | 2 | -1.534969 | -3.069937 |
| AMD | 4 | 4.791673 | 19.166693 |
| ORCL | 2 | -3.494713 | -6.989427 |
| CRM | 0 | n/a | 0.000000 |
| JPM | 0 | n/a | 0.000000 |
| BAC | 0 | n/a | 0.000000 |
| GS | 1 | 1.205253 | 1.205253 |
| MS | 1 | -1.581030 | -1.581030 |
| V | 0 | n/a | 0.000000 |
| MA | 0 | n/a | 0.000000 |
| XOM | 2 | 9.354014 | 18.708027 |
| CVX | 1 | 8.316858 | 8.316858 |
| COP | 1 | 3.182668 | 3.182668 |
| SLB | 2 | 1.081102 | 2.162204 |
| CAT | 2 | -4.075438 | -8.150876 |
| GE | 0 | n/a | 0.000000 |
| RTX | 1 | -15.776880 | -15.776880 |
| ETN | 2 | -2.362867 | -4.725734 |
| HON | 1 | -0.198058 | -0.198058 |
| DE | 0 | n/a | 0.000000 |
| WMT | 1 | -6.867589 | -6.867589 |
| COST | 0 | n/a | 0.000000 |
| HD | 0 | n/a | 0.000000 |
| MCD | 0 | n/a | 0.000000 |
| NKE | 1 | -10.309093 | -10.309093 |
| SBUX | 0 | n/a | 0.000000 |
| LLY | 0 | n/a | 0.000000 |
| UNH | 1 | 4.452933 | 4.452933 |
| JNJ | 0 | n/a | 0.000000 |
| ABBV | 1 | -5.770677 | -5.770677 |
| MRK | 0 | n/a | 0.000000 |
| NFLX | 0 | n/a | 0.000000 |
| DIS | 1 | 4.139613 | 4.139613 |
| T | 2 | -3.282805 | -6.565611 |
| VZ | 1 | 0.008786 | 0.008786 |
| TSLA | 2 | 5.901682 | 11.803365 |
| QCOM | 4 | 7.810333 | 31.241333 |
| TXN | 1 | -6.334127 | -6.334127 |
| IBM | 3 | -0.587377 | -1.762132 |
| AMAT | 3 | 1.977574 | 5.932721 |
| MU | 4 | 0.868715 | 3.474859 |
| LOW | 0 | n/a | 0.000000 |
| PEP | 1 | -5.009539 | -5.009539 |
| KO | 0 | n/a | 0.000000 |

AMD, QCOM and MU tie at four signals each. QCOM contributes +31.241333 pp (154.19% of net); AMD +19.166693 pp (94.60%); XOM +18.708027 pp (92.33%). Removing QCOM's four signals leaves the other 53 with −0.207164 pp average excess. QCOM's best event accounts for most of that stock's contribution. Repeated stock identities matter, but the count leaders alone do not establish robustness: MU contains both the worst event and two of the best four. Largest negative stock totals are RTX −15.776880 pp, NKE −10.309093 pp and META −9.151811 pp.

## 6. Dependence and overlapping outcomes

Treat each holding period as the half-open interval [entry open, exit open). Shared exit/entry timestamps alone are not overlap. Count common trading open-to-open intervals for every unordered event pair:

| category | possible_pairs | overlapping_pairs | pair_overlap_pct | events_with_overlap |
| --- | --- | --- | --- | --- |
| same_stock | 36 | 2 | 5.555556 | 4 |
| different_stock | 1560 | 223 | 14.294872 | 56 |
| all | 1596 | 225 | 14.097744 | 56 |

56/57 events (98.25%) overlap at least one other stock's event. Two within-stock pairs overlap: NVDA by one interval and CAT by six. These involve four events (7.02% of 57); the 5.56% within-stock pair statistic has a different denominator, 36 possible same-stock pairs. Across stocks, 223/1,560 pairs overlap. Pair frequencies do not estimate an effective sample size.

Concurrent exposure peaks at 11 events: December 17 (11 stocks, four sectors), January 13 (11 stocks, five sectors), and August 24–26 (11 events, ten stocks, five sectors). Several nominal observations therefore reuse the same days and market shocks. A shared benchmark subtraction removes the same benchmark return, not every common exposure, beta difference or industry shock. Even non-overlapping events can share a regime. Fifty-seven outcomes cannot be treated as 57 independent experiments; no p-value, independence correction or effective sample size is manufactured.

## 7. Execution sensitivity

Same signals and completed cohort, matching SPY endpoints in every case. Official: entry O(t+1), exit O(t+11). First diagnostic changes entry only to C(t+1), preserving O(t+11) exit; this shortens exposure by the entry session. Second diagnostic uses C(t+1) to C(t+11), preserving ten close-to-close intervals. Neither changes the signal or official rule.

| version | convention | signal_count | average_excess_return_pp | median_excess_return_pp | hit_rate_pct |
| --- | --- | --- | --- | --- | --- |
| V0 | official_open_open | 332 | -0.388842 | -0.259629 | 48.493976 |
| V0 | next_close_original_exit_open | 332 | -0.325434 | -0.487282 | 46.987952 |
| V0 | next_close_t11_close | 332 | -0.334850 | -0.347611 | 46.987952 |
| V1 | official_open_open | 57 | 0.355467 | -0.456418 | 47.368421 |
| V1 | next_close_original_exit_open | 57 | 0.778858 | -0.293705 | 49.122807 |
| V1 | next_close_t11_close | 57 | 1.154423 | -0.039573 | 49.122807 |

This attack does NOT support dependence on favorable next-open execution: V1's mean rises to +0.778858 pp with the original exit open and +1.154423 pp with a matched exit close. V1−V0 mean differences rise from +0.744309 pp to +1.104292 and +1.489273 pp. Both alternative V1 medians remain negative and hit rates remain below 50%. Opening/closing prints are still idealized; no slippage, spreads, costs, capacity or executable fill study is included. The favorable alternative is not selected or recommended.

## 8. What the ATR rule selects

For each V1 date t, let p be the earliest maximum ATR% date among the prior 20 sessions. Exact identity: ATR%(t)/ATR%(p) = [ATR(t)/ATR(p)] / [Close(t)/Close(p)]. “Raw ATR” here means the absolute-price ATR computed from the frozen adjusted OHLC, before dividing by Close, not an unadjusted vendor series. These diagnostic flags overlap and are not new signal definitions.

- **Single-maximum dependence:** remove one maximum observation, use the second-largest prior ATR%, and ask whether the existing 0.80 rule would fail. This happens for 7/57 (12.28%). It measures numerical dependence on one point; it does not prove an unusual one-day volatility shock, since Wilder ATR is smoothed.
- **Price-denominator assistance:** 23/57 (40.35%) have ATR(t)/ATR(p) > 0.80 but pass after dividing by a higher price ratio. Price appreciation is necessary for the full 20% ratio decline in those cases. Nevertheless ATR itself declined in ALL 57; none is purely a price-rise case with flat or rising ATR relative to p.
- **Absolute ATR decline:** 34/57 (59.65%) have at least a 20% ATR decline from the reference peak without needing a rising-price denominator. The peak's median age is 16 sessions (range 8–20), so the rule often compares with an old high.
- **Broader-window diagnostic:** compare median absolute ATR over t−4 through t with the first five sessions of the prior window (t−20 through t−16). It declines in 52/57 (91.23%); it declines at least 20% in 20/57 (35.09%). The other five show no median decline despite passing the max-based rule. These five-session summaries were added for description, not optimized or used to admit signals.

Volatility decline is therefore common in the measured ATR series. The rule is not predominantly a single-point or purely price-denominator artifact. But peak-to-current contraction does not guarantee persistently low volatility, a quiet regime, or any causal connection to subsequent excess returns. Price and numerator contributions are algebraically linked; these observations cannot identify economic causation. No alternative ATR lookback or threshold was tested.

## Robustness scorecard

Ratings are qualitative post-result judgments, not preregistered numerical acceptance criteria. PASS means this particular attack did not reveal the proposed failure, not proof of a trading edge.

| Category | Rating | Reason |
| --- | --- | --- |
| Data integrity | PASS | Frozen hashes, original outputs, endpoints and signal calculations reconcile. Internal integrity only; no independent vendor confirmation. |
| Outlier dependence | FAIL | Removing one winner turns the mean negative; top-three capping also turns it negative. |
| Stock concentration | FAIL | QCOM alone contributes more than the net total; removing that stock makes the mean negative. |
| Sector concentration | FAIL | IT and Energy each exceed the net total; removing either makes V1 negative. |
| Date/regime concentration | CAUTION | Large December/August cohorts, influential sparse months and only one year. |
| Observation dependence | CAUTION | 56/57 events overlap another; independence is unjustified and no inference is claimed. |
| Execution sensitivity | PASS | Both requested next-close diagnostics retain and increase the positive mean; fill realism remains untested. |
| ATR mechanism | CAUTION | Real ATR declines are common, but price normalization and an old maximum materially affect selection. |

**Overall: FRAGILE.** The positive mean fails simple outlier and concentration attacks. Execution and ATR checks do not support every proposed skeptical explanation, so neither a universal failure claim nor a causal story is justified. The original MIXED result remains intact.

Remaining limits: one observed year, selected static universe/sectors, overlapping and regime-related events, revised vendor history, no independent price-event verification, idealized gross fills, and post-result diagnostic selection. These tests do not estimate future performance or establish statistical significance. The year is no longer untouched evidence.

Next lesson, without creating V2: a higher mean must be distinguished from typical-event improvement and broad independent support. Before another hypothesis is tested, specify how concentration, common exposure and numerator-versus-price effects will be judged, and preserve genuinely unobserved evidence. No new strategy or parameter is proposed here.

## Artifacts and preservation

All new diagnostic CSVs, a single outlier chart and their hashes are in output/robustness/. analysis/robustness.py performs calculations; analysis/test_robustness.py tests overlap boundaries; this report and RESEARCH_LOG.md record the complete findings. Original output/v0_v1_* files and frozen files remain hash-identical. No data download or frozen pipeline rewrite was performed.
