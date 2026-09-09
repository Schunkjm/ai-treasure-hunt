import unittest
import numpy as np
import pandas as pd
from analysis.trend_diagnostic import features

class TrendTests(unittest.TestCase):
    def test_warmup_and_exact_windows(self):
        c=pd.Series(np.arange(1.,251.))
        f=features(c)
        self.assertEqual(f.loc[218,'environment'],'Unavailable')
        self.assertEqual(f.loc[219,'environment'],'A')
        self.assertEqual(f.loc[219,'sma200'],120.5)
        self.assertEqual(f.loc[219,'sma200_20_sessions_ago'],100.5)
    def test_equality_and_nonrising_above(self):
        f=features(pd.Series([100.]*220))
        self.assertEqual(f.iloc[-1].environment,'Equality')
        c=pd.Series([200.]*20+[100.]*199+[110.])
        self.assertEqual(features(c).iloc[-1].environment,'B')
    def test_future_price_cannot_change_past_feature(self):
        c=pd.Series(np.arange(1.,251.))
        before=features(c).iloc[219].copy()
        c.iloc[220:]=1e9
        pd.testing.assert_series_equal(before,features(c).iloc[219])

if __name__=='__main__': unittest.main()
