"""Unittest for ``corefunctions.num_or_fallback``."""

import unittest
from core_functions import num_or_fallback


class TestNumOrFallback(unittest.TestCase):
    """Unittest for ``corefunctions.num_or_fallback``."""

    def test_converts_to_int(self):
        """Test that a string is converted to an integer correctly."""
        self.assertEqual(num_or_fallback('1', None, 'I'), 1)

    def test_converts_to_float(self):
        """Test that a string is converted to an float correctly."""
        self.assertEqual(num_or_fallback('1', None), 1.0)

    def test_returns_fallback_for_string(self):
        """Test that the fallback value is returned when using an invalid
        value.
        """
        self.assertEqual(num_or_fallback('abc', 1), 1)

    def test_returns_fallback_for_none(self):
        """Test that the fallback value is returned when using an invalid
        value.
        """
        self.assertEqual(num_or_fallback(None, 1), 1)
