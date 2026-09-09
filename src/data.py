"""Data normalization and validation; no signal-performance statistics."""
import numpy as np
import pandas as pd
from .config import HISTORY_START, AS_OF, HOLIDAYS

OHLC = ["Open", "High", "Low", "Close"]


def apply_corrections(raw, ticker, corrections):
    """Apply only exact, documented source corrections; never infer prices."""
    result = raw.copy()
    for correction in corrections:
        if correction["ticker"] != ticker:
            continue
        date = pd.Timestamp(correction["date"])
        field = correction["field"]
        if date not in result.index or result.at[date, field] != correction["original_value"]:
            raise ValueError(f"Frozen correction source mismatch: {ticker} {date.date()}")
        result.at[date, field] = correction["replacement_value"]
    return result


def expected_sessions():
    return pd.bdate_range(HISTORY_START, AS_OF).difference(pd.DatetimeIndex(HOLIDAYS)).rename("Date")


def adjust_ohlc(raw):
    """Match auto_adjust=True while retaining a separate vendor snapshot.

    Explicit auto_adjust=False download includes Adj Close. Apply its ratio
    to ALL OHLC; volume/actions are retained without price-factor scaling.
    """
    factor = raw["Adj Close"] / raw["Close"]
    adjusted = raw.copy()
    adjusted[OHLC] = raw[OHLC].mul(factor, axis=0)
    adjusted["adjustment_factor"] = factor
    return adjusted


def validate_frame(frame, sessions):
    missing = sessions.difference(frame.index)
    extra = frame.index.difference(sessions)
    prices = frame[OHLC]
    finite_positive = np.isfinite(prices).all(axis=1) & (prices > 0).all(axis=1)
    ordered = (frame.High >= prices[["Open", "Close", "Low"]].max(axis=1)) & (frame.Low <= prices[["Open", "Close", "High"]].min(axis=1))
    volume_ok = np.isfinite(frame.Volume) & (frame.Volume >= 0)
    valid = finite_positive & ordered & volume_ok
    return {
        "rows": len(frame),
        "duplicate_dates": int(frame.index.duplicated().sum()),
        "missing_dates": [str(x.date()) for x in missing],
        "extra_dates": [str(x.date()) for x in extra],
        "invalid_dates": [str(x.date()) for x in frame.index[~valid]],
        "zero_volume_dates": [str(x.date()) for x in frame.index[frame.Volume == 0]],
        "first_date": str(frame.index.min().date()),
        "last_date": str(frame.index.max().date()),
    }
