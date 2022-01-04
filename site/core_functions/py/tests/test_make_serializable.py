"""Unittest for ``corefunctions.make_serializable``."""

import unittest
import decimal
import datetime
from core_functions import make_serializable


class TestMakeSerializable(unittest.TestCase):
    """Unittest for ``corefunctions.make_serializable``."""

    def test_decimal(self):
        """Test that ``decimal.Decimal`` formats are converted to floats."""
        testArray = [decimal.Decimal(5), decimal.Decimal(10)]
        result = make_serializable(testArray)
        expected = [5.0, 10.0]
        self.assertEqual(result, expected)

    def test_datetime(self):
        """Tests that ``datetime.datetime`` objects are converted to string."""
        testArr = [datetime.datetime(2020, 6, 10, 1, 2, 3)]
        result = make_serializable(testArr)
        expected = ["2020-06-10 01:02:03"]
        self.assertEqual(result, expected)

    def test_date(self):
        """Tests that ``datetime.date`` objects are converted to string."""
        testArr = [datetime.date(2020, 6, 10)]
        result = make_serializable(testArr)
        expected = ["2020-06-10"]
        self.assertEqual(result, expected)

    def test_ok_values_remain(self):
        """Test that values which do not need to be converted are not removed.
        """
        testArray = ['abc', None]
        result = make_serializable(testArray)
        self.assertEqual(testArray, result)
