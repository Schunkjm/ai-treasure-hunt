"""Record the narrow, human-origin exploratory trend diagnostic."""
import json
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from analysis.first_comparison import ROOT, EXCESS, STOCK, SPY, sha
from analysis.trend_diagnostic import OUT, verify_original

def table(f):
    def fmt(x):
        if pd.isna(x): return 'n/a'
        if isinstance(x,(float,np.floating)): return f'{x:.6f}'
        return str(x)
    return '\n'.join(['| '+' | '.join(f.columns)+' |','| '+' | '.join(['---']*len(f.columns))+' |']+['| '+' | '.join(fmt(x) for x in row)+' |' for row in f.itertuples(index=False,name=None)])

verify_original()
assert not (ROOT/'LONG_TERM_TREND_DIAGNOSTIC.md').exists()
f=pd.read_csv(OUT/'v1_trend_features.csv'); c=f[f.included_in_evaluation]
g=pd.read_csv(OUT/'environments.csv'); e=pd.read_csv(OUT/'extremes.csv')
cols=['environment','signal_count','average_excess_return_pp','median_excess_return_pp','hit_rate_pct']
ext=e[['tail','ticker','Date','entry_date','exit_date','sector','environment','distance_pct','sma200_change_pct',STOCK,SPY,EXCESS]].copy()
ext[[STOCK,SPY,EXCESS]]*=100
ext.rename(columns={STOCK:'stock_return_pct',SPY:'spy_return_pct',EXCESS:'excess_return_pp'},inplace=True)
tails=[]
for label,sample in [('all_completed',c),('best5',e[e['tail']=='best5']),('worst5',e[e['tail']=='worst5'])]:
    for field in ['environment','sector','ticker','signal_month']:
        for value,n in sample[field].value_counts().items():
            tails.append({'cohort':label,'characteristic':field,'value':value,'count':n,'cohort_size':len(sample),'share_pct':100*n/len(sample)})
pd.DataFrame(tails).to_csv(OUT/'tail_characteristics.csv',index=False,float_format='%.15g')
report='''# Learning from fragile V1: long-term trend environment

2026-09-08. **Classification: WEAK RATIONALE**, based on this diagnostic's evidence for the exact proposed next hypothesis. The general concept is economically coherent, but this observed period does not support the claim that price above a rising SMA200 would address V1's failures. This does not prove the concept false.

## Human origin and boundaries

The human researcher proposed Close > SMA200 and SMA200(t) > SMA200(t−20) before this diagnostic ran. That origin and the definitions were recorded in PROMPTS.md and RESEARCH_LOG.md before feature calculation. The proposal followed the observed V1 failures and is therefore already informed by this historical period. No V2 was created, no setting was optimized, no additional indicator family was searched, and all official V0/V1 outputs, prior robustness outputs and frozen files remain unchanged.

V1's official result is still 57 completed events, +0.355467 pp mean excess, −0.456418 pp median and 47.368421% hit rate. The frozen evaluation window remains 2025-09-08 through 2026-09-08. All 62 detected V1 signals receive trend features, including five pending outcomes. Only the original 57 complete next-open to t+11-open outcomes enter descriptive comparisons. Stock excess is measured against identical SPY endpoints with equal event weights.

## Conceptual motivation and what could be missing

ATR contraction describes declining recent price variability; it does not establish whether the stock is in a sustained advance, a rebound within a decline, or an extended advance vulnerable to reversal. A long-term trend condition could distinguish those environments. That is a coherent human hypothesis, not something the fragile mean alone demonstrates is missing.

Longer-horizon trend persistence has an established research context, but evidence on different assets and horizons does not validate this particular conjunction. For example, [Moskowitz, Ooi and Pedersen's time-series momentum research](https://www.aqr.com/insights/research/journal-article/time-series-momentum) and its [original data description](https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Original-Paper-Data) concern a 12-month momentum signal with monthly holding periods across futures asset classes. They do not establish this stock SMA200/ATR rule or its ten-session excess-return effect.

## Exact diagnostic definitions

Use the frozen adjusted Close convention. SMA200(t) = sum of Close(t−199) through Close(t), divided by 200. The earlier SMA200(t−20) averages Close(t−219) through Close(t−20). Thus the earliest feature requires 220 observed trading-session closes including the signal day, with no discretionary extra seed period for this finite-window average.

- Above: Close(t) > SMA200(t), strictly.
- Rising: SMA200(t) > SMA200(t−20), strictly. Equality means not rising.
- Distance: 100 × [Close(t)/SMA200(t) − 1], plus Close(t) − SMA200(t) in adjusted price units.
- Twenty-session change: 100 × [SMA200(t)/SMA200(t−20) − 1], plus the absolute SMA difference.
- A: above AND rising. B: above AND not rising. C: strictly below SMA200. Exact Close/SMA equality and unavailable values are retained separately, not silently classified as below. Neither occurs here.

Both indicators include only price observations dated on or before the signal close. They do not enter or modify V1. “Rising” compares two endpoints, not continuous daily increases. Because the two 200-session windows overlap by 180 sessions, the sign of their difference compares the latest 20 closes with the 20 observations displaced from the older end. It is slow-moving context, not a guarantee of a healthy trend or an attractive entry price.

## Minimal data extension and verification

Only 21 of the 33 stocks with detected V1 signals needed earlier history; the other 12 already had sufficient frozen history. Retrieved 582 additional pre-snapshot ticker-session observations in total. Start dates were individually chosen to provide exactly the missing warm-up at each stock's earliest signal. Earliest added date: 2024-10-28 for AMAT. Each request included the five existing March 10–14, 2025 sessions for continuity checks; those overlap prices never replace the frozen series. No new benchmark history was needed.

New Yahoo data are isolated in data/trend_warmup/. Settings remain yfinance auto_adjust=False, back_adjust=False, actions=True, repair=False, daily regular-session data, followed by the existing adjusted-Close convention. Every requested date is accounted for, with no duplicate or invalid OHLC/volume bars. Earlier exchange closures include Thanksgiving and Christmas 2024, New Year's Day, January 9 national mourning, MLK Day and Presidents' Day 2025; early closes remain sessions. Calendar references: [NYSE holiday announcement](https://ir.theice.com/press/news-details/2023/NYSE-Group-Announces-2024-2025-and-2026-Holiday-and-Early-Closings-Calendar/default.aspx), and [NYSE January 9 closure announcement](https://ir.theice.com/press/news-details/2024/The-New-York-Stock-Exchange-Will-Close-Markets-on-January-9-to-Honor-the-Passing-of-Former-President-Jimmy-Carter-on-National-Day-of-Mourning/default.aspx).

For every extended stock, all five overlapping unadjusted Close observations matched the saved vendor Close within 1e−8 absolute tolerance. To keep the earlier adjusted values in frozen units, multiply only the added prefix by median(frozen adjusted Close / newly retrieved Adj Close) over the overlap. A pre-calculation 1e−6 relative consistency tolerance rejects a nonconstant bridge. Observed scale factors are within approximately 1.1e−7 of one; the largest overlap relative residual is 2.11e−7. These tiny differences are compatible with adjustment rounding, not an identified substantive revision. Frozen prices are used unchanged from March 10 onward.

The new prices and adjustment factors are retrospective vendor history, not a reconstructed point-in-time corporate-action database. This inherits the frozen adjustment convention's limitation. No future price observation enters either moving-average window. Every event's features match a calculation truncated at its signal date and independently checked direct window means. All 62 events have complete features. Three synthetic tests cover exact windows/warm-up, equality/nonrising classification and immunity to future-price changes. Frozen, original result and robustness hashes pass; group totals reconcile to the 57-event official result.

## Descriptive environments

A = above a rising SMA200; B = above a nonrising SMA200; C = below SMA200. Return columns are percentage points; hit rates are percentages.

'''+table(g[cols])+'''

Detected counts including pending observations are A=36, B=4, C=22. Pending counts are respectively 3, 1 and 1. They are not assigned zero or failed outcomes.

The proposed aligned environment A contains 33/57 completed events (57.89%), with a negative mean and median and sub-50% hit rate. Its mean is lower than both the full V1 mean and the below-SMA200 group's mean. Thus the proposed explanation receives no favorable descriptive support here.

The three-event B group consists of AMAT on September 15 (+17.998463 pp), AMZN on December 10 (−0.524143 pp) and CVX on December 31 (+8.316858 pp). Its high average cannot be treated as reliable evidence or used to pivot to a different trend rule. Group C includes the single largest QCOM winner. These groups differ in stocks, sectors, months and shared exposure; their contrasts do not isolate a causal trend effect.

## Learning from the largest winners and losers

Use the same five best and five worst excess outcomes examined in the prior robustness stage; no new tail cutoff was selected. The table includes the requested distances and slope changes, all calculated at the signal close.

'''+table(ext)+'''

**Weak long-term trends are not disproportionately associated with the largest losses.** Four of the five largest losers (80%) were in A, versus three of the five largest winners (60%) and 57.89% of all completed signals. Only NKE among the five largest losers was below SMA200. The proposed conjunction would retain MU, RTX, AMAT and ETN's large losses while omitting the largest QCOM winner and second-largest AMAT winner. This comparison is environment membership, not a newly implemented strategy.

MU illustrates the missing distinction between a rising trend and a favorable short-horizon outcome. Its largest loss occurred while price was about 102.27% above SMA200 and SMA200 had risen 16.53% over 20 sessions. Its two top-five wins also occurred well above a rising SMA200. A positive long-term trend is therefore neither sufficient protection against a sharp loss nor unique to winners. This observation does not authorize an overextension threshold or another indicator search.

**Sectors:** the five largest winners comprise four IT events and one Energy event; the five largest losers comprise two IT, two Industrials and one Consumer Discretionary event. For context, IT accounts for 27/57 total V1 signals and Industrials six. Industrials represent 40% of the worst five versus 10.53% of the full sample, but only two losses underlie that contrast. Sector composition remains a plausible confounder, not evidence for a new sector rule.

**Repeated stocks:** MU supplies two of the five largest winners and the largest loss. AMAT appears in both tails on different dates. The worst five contain five distinct names, so repeated losers in one stock do not explain that tail; repeated exposure to the same names across both tails still matters. These findings are inconsistent with a simple split between permanently good and bad stock identities.

**Dates/regimes:** MU and QCOM winners on April 15–16 share nine holding intervals, while RTX's April 14 loss overlaps both. NKE's April 27 loss belongs to that same month and overlaps part of their holding periods. December has both MU's December 8 winner and ETN's December 11 loser. The most extreme outcomes can share market dates but have opposing signs. Their economic dependence and sector exposures remain relevant; dates alone cannot identify a specific causal market event. No news-driven or regime indicator was added.

Complete environment, sector, stock and month counts for both tails and the full cohort are saved in tail_characteristics.csv. Five-event tails are far too small for reliable subgroup inference.

## Interpretation and decision

**WEAK RATIONALE** is the classification of the observed evidence supporting this exact candidate. The human idea remains conceptually sensible and falsifiable; the data do not make a positive empirical case for promoting it. A negative 33-event subgroup cannot prove the hypothesis false either, particularly with overlapping outcomes and unequal sector/date composition.

What V1's failure taught us: volatility contraction and a short-term bullish crossover do not guarantee a broad improvement in typical outcomes. A favorable aggregate mean can depend on a few names and events. This diagnostic adds that a positive long-term trend alone does not explain away the large losses. Additional conditions must have a reason independent of chasing attractive subgroups.

Candidate under discussion only: **V1 + Close > SMA200 + SMA200(t) > SMA200(t−20)**. No V2 has been created or preregistered by this stage. These results do not justify treating it as the preferred improvement. If the human still wants to investigate the independent theory, preregister that exact candidate, unchanged shared infrastructure and an untouched future/out-of-sample evaluation plan before testing; keep the present period explicitly exploratory. Do not substitute B, change slope/lookbacks or optimize on the observed groups.

We have already examined this year, used its V1 failure to motivate another question, and now inspected its trend subgroups. Any candidate arising from this process is exploratory and requires genuinely unobserved future/out-of-sample validation. It is not validated, statistically proven or recommended for trading. No p-values or causal claims are made.

## Outputs

output/trend_diagnostic/v1_trend_features.csv: all 62 historical V1 features and unchanged outcomes/status. environments.csv: complete-outcome descriptive summaries. extremes.csv: original five best/five worst with trend features. tail_characteristics.csv: comparison counts. data_audit.json: per-stock retrieval/quality/adjustment bridge. manifest.json: source/code/output hashes. No chart is needed for this three-group comparison.
'''
(ROOT/'LONG_TERM_TREND_DIAGNOSTIC.md').write_text(report,encoding='utf-8')
with (ROOT/'RESEARCH_LOG.md').open('a',encoding='utf-8') as h: h.write('\n\n---\n\n'+report)
with (ROOT/'PROMPTS.md').open('a',encoding='utf-8') as h:
    h.write('\n\nPrompt 009 completion: all 62 V1 signals classified, with 57 completed outcomes unchanged. A: n=33, mean −0.462757 pp, median −0.716914 pp, hit 45.454545%; B: n=3, mean +8.597059 pp, median +8.316858 pp, hit 66.666667%; C: n=21, mean +0.463878 pp, median −0.198058 pp, hit 47.619048%. Four of five largest losses occurred in A. Evidence classification WEAK RATIONALE; concept coherent but empirical support weak in this already-observed period. No V2 created. Full record: LONG_TERM_TREND_DIAGNOSTIC.md.\n')
verify_original()
m=json.loads((OUT/'manifest.json').read_text())
m.update({'report_completed_utc':datetime.now(timezone.utc).isoformat(),'classification':'WEAK RATIONALE','report_sha256':sha(ROOT/'LONG_TERM_TREND_DIAGNOSTIC.md'),
          'report_writer_sha256':sha(ROOT/'analysis/write_trend_report.py'),'test_sha256':sha(ROOT/'analysis/test_trend_diagnostic.py'),
          'outputs':{p.name:sha(p) for p in OUT.iterdir() if p.name!='manifest.json'}})
(OUT/'manifest.json').write_text(json.dumps(m,indent=2))
print('Trend report, research log and prompt completion saved; original outputs unchanged.')
