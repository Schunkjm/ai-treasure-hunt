# Research decision gate — retain signals, do not promote a strategy

Decision date: 2026-09-08.

**D. DO NOT PROMOTE A STRATEGY — KEEP V0/V1 AS RESEARCH SIGNALS.**

This decision uses only the evidence already generated. No new data, return calculation, indicator, subgroup search, optimization or strategy version was introduced. Prospective tracking has not begun. V0/V1 and their original results remain unchanged.

## Supported by the evidence

| Stage | Documented observation | Bounded conclusion |
| --- | --- | --- |
| V0: GitHub-derived strict bullish SMA10/SMA20 crossover | 332 completed events; mean excess −0.388842 pp; median −0.259629 pp; hit rate 48.493976% | An understandable, reproducible research baseline; this sample does not justify promotion. GitHub adoption is not investment edge. |
| V1: human-origin, preregistered ATR contraction | 57 completed events; mean excess +0.355467 pp; median −0.456418 pp; hit rate 47.368421% | The filter improves the mean by +0.744309 pp but worsens median and hit rate while removing 82.83% of completed signals. First-pass classification remains MIXED. |
| V1 robustness | Mean becomes −0.154410 pp without the best event and −0.771491 pp without the best three; outlier, stock and sector concentration checks fail | The positive mean is FRAGILE. A few large gains outweigh more frequent underperformance. Diagnostic exclusions do not replace the official result. |
| Long-term-trend diagnostic | Above a rising SMA200: 33 events; mean −0.462757 pp; median −0.716914 pp; hit rate 45.454545%; four of five worst losses | WEAK RATIONALE for the exact proposed trend addition. The human idea was coherent but did not explain away the losses. It will not be promoted to V2. |
| Observation dependence | 56 of 57 V1 events overlap another stock's holding period; two same-stock pairs overlap | The 57 observations are not automatically 57 independent experiments. Common dates, sectors and regimes limit information in the sample. |

These are equal-event-weighted, gross, ten-trading-interval excess returns against SPY, not portfolio returns. The studied signal window is 2025-09-08 through 2026-09-08, with only mature outcomes included. Pending events were not treated as zeros or failures.

The skeptical review did not support every proposed failure story: next-close execution diagnostics increased V1's mean, and absolute ATR declined from the reference peak in every V1 event. Those findings remain part of the record. Internal integrity checks passed, but they do not independently verify vendor prices or prove economic validity.

## Not supported by the evidence

- Calling V0 or V1 a validated, statistically established or implementable trading edge.
- Calling V1 broadly better solely because its primary mean improved, or calling V0 superior simply because V1 is fragile.
- Claiming that price above a rising SMA200 fixes V1, creating V2 from that diagnosis, or promoting the attractive three-event nonrising-trend subgroup.
- Treating GitHub popularity, a successful code test or an internally consistent data pipeline as evidence of profitability.
- Treating diagnostic deletions as permission to discard losing stocks, sectors or dates from the official record.
- Assuming a higher hit rate is necessary or sufficient for profitability. Here the negative median and lower hit rate weaken the claim of broad improvement; neither statistic alone decides whether an edge exists.
- Declaring the general SMA, ATR or trend concepts permanently disproven. This experiment is bounded by its period, universe and design.

## Still unknown

- Whether either unchanged signal has positive expected excess return on genuinely new data, and whether V1 has a reproducible incremental benefit over V0.
- Whether any effect persists across independent market periods and remains economically meaningful after realistic execution costs and risk exposure are considered.
- How much confidence is warranted after accounting for overlapping holdings, repeated stocks, shared sectors and market regimes. No defensible effective sample size or uncertainty interval was established here.
- Whether the influential vendor price events would survive independent price/corporate-action verification, and how revised history affects reproducibility.
- Whether a separately specified portfolio construction, sizing and execution process could turn event-level signals into an investable strategy. That has not been studied or authorized.
- What economic mechanism, if any, causes the observed differences. Descriptive subgroup comparisons do not identify causation.

## Decision and why stopping is success

Choose D. Neither signal has sufficient evidence for promotion, and the narrow follow-up supplied no persuasive reason to create V2. The project has succeeded at distinguishing a reproducible signal from demonstrated predictive value, exposing fragility, and documenting a plausible human idea that did not earn support.

**We explicitly chose not to manufacture a better backtest by continuing to search the same historical sample.** The previously examined year remains observed research data; changing its label or rerunning another filter cannot make it untouched evidence. Stopping preserves an honest negative/mixed result, the original hypotheses, useful infrastructure and the opportunity to learn prospectively. It prevents a research exercise from becoming repeated selection for a favorable answer.

This is a stop to modification and promotion, not proof that further learning is impossible. The retained artifacts are an auditable research case study and frozen signal definitions, not trading recommendations.

## Clean prospective experiment — proposed, not started

1. **Preregister before collection.** A later, explicitly authorized protocol should record its start date after registration, duration/end date, scheduled review dates, data-handling rules and decision criteria before any new outcomes are inspected. Select the duration and evidence target using a justified precision/power plan that allows for clustering; do not invent a magic raw signal count. Do not stop because cumulative performance first looks positive. No dates, numerical promotion thresholds or tracking automation are activated by this document.

2. **Carry forward both frozen hypotheses.** Retain the fixed 50-stock universe, SPY benchmark, Yahoo adjustment convention, strict crossover, ATR settings, timing and metrics. V0 requires SMA10(t−1) < SMA20(t−1) and SMA10(t) > SMA20(t). V1 adds ATR14(t)/Close(t) <= 0.80 times the maximum of that ratio over t−20 through t−1, using the frozen Wilder ATR definition. No SMA200 condition is added. Future operational calendar/history support must be isolated from the archived frozen snapshot, with sufficient warm-up and an auditable exchange calendar; it must not silently change signal definitions.

3. **Create an append-only, timestamped signal ledger.** After each completed market close, capture the available data snapshot, retrieval timestamp, code/specification hashes, quality status and both signals for every universe member. Record qualifying signals and indicator values before the next open and before their forward outcomes are known. Retain no-signal days and missing/late-data incidents for audit. Predefine an incident policy: a signal reconstructed late cannot be passed off as an on-time prospective call. Preserve original data and separately log corrections rather than rewriting the prediction history.

4. **Measure the identical outcomes.** Hypothetical entry remains O(t+1); exit remains O(t+11), ten open-to-open intervals later. Compute stock return O(t+11)/O(t+1)−1, identical-date SPY return, and their difference. Record actual available endpoint data after each endpoint occurs. Pending events stay pending; unavailable prices follow the preregistered missing-data policy. Previously observed historical signals, including their pending outcomes, remain in the original cohort and are not relabeled as new prospective signals.

5. **Accumulate and review without adaptation.** Keep each outcome linked to the earlier immutable signal record. Use the same equal-event-weighted mean excess as primary, with median, hit rate and sample size as secondary; show concentration and overlap diagnostics. Set review dates in advance and do not change the rule after individual wins, losses or disappointing reviews. Any future authorized change must be a distinct hypothesis with a new timestamp and new validation evidence, not a repaired V0/V1 history.

6. **Plan uncertainty and economic validation before making promotion claims.** The future analysis plan must account for V1 being nested inside V0 and for dependence across dates/stocks; do not use independent-sample reasoning by default. Specify an appropriate cluster-aware estimation method and sensitivity analyses before evaluating new outcomes. Preserve gross frozen metrics for comparability; any cost-adjusted layer should be separately preregistered, not substituted retrospectively for the official outcome. Promotion would also require data/event verification, realistic execution and cost assessment, risk/portfolio feasibility, and replication or further unobserved evidence sufficient to support an economically meaningful effect. A positive mean or a single favorable statistical test is insufficient.

What we could build later is a transparent prospective signal journal and evaluation dashboard, alongside an educational account of falsification and disciplined stopping. This stage only defines that possibility; it does not begin data acquisition, signal generation, tracking, paper trading or portfolio implementation.

## Evidence record and preservation

Sources are the existing project records only: FIRST_PASS_RESULTS.md, ROBUSTNESS_REPORT.md, LONG_TERM_TREND_DIAGNOSTIC.md and FROZEN_SPECIFICATION.md. Existing frozen inputs and original first-pass, robustness and trend output hashes were verified. RESEARCH_LOG.md and PROMPTS.md record this decision. No existing performance artifact was changed.
