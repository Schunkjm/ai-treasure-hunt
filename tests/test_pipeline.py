"""Synthetic-only numerical tests; no historical return values are loaded."""
import unittest
import numpy as np
import pandas as pd
from src import config
from src.data import adjust_ohlc, expected_sessions, validate_frame
from src.signals import generate_signals, bullish_cross, contraction, wilder_atr
from src.outcomes import forward_outcomes


def fixture(n=120):
    index = pd.bdate_range("2025-01-02", periods=n, name="Date")
    close = 100 + np.sin(np.arange(n) / 6) * 8 + np.arange(n) / 20
    return pd.DataFrame({"Open": close + .2, "High": close + 2,
                         "Low": close - 2, "Close": close, "Volume": 1000}, index=index)


class SignalTests(unittest.TestCase):
    def test_exact_frozen_universe(self):
        self.assertEqual(len(config.UNIVERSE), 50)
        self.assertEqual(len(set(config.UNIVERSE)), 50)
        self.assertNotIn("SPY", config.UNIVERSE)

    def test_strict_cross_and_equality(self):
        fast = pd.Series([9., 11., 12., 10., 11., 9., 10., 11., 9., 11.])
        result = bullish_cross(fast, pd.Series(10., index=fast.index))
        self.assertEqual(list(np.flatnonzero(result.fillna(False))), [1, 9])

    def test_sma_windows_include_current_close(self):
        frame = fixture(40)
        frame["Close"] = np.arange(1., 41.)
        result = generate_signals(frame)
        self.assertEqual(result.sma10.iloc[19], 15.5)
        self.assertEqual(result.sma20.iloc[19], 10.5)
        self.assertTrue(pd.isna(result.v0.iloc[19]))
        self.assertFalse(pd.isna(result.v0.iloc[20]))

    def test_prefix_causality_every_prefix(self):
        frame = fixture()
        full = generate_signals(frame)
        for n in range(1, len(frame) + 1):
            pd.testing.assert_frame_equal(generate_signals(frame.iloc[:n]), full.iloc[:n])

    def test_future_mutation_cannot_change_past(self):
        frame = fixture()
        original = generate_signals(frame).iloc[:70]
        frame.iloc[70:, :4] *= 20
        pd.testing.assert_frame_equal(generate_signals(frame).iloc[:70], original)

    def test_outcome_and_open_columns_are_ignored(self):
        frame = fixture()
        original = generate_signals(frame)
        frame["Open"] = -999
        for name in ("stock_forward_return", "spy_forward_return", "forward_10d_excess_return"):
            frame[name] = np.arange(len(frame)) * 999
        frame["exit_date"] = "future"
        pd.testing.assert_frame_equal(generate_signals(frame), original)

    def test_wilder_seed_and_recurrence(self):
        index = pd.RangeIndex(17)
        close = pd.Series(100., index=index)
        high = pd.Series(101., index=index)
        low = pd.Series(99., index=index)
        high.iloc[15] = 105  # TR = 6; next ATR = (13*2 + 6)/14
        atr = wilder_atr(high, low, close)
        self.assertTrue(atr.iloc[:14].isna().all())
        self.assertEqual(atr.iloc[14], 2.)
        self.assertAlmostEqual(atr.iloc[15], 32 / 14)
        self.assertAlmostEqual(atr.iloc[16], ((32 / 14) * 13 + 2) / 14)

    def test_true_range_includes_overnight_gaps(self):
        close = pd.Series([100.] + [110.] * 14)
        high, low = close + 1, close - 1
        # First TR is 11 (gap); next thirteen are 2.
        self.assertAlmostEqual(wilder_atr(high, low, close).iloc[14], 37 / 14)

    def test_prior_max_excludes_today_and_has_20_values(self):
        values = pd.Series([1.] * 20 + [100., .8, .81])
        maximum, flag = contraction(values)
        self.assertTrue(maximum.iloc[:20].isna().all())
        self.assertEqual(maximum.iloc[20], 1.)
        self.assertEqual(maximum.iloc[21], 100.)
        self.assertFalse(flag.iloc[20])
        maximum, flag = contraction(pd.Series([1.] * 20 + [.8, .81]))
        self.assertTrue(flag.iloc[20])
        self.assertFalse(flag.iloc[21])
        values = pd.Series([100.] + [1.] * 20 + [.9])
        maximum, _ = contraction(values)
        self.assertEqual(maximum.iloc[21], 1.)  # oldest spike expires

    def test_v1_is_exact_conjunction_and_subset(self):
        result = generate_signals(fixture())
        pd.testing.assert_series_equal(result.v1, (result.v0 & result.atr_contracted).rename("v1"))
        self.assertFalse((result.v1.fillna(False) & ~result.v0.fillna(False)).any())

    def test_missing_data_resets_atr_without_backfill(self):
        frame = fixture(100)
        frame.loc[frame.index[40], ["High", "Low", "Close"]] = np.nan
        result = generate_signals(frame)
        self.assertTrue(result.atr14.iloc[40:55].isna().all())
        self.assertTrue(pd.notna(result.atr14.iloc[55]))
        self.assertTrue(result.prior20_atr_pct_max.iloc[41:75].isna().all())
        self.assertTrue(pd.notna(result.prior20_atr_pct_max.iloc[75]))

    def test_v1_has_a_positive_synthetic_example(self):
        frame = fixture(100)
        close = np.r_[np.linspace(120, 90, 50), np.linspace(91, 150, 50)]
        width = np.r_[np.full(45, 20.), np.full(55, .5)]
        frame["Close"] = close
        frame["High"] = close + width
        frame["Low"] = close - width
        result = generate_signals(frame)
        self.assertTrue(result.v0.fillna(False).any())
        self.assertTrue(result.v1.fillna(False).any())
        self.assertFalse((result.v1.fillna(False) & ~result.v0.fillna(False)).any())


class OutcomeTests(unittest.TestCase):
    def setUp(self):
        # Irregular dates deliberately include a weekend and a removed holiday.
        self.index = pd.bdate_range("2025-06-10", periods=30).difference(pd.DatetimeIndex(["2025-06-19"]))
        self.stock = pd.Series(100. + np.arange(len(self.index)), index=self.index)
        self.spy = pd.Series(200. + 3 * np.arange(len(self.index)), index=self.index)

    def test_next_open_ten_intervals_same_spy_endpoints(self):
        result = forward_outcomes(self.stock, self.spy)
        self.assertEqual(result.entry_date.iloc[0], self.index[1])
        self.assertEqual(result.exit_date.iloc[0], self.index[11])
        self.assertAlmostEqual(result.stock_forward_return.iloc[0], 111 / 101 - 1)
        self.assertAlmostEqual(result.spy_forward_return.iloc[0], 233 / 203 - 1)
        self.assertAlmostEqual(result.forward_10d_excess_return.iloc[0], 111 / 101 - 233 / 203)
        for i in range(len(result) - 11):
            self.assertEqual(self.index.get_loc(result.exit_date.iloc[i]) - self.index.get_loc(result.entry_date.iloc[i]), 10)

    def test_incomplete_horizons_are_not_zero_returns(self):
        result = forward_outcomes(self.stock, self.spy)
        self.assertTrue(result.stock_forward_return.iloc[-11:].isna().all())
        self.assertTrue((result.outcome_status.iloc[-11:] == "pending_horizon").all())

    def test_missing_endpoint_does_not_shift_trade_date(self):
        self.stock.iloc[1] = np.nan
        result = forward_outcomes(self.stock, self.spy)
        self.assertEqual(result.entry_date.iloc[0], self.index[1])
        self.assertTrue(pd.isna(result.forward_10d_excess_return.iloc[0]))
        self.assertEqual(result.outcome_status.iloc[0], "missing_endpoint_price")

    def test_spy_missing_endpoint_invalidates_excess_label(self):
        self.spy.iloc[11] = np.nan
        result = forward_outcomes(self.stock, self.spy)
        self.assertTrue(pd.isna(result.forward_10d_excess_return.iloc[0]))

    def test_misaligned_dates_rejected(self):
        with self.assertRaises(ValueError):
            forward_outcomes(self.stock, self.spy.iloc[1:])


class DataTests(unittest.TestCase):
    def test_consistent_adjustment_all_ohlc(self):
        frame = fixture(4)
        frame["Adj Close"] = frame.Close * pd.Series([.5, .5, 1., 1.], index=frame.index)
        result = adjust_ohlc(frame)
        np.testing.assert_allclose(result.loc[:, ["Open", "High", "Low", "Close"]].iloc[0], frame.loc[:, ["Open", "High", "Low", "Close"]].iloc[0] * .5)
        pd.testing.assert_series_equal(result.Volume, frame.Volume)
        np.testing.assert_allclose(result.Close, frame["Adj Close"])

    def test_quality_detects_invalid_missing_duplicate(self):
        frame = fixture(40)
        sessions = frame.index
        frame = frame.drop(sessions[4])
        frame.loc[sessions[6], "High"] = 0
        frame = pd.concat([frame, frame.iloc[:1]])
        report = validate_frame(frame, sessions)
        self.assertEqual(report["duplicate_dates"], 1)
        self.assertEqual(report["missing_dates"], [str(sessions[4].date())])
        self.assertIn(str(sessions[6].date()), report["invalid_dates"])

    def test_calendar_holidays_and_half_days(self):
        sessions = expected_sessions()
        self.assertNotIn(pd.Timestamp("2026-09-07"), sessions)
        self.assertNotIn(pd.Timestamp("2025-06-19"), sessions)
        self.assertIn(pd.Timestamp("2025-11-28"), sessions)
        self.assertEqual(sessions[-1], pd.Timestamp(config.AS_OF))


if __name__ == "__main__":
    unittest.main()
