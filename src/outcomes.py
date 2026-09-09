"""Evaluation-only labels. This module is never imported by signals.py."""
import numpy as np
import pandas as pd
from .config import HORIZON


def forward_outcomes(stock_open, spy_open):
    """t signal -> t+1 entry -> t+11 exit: exactly 10 intervals.

    Align by dates before shifting, never by each ticker's available rows.
    Returns fractions (0.01 is one percent), not percentage-point display.
    """
    if not stock_open.index.equals(spy_open.index):
        raise ValueError("Stock and SPY must share the identical session index")
    index = stock_open.index
    if not index.is_unique or not index.is_monotonic_increasing:
        raise ValueError("Outcome dates must be unique and increasing")
    dates = pd.Series(index, index=index)
    entry_date = dates.shift(-1)
    exit_date = dates.shift(-(HORIZON + 1))
    stock = stock_open.where(np.isfinite(stock_open) & (stock_open > 0))
    spy = spy_open.where(np.isfinite(spy_open) & (spy_open > 0))
    entry, exit_ = stock.shift(-1), stock.shift(-(HORIZON + 1))
    spy_entry, spy_exit = spy.shift(-1), spy.shift(-(HORIZON + 1))
    available = exit_date.notna() & entry.notna() & exit_.notna() & spy_entry.notna() & spy_exit.notna()
    stock_return = (exit_ / entry - 1).where(available)
    spy_return = (spy_exit / spy_entry - 1).where(available)
    status = pd.Series("available", index=index)
    status.loc[~available] = "missing_endpoint_price"
    status.loc[exit_date.isna()] = "pending_horizon"
    return pd.DataFrame({
        "entry_date": entry_date, "exit_date": exit_date,
        "outcome_status": status,
        "stock_forward_return": stock_return,
        "spy_forward_return": spy_return,
        "forward_10d_excess_return": stock_return - spy_return,
    }, index=index)
