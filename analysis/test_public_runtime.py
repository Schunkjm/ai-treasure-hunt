import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from src.runtime_sectors import fetch_sectors
from src.run_signal_engine import scan_frames, calendar
from src import config
from src.frozen import specification_settings

class PublicRuntimeTests(unittest.TestCase):
    def test_frozen_settings(self):
        import json
        self.assertEqual(specification_settings(), json.loads(json.dumps(
            {k:v for k,v in vars(config).items() if k.isupper()})))

    def test_sector_failure_is_explicit_and_partial(self):
        def get(ticker):
            if ticker == 'AAPL': return 'Technology'
            raise RuntimeError('unavailable')
        labels, audit = fetch_sectors(['AAPL','MSFT'], getter=get)
        self.assertEqual(labels, {'AAPL':'Technology','MSFT':'UNAVAILABLE'})
        self.assertEqual(audit['MSFT']['status'], 'RuntimeError')

    def test_quarantine_without_private_file_or_price_repair(self):
        now=pd.Timestamp('2026-09-09T22:00Z');cal=calendar(now)
        target=pd.Timestamp('2026-09-09');sessions=cal.sessions_in_range(cal.first_session,target)
        close=np.full(len(sessions),100.)
        frame=pd.DataFrame({'Open':close,'High':close+1,'Low':close-1,
                            'Close':close,'Adj Close':close,'Volume':1000},index=sessions)
        original=frame.copy()
        with patch.object(Path,'read_text',side_effect=AssertionError('No reference reads')):
            scans,_,_=scan_frames({'AAPL':frame},target,cal,now,{'AAPL':'UNAVAILABLE'})
        self.assertEqual(scans[0]['data_status'],'OK')
        frame.loc[target,'Low']=102.
        scans,adjusted,audits=scan_frames({'AAPL':frame},target,cal,now,{})
        self.assertEqual(scans[0]['data_status'],'UNAVAILABLE')
        self.assertIsNone(scans[0]['V0'])
        self.assertTrue(pd.isna(adjusted['AAPL'].loc[target,'Close']))
        self.assertEqual(frame.loc[target,'Low'],102.)
        self.assertIn(str(target.date()),audits['AAPL']['invalid_dates'])
        pd.testing.assert_series_equal(frame.Close,original.Close)

if __name__=='__main__': unittest.main()
