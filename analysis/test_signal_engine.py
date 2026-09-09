import contextlib
import io
import json
import tempfile
import uuid
import shutil
import unittest
from pathlib import Path
import pandas as pd
from src.run_signal_engine import (ROOT, FEATURES, initialize, calendar, latest_closed, update_journal,
                                    load_ledger, append_event, scan_frames, main)
from src.frozen import load_sectors
from src.data import expected_sessions

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.out=ROOT/'output'/('engine_test_'+uuid.uuid4().hex);self.out.mkdir();initialize(self.out)
        self.cal=calendar(pd.Timestamp('2026-10-20T22:00Z'))
        self.date=pd.Timestamp('2026-09-09');self.now=pd.Timestamp('2026-09-09T22:00Z')
        self.row={k:1.0 for k in FEATURES}
        self.row.update(ticker='AAPL',sector='Information Technology',market_data_date='2026-09-09',
                        latest_data_date='2026-09-09',run_datetime=self.now.isoformat(),data_status='OK',V0=True,V1=True)
    def tearDown(self):
        assert self.out.resolve().parent==(ROOT/'output').resolve()
        shutil.rmtree(self.out)
    def update(self,rows=None,prices=None,now=None,replay=False):
        return update_journal(self.out,[self.row] if rows is None else rows,prices or {},self.cal,now or self.now,'fixture',replay)
    def test_duplicates_and_feature_immutability(self):
        self.update();before=(self.out/'prospective_signal_events.jsonl').read_bytes()
        self.row['SMA10']=999.;self.row['V1']=False
        added,_,records=self.update()
        self.assertEqual(added,0);self.assertEqual(len(records),2)
        self.assertEqual(before,(self.out/'prospective_signal_events.jsonl').read_bytes())
        self.assertTrue(all(r['SMA10']==1. for r in records.values()))
    def test_pending_and_completion_append_only(self):
        self.update();original=(self.out/'prospective_signal_events.jsonl').read_text()
        entry=self.cal.session_offset(self.date,1);exit_=self.cal.session_offset(self.date,11)
        prices={'AAPL':pd.DataFrame({'Open':[100.]},index=[entry]),'SPY':pd.DataFrame({'Open':[200.]},index=[entry])}
        self.update(rows=[],prices=prices,now=self.cal.session_close(entry)+pd.Timedelta(minutes=1))
        before=(self.out/'prospective_signal_events.jsonl').read_bytes()
        _,completed,records=self.update(rows=[],prices=prices,now=self.cal.session_close(entry)+pd.Timedelta(days=1))
        self.assertEqual(completed,0);self.assertEqual(before,(self.out/'prospective_signal_events.jsonl').read_bytes())
        self.assertTrue(all(r['outcome_status']=='PENDING' and 'stock_return' not in r for r in records.values()))
        # Same-source valuation handles a later uniform adjustment without rewriting original entry.
        prices={'AAPL':pd.DataFrame({'Open':[50.,55.]},index=[entry,exit_]),'SPY':pd.DataFrame({'Open':[100.,102.]},index=[entry,exit_])}
        _,completed,records=self.update(rows=[],prices=prices,now=self.cal.session_close(exit_)+pd.Timedelta(minutes=1))
        self.assertEqual(completed,2)
        for r in records.values():
            self.assertEqual(r['entry_price'],100.);self.assertEqual(r['valuation_entry_price'],50.)
            self.assertAlmostEqual(r['excess_return'],.08);self.assertEqual(r['SMA10'],1.)
        self.assertTrue((self.out/'prospective_signal_events.jsonl').read_text().startswith(original))
        before=(self.out/'prospective_signal_events.jsonl').read_bytes()
        self.update(rows=[],prices=prices,now=self.cal.session_close(exit_)+pd.Timedelta(days=1))
        self.assertEqual(before,(self.out/'prospective_signal_events.jsonl').read_bytes())
    def test_late_and_replay_are_not_prospective(self):
        _,_,records=self.update(now=self.cal.session_open(self.cal.session_offset(self.date,1)))
        self.assertTrue(all(r['record_class']=='RETROSPECTIVE' for r in records.values()))
        self.row['market_data_date']='2026-09-10'
        _,_,records=self.update(now=pd.Timestamp('2026-09-10T22:00Z'),replay=True)
        self.assertTrue(all(r['record_class']=='RETROSPECTIVE' for r in records.values()))
    def test_on_time_future_is_prospective(self):
        _,_,records=self.update()
        self.assertTrue(all(r['record_class']=='PROSPECTIVE' for r in records.values()))
    def test_future_exit_bar_is_not_used_early(self):
        self.update()
        entry=self.cal.session_offset(self.date,1);exit_=self.cal.session_offset(self.date,11)
        prices={'AAPL':pd.DataFrame({'Open':[100.,120.]},index=[entry,exit_]),'SPY':pd.DataFrame({'Open':[100.,101.]},index=[entry,exit_])}
        _,completed,records=self.update(rows=[],prices=prices,now=self.cal.session_close(entry))
        self.assertEqual(completed,0)
        self.assertTrue(all(r['outcome_status']=='PENDING' for r in records.values()))
    def test_no_missing_day_backfill(self):
        self.update()
        self.row['market_data_date']='2026-09-15'
        self.update(now=pd.Timestamp('2026-09-15T22:00Z'))
        records,_=load_ledger(self.out/'prospective_signal_events.jsonl')
        self.assertEqual({r['market_data_date'] for r in records.values()},{'2026-09-09','2026-09-15'})
    def test_reject_feature_update_and_tampering(self):
        self.update();path=self.out/'prospective_signal_events.jsonl';records,head=load_ledger(path)
        append_event(path,head,'ENTRY',next(iter(records)),{'SMA10':99})
        with self.assertRaisesRegex(ValueError,'rewrite'): load_ledger(path)
    def test_calendar_matches_frozen_and_early_close(self):
        pd.testing.assert_index_equal(self.cal.sessions_in_range('2025-03-10','2026-09-08'),expected_sessions(),check_names=False)
        self.assertEqual(str(latest_closed(self.cal,pd.Timestamp('2026-09-09T15:00Z')).date()),'2026-09-08')
        self.assertEqual(str(self.cal.session_close('2025-11-28')),'2025-11-28 18:00:00+00:00')
    @unittest.skipUnless((ROOT/'data/snapshot_2026-09-08/vendor/AAPL.csv').exists(), 'Requires unpublished vendor archive')
    def test_command_replay_and_subset(self):
        args=['--fixture-dir',str(ROOT/'data/snapshot_2026-09-08/vendor'),'--output-dir',str(self.out),'--now','2026-09-08T22:00Z']
        with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(main(args),0)
        scan=pd.read_csv(self.out/'current_signal_scan.csv');self.assertEqual(len(scan),50)
        self.assertTrue((~scan.V1|scan.V0).all());self.assertTrue(scan.data_status.eq('OK').all())
        ledger=self.out/'prospective_signal_events.jsonl'
        before=ledger.read_bytes() if ledger.exists() else b''
        with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(main(args),0)
        self.assertEqual(before,ledger.read_bytes() if ledger.exists() else b'')
        pd.testing.assert_frame_equal(scan,pd.read_csv(self.out/'current_signal_scan.csv'))
        journal=pd.read_csv(self.out/'prospective_signal_journal.csv')
        self.assertTrue(journal.record_class.eq('RETROSPECTIVE').all())
    @unittest.skipUnless((ROOT/'data/snapshot_2026-09-08/vendor/AAPL.csv').exists(), 'Requires unpublished vendor archive')
    def test_unavailable_latest_bar_not_false(self):
        raw=pd.read_csv(ROOT/'data/snapshot_2026-09-08/vendor/AAPL.csv',index_col='Date',parse_dates=True).iloc[:-1]
        scans,_,_=scan_frames({'AAPL':raw},pd.Timestamp('2026-09-08'),self.cal,self.now,load_sectors().to_dict())
        r=scans[0];self.assertEqual(r['data_status'],'UNAVAILABLE');self.assertIsNone(r['V0']);self.assertIsNone(r['V1'])

if __name__=='__main__': unittest.main()
