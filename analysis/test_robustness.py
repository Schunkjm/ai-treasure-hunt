import unittest
from analysis.robustness import overlap

class OverlapTests(unittest.TestCase):
    def test_shared_endpoint_is_not_shared_interval(self):
        self.assertEqual(overlap(1,11,11,21),0)
    def test_partial_and_complete_overlap(self):
        self.assertEqual(overlap(1,11,6,16),5)
        self.assertEqual(overlap(1,11,1,11),10)
        self.assertEqual(overlap(1,11,12,22),0)

if __name__=='__main__':
    unittest.main()
