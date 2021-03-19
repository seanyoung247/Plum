import os
import unittest

from helpers import calculate_rating, encode_time, calculate_pages
from app import app

class TestHelpers(unittest.TestCase):

    def test_calculate_rating(self):
        with self.subTest():
            # Test rating calculation with no votes
            self.assertEqual(calculate_rating([0,0,0,0,0,0]), 0.0)
        with self.subTest():
            # Test rating calculation with one vote
            self.assertEqual(calculate_rating([0,0,0,0,1,0]), 4.0)
        with self.subTest():
            # Test rating calculation with multiple votes
            self.assertEqual(calculate_rating([0,1,2,5,2,1]), 3.0)

    def test_encode_time(self):
        with self.subTest():
            #Test zero case
            self.assertEqual(encode_time("00:00"), 0)
        with self.subTest():
            #Test minutes
            self.assertEqual(encode_time("00:25"), 25)
        with self.subTest():
            #Test hours
            self.assertEqual(encode_time("04:15"), 255)

    def test_calculate_pages(self):
        with self.subTest():
            #Test zero case
            pages = {
                "items_per_page" : 10,
                "current_page" : 0,
                "total_items" : 0,
                "page_count" : 0,
                "first_item" : 0,
                "last_item" : 0
            }
            self.assertEqual(calculate_pages(0,0,10), pages)
        with self.subTest():
            #Test single page case
            pages = {
                "items_per_page" : 10,
                "current_page" : 0,
                "total_items" : 8,
                "page_count" : 0,
                "first_item" : 1,
                "last_item" : 8
            }
            self.assertEqual(calculate_pages(8,0,10), pages)
        with self.subTest():
            #Test multiple pages case
            pages = {
                "items_per_page" : 10,
                "current_page" : 0,
                "total_items" : 53,
                "page_count" : 5,
                "first_item" : 1,
                "last_item" : 10
            }
            self.assertEqual(calculate_pages(53,0,10), pages)
        with self.subTest():
            #Test offset page case
            pages = {
                "items_per_page" : 10,
                "current_page" : 3,
                "total_items" : 53,
                "page_count" : 5,
                "first_item" : 31,
                "last_item" : 40
            }
            self.assertEqual(calculate_pages(53,3,10), pages)


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    #
    # Get tests
    #
    def test_get_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_recipe(self):
        with self.subTest():
            #Test existing page
            response = self.app.get('/recipe/crispy-parmesan-crusted-chicken-mDkZitREMUU', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            #Test missing page redirects
            response = self.app.get('/recipe/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.app.get('/profile/testuser', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
