"""Optional current Yahoo sector labels, never a signal input or fallback archive."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

def fetch_sectors(tickers, offline=False, getter=None):
    labels = {ticker: 'UNAVAILABLE' for ticker in tickers}
    audit = {}
    if offline:
        return labels, {'status': 'OFFLINE_UNAVAILABLE'}
    if getter is None:
        import yfinance as yf
        getter = lambda ticker: yf.Ticker(ticker).get_info().get('sector')
    def fetch(ticker):
        try:
            label = getter(ticker)
            if not isinstance(label, str) or not label.strip():
                raise ValueError('No sector supplied')
            return label, 'OK'
        except Exception as exc:
            return 'UNAVAILABLE', type(exc).__name__
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(fetch, ticker): ticker for ticker in tickers}
        for future in as_completed(futures):
            ticker = futures[future]
            labels[ticker], status = future.result()
            audit[ticker] = {'status': status, 'source': 'Yahoo/yfinance current sector',
                             'retrieved_utc': datetime.now(timezone.utc).isoformat()}
    return labels, audit
