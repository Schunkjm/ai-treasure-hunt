"""Publish the authorized robustness findings without changing official results."""
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analysis.first_comparison import ROOT, sha, EXCESS, STOCK, SPY
from src.frozen import verify_freeze

D=ROOT/'output/robustness'
def read(n): return pd.read_csv(D/(n+'.csv'))
def table(f):
    def fmt(v):
        if pd.isna(v): return 'n/a'
        if isinstance(v,(float,np.floating)): return f'{v:.6f}'
        return str(v)
    return '\n'.join(['| '+' | '.join(f.columns)+' |','| '+' | '.join(['---']*len(f.columns))+' |']+['| '+' | '.join(fmt(x) for x in row)+' |' for row in f.itertuples(index=False,name=None)])

assert verify_freeze()
assert not (ROOT/'ROBUSTNESS_REPORT.md').exists()
ranked=read('v1_ranked_events'); sens=read('outlier_sensitivity'); mech=read('atr_mechanism')
ext=ranked.iloc[list(range(5))+list(range(52,57))][['ticker','Date','entry_date','exit_date',STOCK,SPY,EXCESS]].copy()
ext[[STOCK,SPY,EXCESS]]*=100
ext.columns=['Ticker','Signal','Entry','Exit','Stock %','SPY %','Excess pp']
cols=['signal_count','average_excess_return_pp','sum_excess_return_pp_not_portfolio']
stocks=read('stocks'); sectors=read('sectors'); months=read('months'); execution=read('execution_summary')
summary={
    'v1_events':57,'single_peak_necessary':int(mech.fails_without_single_max.sum()),
    'raw_atr_down_20pct_from_reference_peak':int(mech.raw_atr_fell_at_least_20pct_from_peak.sum()),
    'price_rise_needed_for_20pct_ratio':int(mech.price_rise_needed_for_20pct_ratio.sum()),
    'raw_atr_not_lower_than_peak':int(mech.raw_atr_not_lower_than_peak.sum()),
    'last5_median_atr_below_first5':int((mech.last5_to_first5_median_atr_ratio<1).sum()),
    'last5_median_atr_at_least20pct_below_first5':int((mech.last5_to_first5_median_atr_ratio<=.8).sum()),
    'median_reference_peak_age_sessions':float(mech.peak_age_sessions.median()),
    'reference_peak_age_min':int(mech.peak_age_sessions.min()),'reference_peak_age_max':int(mech.peak_age_sessions.max())}
(D/'atr_mechanism_summary.json').write_text(json.dumps(summary,indent=2))
score=pd.DataFrame([
 ['Data integrity','PASS','Frozen hashes, original outputs, endpoints and signal calculations reconcile. Internal integrity only; no independent vendor confirmation.'],
 ['Outlier dependence','FAIL','Removing one winner turns the mean negative; top-three capping also turns it negative.'],
 ['Stock concentration','FAIL','QCOM alone contributes more than the net total; removing that stock makes the mean negative.'],
 ['Sector concentration','FAIL','IT and Energy each exceed the net total; removing either makes V1 negative.'],
 ['Date/regime concentration','CAUTION','Large December/August cohorts, influential sparse months and only one year.'],
 ['Observation dependence','CAUTION','56/57 events overlap another; independence is unjustified and no inference is claimed.'],
 ['Execution sensitivity','PASS','Both requested next-close diagnostics retain and increase the positive mean; fill realism remains untested.'],
 ['ATR mechanism','CAUTION','Real ATR declines are common, but price normalization and an old maximum materially affect selection.'],
],columns=['Category','Rating','Reason'])
score.to_csv(D/'scorecard.csv',index=False)
fig,ax=plt.subplots(figsize=(9,4.7),layout='constrained')
plot=sens.set_index('diagnostic').loc[['official','exclude_best_1','exclude_best_3','winsorize_best_5pct_3_events','exclude_worst_1','exclude_worst_3'],'average_excess_return_pp']
labels=['Official','Exclude best 1','Exclude best 3','Cap best 3','Exclude worst 1','Exclude worst 3']
bars=ax.barh(labels,plot,color=['#245b8a']+['#c46a28']*3+['#808080']*2)
ax.axvline(0,color='black',linewidth=.8);ax.invert_yaxis();ax.set_xlim(-1.05,1.55)
ax.bar_label(bars,fmt='%+.3f',padding=4);ax.set_xlabel('Average 10-interval excess return (percentage points)')
ax.set_title('V1: a few outcomes determine the sign of the average\nDiagnostic exclusions/capping only; official result unchanged')
fig.savefig(D/'outlier_sensitivity.png',dpi=160);plt.close(fig)
report='''# V1 adversarial robustness review

Date: 2026-09-08. **Overall classification: FRAGILE.** The official first-pass classification remains **MIXED**, and its 57-event V1 mean remains +0.355467 pp, median −0.456418 pp and hit rate 47.368421%. No parameter, universe, signal, data snapshot or official result was changed. No V2 was created.

The strongest explanation for a positive mean alongside a negative median and sub-50% hit rate is the magnitude of a few right-tail outcomes. The positive sum is a small remainder after large gains and losses offset. Stress tests are descriptive, selected after viewing first-pass results, and cannot supply independent confirmation, causal explanation or corrected significance.

## Methods and data integrity

Use exactly the 57 completed official V1 events, with V0's 332 completed events for execution comparisons. Pending signals remain excluded. Rank best/worst by excess return, with stock, SPY and excess shown separately. Individual event outcomes are equally weighted. All aggregate excess units are percentage points (pp); event CSV return fields retain fractions. Contribution means arithmetic sum of event excess returns, not a compounded or investable portfolio. Percentages of the net sum can exceed 100% because negative contributions offset winners.

The saved first-pass outputs and all frozen hashes passed before and after diagnostics. The original loader independently reconciles all official stock/SPY returns to adjusted endpoint opens. V1 indicators were recomputed over the full frozen histories, and ATR% and qualifying membership checked. All execution alternatives use matching stock/SPY dates and fields. Two new overlap boundary tests and three existing reporting tests passed. This verifies internal arithmetic and provenance, not whether Yahoo's extreme price moves are economically correct; no independent feed, exchange print or event-news audit was performed. The existing KO correction is untouched and KO has zero V1 events.

## 1. Largest winners and losers

Five best and five worst V1 excess-return observations:

'''+table(ext)+'''

Tail conventions were stated before this diagnostic calculation: ceil(5% × 57) = 3 events (5.263% of the sample). Excluding the best/worst 5% therefore equals excluding three. Winsorization caps those three at the fourth-best/fourth-worst observed excess return. Only excess is capped; synthetic capped stock/SPY metrics are intentionally blank. Also show exclusion of five events for the requested top-five contribution context. The two sides are treated symmetrically; deleting losses predictably improves the average and is not evidence of a better strategy.

'''+table(sens[['diagnostic','signal_count','average_excess_return_pp','median_excess_return_pp','hit_rate_pct']])+'''

Removing the best event changes the mean by −0.509877 pp, to −0.154410 pp. Removing the best three changes it by −1.126958 pp, to −0.771491 pp. Capping the best three, rather than deleting them, also makes the mean negative (−0.075791 pp). The downside equivalents are +0.688746 pp after removing the worst one, +1.216583 pp after the worst three, and +0.609969 pp after bottom-tail capping. Tail sensitivity is substantial in both directions.

## 2. Contribution concentration

Net summed V1 excess contribution is +20.261630 pp. Shares below use that net denominator, not gross positive returns:

'''+table(read('contribution_shares'))+'''

The best three are QCOM, AMAT and MU; two of those signals are only one session apart (April 15–16, 2026). The three best contribute +61.922124 pp while the remaining 54 contribute −41.660494 pp. One observation contributes more than the entire positive net result. This is strong descriptive evidence of dependence on a few large winners, not proof that those winners are erroneous.

## 3. Month and calendar concentration

'''+table(months[['signal_month',*cols]])+'''

December has the most signals (16/57, 28.07%); August has 13/57 (22.81%). Together they account for 50.88% of V1. September's single AMAT event contributes +17.998463 pp (88.83% of the net aggregate), December +16.867907 pp (83.25%), and July +15.706427 pp (77.52%). No single month exclusively supplies the positive result: removing any one month leaves V1 positive. However, removing September and December together leaves −0.365119 pp; V0 with those same months removed is −0.891304 pp. Thus the positive level is fragile while the relative mean advantage survives that particular attack. March and August supply substantial negative contributions.

Five-session windows are descriptive rolling windows, not optimized partitions. Their overlaps mean they must not be added together. Largest examples: December 29–January 5 has seven signals in seven stocks; August 12–18 has seven in seven stocks; August 17–21 has seven in six stocks. Same-date counts peak at three (January 5, August 17 and August 21). The full date and rolling-window files show membership.

The April 15 MU and April 16 QCOM winners hold for nine shared open-to-open intervals. RTX's April 14 loss overlaps those same dates. These are simultaneous exposures, and MU/QCOM share the frozen IT sector; a particular common news catalyst cannot be established from OHLCV and dates alone. Broad market and industry influences can affect several outcomes at once, even after subtracting SPY.

## 4. Sector concentration

'''+table(sectors[['sector',*cols]])+'''

IT supplies 27/57 events (47.37%) and +36.090096 pp, 178.12% of the net aggregate. Energy supplies six events and +32.369758 pp, 159.76% of net. All other sectors combined contribute −48.198224 pp. Removing IT leaves V1 −0.527616 pp, below V0's corresponding −0.392540 pp. Removing Energy leaves V1 −0.237414 pp, although still above corresponding V0 −0.557858 pp. There is concentration in two favorable sectors, rather than broad sector confirmation. Sector counts of 2–27 are too sparse and dependent to establish sector-specific effects.

## 5. Stock concentration

All 50 frozen stocks are retained below. Zero-event mean is unavailable; a zero sum is only an additive identity. No stock has more than four V1 signals, so every stock mean is descriptive arithmetic, not a reliable estimate of a stock-specific effect.

'''+table(stocks[['ticker',*cols]])+'''

AMD, QCOM and MU tie at four signals each. QCOM contributes +31.241333 pp (154.19% of net); AMD +19.166693 pp (94.60%); XOM +18.708027 pp (92.33%). Removing QCOM's four signals leaves the other 53 with −0.207164 pp average excess. QCOM's best event accounts for most of that stock's contribution. Repeated stock identities matter, but the count leaders alone do not establish robustness: MU contains both the worst event and two of the best four. Largest negative stock totals are RTX −15.776880 pp, NKE −10.309093 pp and META −9.151811 pp.

## 6. Dependence and overlapping outcomes

Treat each holding period as the half-open interval [entry open, exit open). Shared exit/entry timestamps alone are not overlap. Count common trading open-to-open intervals for every unordered event pair:

'''+table(read('overlap_summary'))+'''

56/57 events (98.25%) overlap at least one other stock's event. Two within-stock pairs overlap: NVDA by one interval and CAT by six. These involve four events (7.02% of 57); the 5.56% within-stock pair statistic has a different denominator, 36 possible same-stock pairs. Across stocks, 223/1,560 pairs overlap. Pair frequencies do not estimate an effective sample size.

Concurrent exposure peaks at 11 events: December 17 (11 stocks, four sectors), January 13 (11 stocks, five sectors), and August 24–26 (11 events, ten stocks, five sectors). Several nominal observations therefore reuse the same days and market shocks. A shared benchmark subtraction removes the same benchmark return, not every common exposure, beta difference or industry shock. Even non-overlapping events can share a regime. Fifty-seven outcomes cannot be treated as 57 independent experiments; no p-value, independence correction or effective sample size is manufactured.

## 7. Execution sensitivity

Same signals and completed cohort, matching SPY endpoints in every case. Official: entry O(t+1), exit O(t+11). First diagnostic changes entry only to C(t+1), preserving O(t+11) exit; this shortens exposure by the entry session. Second diagnostic uses C(t+1) to C(t+11), preserving ten close-to-close intervals. Neither changes the signal or official rule.

'''+table(execution[['version','convention','signal_count','average_excess_return_pp','median_excess_return_pp','hit_rate_pct']])+'''

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

'''+table(score)+'''

**Overall: FRAGILE.** The positive mean fails simple outlier and concentration attacks. Execution and ATR checks do not support every proposed skeptical explanation, so neither a universal failure claim nor a causal story is justified. The original MIXED result remains intact.

Remaining limits: one observed year, selected static universe/sectors, overlapping and regime-related events, revised vendor history, no independent price-event verification, idealized gross fills, and post-result diagnostic selection. These tests do not estimate future performance or establish statistical significance. The year is no longer untouched evidence.

Next lesson, without creating V2: a higher mean must be distinguished from typical-event improvement and broad independent support. Before another hypothesis is tested, specify how concentration, common exposure and numerator-versus-price effects will be judged, and preserve genuinely unobserved evidence. No new strategy or parameter is proposed here.

## Artifacts and preservation

All new diagnostic CSVs, a single outlier chart and their hashes are in output/robustness/. analysis/robustness.py performs calculations; analysis/test_robustness.py tests overlap boundaries; this report and RESEARCH_LOG.md record the complete findings. Original output/v0_v1_* files and frozen files remain hash-identical. No data download or frozen pipeline rewrite was performed.
'''
(ROOT/'ROBUSTNESS_REPORT.md').write_text(report,encoding='utf-8')
with (ROOT/'RESEARCH_LOG.md').open('a',encoding='utf-8') as f:
    f.write('\n\n---\n\n'+report)
with (ROOT/'PROMPTS.md').open('a',encoding='utf-8') as f:
    f.write('''\n\n## Prompt 008 — Human-authorized adversarial robustness review (2026-09-08)

After the official MIXED V0/V1 comparison, the human researcher asked Codex to assume V1's positive mean might mislead and challenge it without modifying the strategy. Authorized: symmetric best/worst outlier deletion and 5% tail capping/exclusion; top 1/3/5 contribution shares; month/date, sector and stock concentration; quantified within/across-stock holding overlaps; next-open versus next-close execution diagnostics; and diagnostics of an old ATR% peak, price-denominator effects and broad ATR decline. Require PASS/CAUTION/FAIL by category and an overall robustness classification; preserve all official results, update documentation, provide a one-screen video summary, and stop. Explicitly prohibited: optimization, altered SMA/ATR settings, universe changes, V2 or a search for a better strategy.

Implementation conventions stated before calculation: 5% uses ceil(0.05×57)=3 ranked excess outcomes; cap at the next retained observation and apply symmetrically to the downside. Show entry-only next-close with original exit open plus ten-interval close-to-close timing. Rolling five-session clusters and first/last-five ATR medians are descriptive post-result diagnostics, not selection rules. Complete outputs and rationale: ROBUSTNESS_REPORT.md and output/robustness/. Overall FRAGILE; official first-pass MIXED and all official output hashes preserved. No V2 created.
''')
assert verify_freeze()
original=json.loads((ROOT/'output/v0_v1_evaluation_manifest.json').read_text())
assert all(sha(ROOT/'output'/p)==h for p,h in original['reported_output_sha256'].items())
m=json.loads((D/'manifest.json').read_text())
m.update({'completed_utc':datetime.now(timezone.utc).isoformat(),'classification':'FRAGILE','report_sha256':sha(ROOT/'ROBUSTNESS_REPORT.md'),
          'report_writer_sha256':sha(ROOT/'analysis/write_robustness_report.py'),
          'outputs':{p.name:sha(p) for p in D.iterdir() if p.name!='manifest.json'}})
(D/'manifest.json').write_text(json.dumps(m,indent=2))
print('Report, log, prompt record and chart saved. Freeze and official hashes unchanged.')
