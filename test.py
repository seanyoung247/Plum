import unittest
from helpers import calculate_rating


class TestHelpers(unittest.TestCase):

    def test_calculate_rating(self):
        # Test rating calculation with no votes
        with self.subTest():
            self.assertEqual(calculate_rating([0,0,0,0,0,0]), 0.0)
        # Test rating calculation with one vote
        with self.subTest():
            self.assertEqual(calculate_rating([0,0,0,0,1,0]), 4.0)
        # Test rating calculation with multiple votes
        with self.subTest():
            self.assertEqual(calculate_rating([0,1,0,0,0,1]), 3.0)


if __name__ == '__main__':
    unittest.main()
