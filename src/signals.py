"""Independent implementation of the preregistered equations.

Conceptual reference: kernc/backtesting.py Quick Start and crossover helper.
No upstream implementation copied. Only High, Low and Close are admitted.
"""
import numpy as np
import pandas as pd

from .config import FAST, SLOW, ATR_PERIOD, CONTRACTION_LOOKBACK, CONTRACTION_MULTIPLIER


def wilder_atr(high, low, close):
    """Seed with 14 complete TRs; reset after gaps. Never fill warm-up."""
    previous = close.shift(1)
    components = pd.concat(
        [high - low, (high - previous).abs(), (low - previous).abs()], axis=1
    )
    tr = components.max(axis=1, skipna=False)
    tr = tr.where(high.notna() & low.notna() & close.notna() & previous.notna())
    values = np.full(len(tr), np.nan)
    seed = []
    state = np.nan
    for position, value in enumerate(tr.to_numpy()):
        if not np.isfinite(value):
            seed = []
            state = np.nan
        elif np.isnan(state):
            seed.append(value)
            if len(seed) == ATR_PERIOD:
                state = float(np.mean(seed))
                values[position] = state
        else:
            state = ((ATR_PERIOD - 1) * state + value) / ATR_PERIOD
            values[position] = state
    return pd.Series(values, index=close.index, name="atr14")


def bullish_cross(fast, slow):
    eligible = fast.notna() & slow.notna() & fast.shift(1).notna() & slow.shift(1).notna()
    return ((fast.shift(1) < slow.shift(1)) & (fast > slow)).astype("boolean").where(eligible)


def contraction(atr_pct):
    prior_max = atr_pct.shift(1).rolling(CONTRACTION_LOOKBACK, min_periods=CONTRACTION_LOOKBACK).max()
    valid = atr_pct.notna() & prior_max.notna()
    flag = (atr_pct <= CONTRACTION_MULTIPLIER * prior_max).astype("boolean").where(valid)
    return prior_max, flag


def generate_signals(frame):
    """Input must already be aligned to the common session calendar.

    Outcome columns and Open are intentionally excluded at this boundary.
    Missing observations remain NA, distinguishable from an observed False.
    """
    if not frame.index.is_unique or not frame.index.is_monotonic_increasing:
        raise ValueError("Signal input dates must be unique and increasing")
    prices = frame.loc[:, ["High", "Low", "Close"]].astype(float).copy()
    prices = prices.where(np.isfinite(prices) & (prices > 0))
    close = prices["Close"]
    fast = close.rolling(FAST, min_periods=FAST).mean()
    slow = close.rolling(SLOW, min_periods=SLOW).mean()
    atr = wilder_atr(prices["High"], prices["Low"], close)
    pct = atr / close
    prior_max, contracted = contraction(pct)
    v0 = bullish_cross(fast, slow)
    v1 = v0 & contracted
    return pd.DataFrame({
        "sma10": fast, "sma20": slow, "atr14": atr, "atr_pct": pct,
        "prior20_atr_pct_max": prior_max, "atr_contracted": contracted,
        "v0": v0, "v1": v1,
    }, index=frame.index)
