import unittest

from calculator import clamp


class ClampTests(unittest.TestCase):
    def test_value_inside_range(self):
        self.assertEqual(5, clamp(5, 0, 10))

    def test_value_below_range(self):
        self.assertEqual(0, clamp(-3, 0, 10))

    def test_value_above_range(self):
        self.assertEqual(10, clamp(14, 0, 10))

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            clamp(1, 4, 2)


if __name__ == "__main__":
    unittest.main()
