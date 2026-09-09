"""Synthetic tests of newly authorized reporting code, outside frozen source."""
import unittest
import numpy as np
import pandas as pd
from analysis.first_comparison import metrics, grouped_results, EXCESS, STOCK, SPY


class EvaluationTests(unittest.TestCase):
    def test_known_metrics_units_and_zero_hit(self):
        f = pd.DataFrame({EXCESS: [-.02, 0., .01, .03], STOCK: [-.01, .01, .02, .04], SPY: [.01]*4})
        m = metrics(f)
        self.assertEqual(m["signal_count"], 4)
        self.assertAlmostEqual(m["average_excess_return_pp"], .5)
        self.assertAlmostEqual(m["median_excess_return_pp"], .5)
        self.assertEqual(m["hit_rate_pct"], 50.)
        self.assertEqual(m["positive_stock_return_pct"], 75.)
        self.assertAlmostEqual(m["q25_excess_return_pp"], -.5)
        self.assertAlmostEqual(m["q75_excess_return_pp"], 1.5)
        self.assertAlmostEqual(m["std_excess_return_pp"], np.std([-2., 0., 1., 3.], ddof=1))

    def test_empty_means_unavailable(self):
        m = metrics(pd.DataFrame(columns=[EXCESS, STOCK, SPY], dtype=float))
        self.assertEqual(m["signal_count"], 0)
        for key in ("average_excess_return_pp", "median_excess_return_pp", "hit_rate_pct"):
            self.assertTrue(pd.isna(m[key]))

    def test_group_contribution_uses_whole_sample_denominator(self):
        f = pd.DataFrame({EXCESS: [-.02, 0., .01, .03], STOCK: [-.01, .01, .02, .04], SPY: [.01]*4, "ticker": ["A", "A", "B", "B"]})
        groups = grouped_results({"V0": f, "V1": f.iloc[2:]}, "ticker", ["A", "B", "C"])
        self.assertEqual(groups.V0_signal_count.sum(), 4)
        self.assertAlmostEqual(groups.V0_contribution_to_overall_mean_pp.sum(), .5)
        self.assertAlmostEqual(groups.V1_contribution_to_overall_mean_pp.sum(), 2.)
        self.assertTrue(pd.isna(groups.loc[2, "V1_average_excess_return_pp"]))


if __name__ == "__main__":
    unittest.main()
