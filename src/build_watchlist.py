"""Educational ordering only; never adds or changes journal signals."""
from pathlib import Path
import pandas as pd

def build(scan):
    f=scan.copy()
    f['ATR_contraction_satisfied']=f.ATR_pct.le(f.ATR_contraction_threshold)
    f['sma_gap_pct']=100*(f.SMA10/f.SMA20-1)
    valid=f.data_status.eq('OK')
    active=f.V0.eq(True);v1=f.V1.eq(True)
    a=f[valid&v1].sort_values('ticker').assign(watch_status='ACTIVE V1 (also V0)')
    b=f[valid&active&~v1].sort_values('ticker').assign(watch_status='ACTIVE V0 ONLY')
    c=f[valid&~active&f.sma_gap_pct.le(0)].sort_values(['sma_gap_pct','ticker'],ascending=[False,True]).assign(watch_status='NEAR SIGNAL — NOT ACTIVE')
    w=pd.concat([a,b,c.head(max(0,10-len(a)-len(b)))],ignore_index=True).head(10)
    w.insert(0,'watch_rank',range(1,len(w)+1))
    return w

def main():
    out=Path(__file__).resolve().parents[1]/'output'
    scan=pd.read_csv(out/'current_signal_scan.csv')
    if scan.empty: raise ValueError('Run the signal engine first; an empty template is not a scan')
    w=build(scan);w.to_csv(out/'current_watchlist_top10.csv',index=False,float_format='%.17g')
    print(f'{len(w)} educational watchlist rows saved; near signals are NOT ACTIVE. No journal changes.')

if __name__=='__main__': main()
