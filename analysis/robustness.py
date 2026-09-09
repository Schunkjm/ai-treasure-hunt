"""Authorized post-result diagnostics; never overwrites official results."""
import json
from itertools import combinations
import numpy as np
import pandas as pd
from analysis.first_comparison import ROOT, SOURCE, EXCESS, STOCK, SPY, load_events, metrics, sha
from src.config import UNIVERSE
from src.signals import generate_signals
from src.frozen import verify_freeze

OUT = ROOT / 'output/robustness'

def overlap(a, b, c, d):
    return max(0, min(b, d) - max(a, c))

def main():
    if OUT.exists():
        raise RuntimeError('Diagnostic output already exists; do not overwrite')
    original = json.loads((ROOT/'output/v0_v1_evaluation_manifest.json').read_text())
    for p, h in original['reported_output_sha256'].items():
        assert sha(ROOT/'output'/p) == h
    events = load_events()
    v0 = events[events.included_in_evaluation].copy()
    v = v0[v0.v1].copy().reset_index(drop=True)
    assert len(v) == 57
    OUT.mkdir()
    def save(f, name):
        f.to_csv(OUT/(name+'.csv'), index=False, float_format='%.15g')
    ranked = v.sort_values(EXCESS, ascending=False).reset_index(drop=True)
    save(ranked, 'v1_ranked_events')
    rows = [{'diagnostic':'official', **metrics(v)}]
    for side in ['best','worst']:
        order = v.sort_values(EXCESS, ascending=(side=='worst'))
        for k in [1,3,5]:
            rows.append({'diagnostic':f'exclude_{side}_{k}', **metrics(order.iloc[k:])})
        # ceil(5%*57)=3 observations, i.e. 5.263%; cap at the next retained value.
        capped = order.copy()
        capped.loc[capped.index[:3], EXCESS] = capped.iloc[3][EXCESS]
        # Only excess is winsorized; stock/SPY summaries would no longer reconcile.
        m = metrics(capped)
        rows.append({'diagnostic':f'winsorize_{side}_5pct_3_events', **{k:x for k,x in m.items() if 'stock' not in k and 'spy' not in k}})
    save(pd.DataFrame(rows), 'outlier_sensitivity')
    total = v[EXCESS].sum()
    save(pd.DataFrame([{'best_n':n,'sum_excess_pp':ranked.iloc[:n][EXCESS].sum()*100,
                       'percent_of_net_sum':ranked.iloc[:n][EXCESS].sum()/total*100} for n in [1,3,5]]), 'contribution_shares')
    def group(field, labels):
        return pd.DataFrame([{field:x, **metrics(v[v[field]==x])} for x in labels])
    save(group('signal_month', pd.period_range('2025-09','2026-09',freq='M').astype(str)), 'months')
    save(group('sector', sorted(events.sector.unique())), 'sectors')
    save(group('ticker', UNIVERSE), 'stocks')
    save(group('Date', sorted(v.Date.unique())), 'dates')
    prices = {t:pd.read_csv(SOURCE/'adjusted'/f'{t}.csv',index_col='Date',parse_dates=True) for t in [*UNIVERSE,'SPY']}
    calendar = prices['SPY'].index
    starts = calendar.get_indexer(v.entry_date)
    ends = calendar.get_indexer(v.exit_date)
    pairs=[]
    for i,j in combinations(range(len(v)),2):
        shared=overlap(starts[i],ends[i],starts[j],ends[j])
        pairs.append({'i':i,'j':j,'ticker_a':v.iloc[i].ticker,'ticker_b':v.iloc[j].ticker,
                      'same_stock':v.iloc[i].ticker==v.iloc[j].ticker,'shared_open_intervals':shared})
    pair=pd.DataFrame(pairs)
    save(pair,'overlap_pairs')
    exposure=[]
    for i,d in enumerate(calendar):
        active=v[(starts<=i)&(ends>i)]
        if len(active):
            exposure.append({'Date':d,'active_events':len(active),'unique_stocks':active.ticker.nunique(),
                             'sectors':active.sector.nunique(),'tickers':','.join(active.ticker)})
    save(pd.DataFrame(exposure),'daily_exposure')
    rolling=[]
    for i,d in enumerate(calendar):
        cohort=v[v.Date.between(d, calendar[min(i+4,len(calendar)-1)])]
        if len(cohort):
            rolling.append({'start':d,'end':calendar[min(i+4,len(calendar)-1)],'signals':len(cohort),
                            'stocks':cohort.ticker.nunique(),'tickers':','.join(cohort.ticker)})
    save(pd.DataFrame(rolling),'five_session_clusters')
    overlap_summary=[]
    for name,mask in [('same_stock',pair.same_stock),('different_stock',~pair.same_stock),('all',pair.index>=0)]:
        p=pair[mask]; hit=p[p.shared_open_intervals>0]
        overlap_summary.append({'category':name,'possible_pairs':len(p),'overlapping_pairs':len(hit),
                                'pair_overlap_pct':100*len(hit)/len(p) if len(p) else None,
                                'events_with_overlap':len(set(hit.i)|set(hit.j))})
    save(pd.DataFrame(overlap_summary),'overlap_summary')
    execution=[]; detail=[]
    for version, sample in [('V0',v0),('V1',v)]:
        for convention,entryfield,exitfield in [('official_open_open','Open','Open'),('next_close_original_exit_open','Close','Open'),('next_close_t11_close','Close','Close')]:
            alt=sample.copy()
            for idx,e in alt.iterrows():
                p=prices[e.ticker]; b=prices['SPY']
                r=p.loc[e.exit_date,exitfield]/p.loc[e.entry_date,entryfield]-1
                s=b.loc[e.exit_date,exitfield]/b.loc[e.entry_date,entryfield]-1
                alt.loc[idx,[STOCK,SPY,EXCESS]]=[r,s,r-s]
                detail.append({'version':version,'convention':convention,'ticker':e.ticker,'Date':e.Date,'entry_date':e.entry_date,'exit_date':e.exit_date,'stock_return':r,'spy_return':s,'excess_return':r-s})
            if convention=='official_open_open':
                np.testing.assert_allclose(alt[EXCESS],sample[EXCESS],atol=1e-12)
            execution.append({'version':version,'convention':convention,**metrics(alt)})
    save(pd.DataFrame(execution),'execution_summary'); save(pd.DataFrame(detail),'execution_events')
    mechanism=[]
    generated={}
    for _,e in v.iterrows():
        p=prices[e.ticker]
        if e.ticker not in generated:
            generated[e.ticker]=generate_signals(p)
        s=generated[e.ticker]; pos=s.index.get_loc(e.Date); prior=s.iloc[pos-20:pos]; now=s.iloc[pos]
        assert bool(now.v1)
        np.testing.assert_allclose(now.atr_pct,e.atr_pct,rtol=1e-12)
        peakdate=prior.atr_pct.idxmax(); peak=prior.loc[peakdate]
        second=prior.atr_pct.sort_values(ascending=False).iloc[1]
        atrratio=now.atr14/peak.atr14; priceratio=p.loc[e.Date,'Close']/p.loc[peakdate,'Close']
        np.testing.assert_allclose(now.atr_pct/peak.atr_pct,atrratio/priceratio)
        mechanism.append({'ticker':e.ticker,'Date':e.Date,'peak_date':peakdate,'peak_age_sessions':pos-s.index.get_loc(peakdate),
                          'atr_pct_ratio_to_peak':now.atr_pct/peak.atr_pct,'atr_ratio_to_peak':atrratio,'price_ratio_to_peak':priceratio,
                          'fails_without_single_max':bool(now.atr_pct>.8*second),
                          'raw_atr_fell_at_least_20pct_from_peak':bool(atrratio<=.8),
                          'price_rise_needed_for_20pct_ratio':bool(atrratio>.8 and priceratio>1),
                          'raw_atr_not_lower_than_peak':bool(atrratio>=1),
                          'last5_to_first5_median_atr_ratio':s.iloc[pos-4:pos+1].atr14.median()/prior.iloc[:5].atr14.median(),
                          'last5_to_first5_median_atrpct_ratio':s.iloc[pos-4:pos+1].atr_pct.median()/prior.iloc[:5].atr_pct.median()})
    save(pd.DataFrame(mechanism),'atr_mechanism')
    verify_freeze()
    for p,h in original['reported_output_sha256'].items():
        assert sha(ROOT/'output'/p)==h
    (OUT/'manifest.json').write_text(json.dumps({'official_results_unchanged':True,'frozen_files_unchanged':True,
        'script_sha256':sha(Path(__file__)),'outputs':{p.name:sha(p) for p in OUT.glob('*.csv')}},indent=2))
    print('Diagnostics completed; official outputs and frozen inputs unchanged.')

if __name__=='__main__':
    from pathlib import Path
    main()
