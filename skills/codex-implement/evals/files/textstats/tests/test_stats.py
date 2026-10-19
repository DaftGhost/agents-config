import unittest

from textstats.stats import mean, median


class MeanTests(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4]), 2.5)

    def test_mean_rejects_empty(self):
        with self.assertRaises(ValueError):
            mean([])


class MedianTests(unittest.TestCase):
    def test_median_odd_count(self):
        self.assertEqual(median([5, 1, 3]), 3)

    def test_median_even_count(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_median_rejects_empty(self):
        with self.assertRaises(ValueError):
            median([])
