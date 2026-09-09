"""Human-origin SMA200 environment diagnostic, not a new strategy."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import yfinance as yf
from analysis.first_comparison import ROOT, SOURCE, load_events, metrics, sha, EXCESS
from src.config import HOLIDAYS, DATA_SETTINGS
from src.data import validate_frame
from src.frozen import verify_freeze

DATA=ROOT/'data/trend_warmup'
OUT=ROOT/'output/trend_diagnostic'
EARLY_HOLIDAYS=['2024-11-28','2024-12-25','2025-01-01','2025-01-09','2025-01-20','2025-02-17']
CAL=pd.bdate_range('2024-10-01','2026-09-08').difference(pd.DatetimeIndex([*HOLIDAYS,*EARLY_HOLIDAYS]))

def features(close):
    sma=close.rolling(200,min_periods=200).mean()
    prior=sma.shift(20)
    f=pd.DataFrame({'close':close,'sma200':sma,'sma200_20_sessions_ago':prior,
                    'distance_price_units':close-sma,'distance_pct':(close/sma-1)*100,
                    'sma200_change_price_units':sma-prior,'sma200_change_pct':(sma/prior-1)*100})
    f['above']=close>sma; f['rising']=sma>prior
    f['environment']=np.select([sma.isna()|prior.isna(),close.eq(sma),f.above&f.rising,f.above&~f.rising],
                               ['Unavailable','Equality','A','B'],default='C')
    return f

def verify_original():
    verify_freeze()
    m=json.loads((ROOT/'output/v0_v1_evaluation_manifest.json').read_text())
    assert all(sha(ROOT/'output'/p)==h for p,h in m['reported_output_sha256'].items())
    r=json.loads((ROOT/'output/robustness/manifest.json').read_text())
    assert all(sha(ROOT/'output/robustness'/p)==h for p,h in r['outputs'].items())

def main():
    verify_original()
    if (OUT/'environments.csv').exists(): raise RuntimeError('Completed diagnostic exists; refusing overwrite')
    DATA.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
    yf.set_tz_cache_location(str(ROOT/'.cache/yfinance'))
    events=load_events(); v=events[events.v1].copy()
    rows=[]; audit=[]
    for ticker,group in v.groupby('ticker'):
        frozen=pd.read_csv(SOURCE/'adjusted'/f'{ticker}.csv',index_col='Date',parse_dates=True)
        first=group.Date.min(); needed=CAL[CAL.get_loc(first)-219]
        combined=frozen.Close.copy()
        check={'ticker':ticker,'first_signal':str(first.date()),'required_start':str(needed.date()),'download_needed':bool(needed<frozen.index.min())}
        if needed<frozen.index.min():
            path=DATA/f'{ticker}.csv'
            if not path.exists():
                raw=yf.Ticker(ticker).history(start=str(needed.date()),end='2025-03-15',**DATA_SETTINGS,raise_errors=True,timeout=25)
                raw.index=raw.index.tz_localize(None).normalize();raw.index.name='Date'
                raw.to_csv(path)
                (DATA/f'{ticker}.json').write_text(json.dumps({'retrieved_utc':datetime.now(timezone.utc).isoformat(),'start':str(needed.date()),'end_exclusive':'2025-03-15','settings':DATA_SETTINGS,'sha256':sha(path)},indent=2))
            raw=pd.read_csv(path,index_col='Date',parse_dates=True)
            sessions=CAL[(CAL>=needed)&(CAL<=pd.Timestamp('2025-03-14'))]
            quality=validate_frame(raw,sessions)
            check['quality']=quality
            assert not any(quality[k] for k in ['missing_dates','extra_dates','invalid_dates','duplicate_dates']), (ticker,quality)
            assert np.isfinite(raw['Adj Close']).all() and (raw['Adj Close']>0).all()
            overlap=raw.index.intersection(frozen.index)
            assert len(overlap)==5
            oldraw=pd.read_csv(ROOT/'data/snapshot_2026-09-08/vendor'/f'{ticker}.csv',index_col='Date',parse_dates=True)
            np.testing.assert_allclose(raw.loc[overlap,'Close'],oldraw.loc[overlap,'Close'],rtol=0,atol=1e-8)
            ratios=frozen.loc[overlap,'Close']/raw.loc[overlap,'Adj Close']
            scale=float(ratios.median())
            # Reject inconsistent revisions; one constant unit conversion must align all overlap closes.
            np.testing.assert_allclose(ratios,scale,rtol=1e-6,atol=0)
            check.update({'overlap_sessions':5,'scale_to_frozen_units':scale,'overlap_max_relative_residual':float(abs(ratios/scale-1).max()),'new_rows_used':int((raw.index<frozen.index.min()).sum())})
            prefix=raw.loc[raw.index<frozen.index.min(),'Adj Close']*scale
            combined=pd.concat([prefix,frozen.Close])
        combined=combined.reindex(CAL[(CAL>=combined.index.min())])
        f=features(combined)
        for _,e in group.iterrows():
            x=f.loc[e.Date]
            assert x.environment!='Unavailable'
            pos=combined.index.get_loc(e.Date)
            np.testing.assert_allclose(x.sma200,combined.iloc[pos-199:pos+1].mean(),rtol=1e-13)
            np.testing.assert_allclose(x.sma200_20_sessions_ago,combined.iloc[pos-219:pos-19].mean(),rtol=1e-13)
            # Truncation to the signal close must give identical features.
            truncated=features(combined.loc[:e.Date]).iloc[-1]
            pd.testing.assert_series_equal(x,truncated)
            rows.append({**e.to_dict(),**x.to_dict()})
        audit.append(check)
        print(f'{ticker}: historical features available; earlier data {check["download_needed"]}',flush=True)
    f=pd.DataFrame(rows).sort_values(['Date','ticker'])
    f.to_csv(OUT/'v1_trend_features.csv',index=False,float_format='%.15g')
    complete=f[f.included_in_evaluation]
    groups=pd.DataFrame([{'environment':g,**metrics(complete[complete.environment==g]),'all_signals':int(f.environment.eq(g).sum()),'pending_signals':int((f.environment.eq(g)&~f.included_in_evaluation).sum())} for g in ['A','B','C','Equality','Unavailable']])
    groups.to_csv(OUT/'environments.csv',index=False,float_format='%.15g')
    assert len(complete)==57 and len(f)==62 and groups.signal_count.sum()==57
    np.testing.assert_allclose(groups.sum_excess_return_pp_not_portfolio.sum(),complete[EXCESS].sum()*100)
    extremes=pd.concat([complete.nlargest(5,EXCESS).assign(tail='best5'),complete.nsmallest(5,EXCESS).assign(tail='worst5')])
    extremes.to_csv(OUT/'extremes.csv',index=False,float_format='%.15g')
    (OUT/'data_audit.json').write_text(json.dumps(audit,indent=2))
    verify_original()
    (OUT/'manifest.json').write_text(json.dumps({'completed_utc':datetime.now(timezone.utc).isoformat(),'origin':'Human researcher; recorded before diagnostic','official_results_unchanged':True,'script_sha256':sha(Path(__file__)),
      'earlier_holidays':EARLY_HOLIDAYS,'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in DATA.iterdir()},'outputs':{p.name:sha(p) for p in OUT.iterdir() if p.name!='manifest.json'}},indent=2))
    print(groups[['environment','signal_count','average_excess_return_pp','median_excess_return_pp','hit_rate_pct']].to_string(index=False))

if __name__=='__main__': main()
