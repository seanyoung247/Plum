import os
import unittest
import json

from flask import request

from helpers import calculate_rating, encode_time, calculate_pages
from app import app, mongo

if os.path.exists("env.py"):
    import env

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
        with self.subTest():
            #Test silent failure on bad data case
            pages = {
                "items_per_page" : 10,
                "current_page" : 6,
                "total_items" : 53,
                "page_count" : 5,
                "first_item" : 61,
                "last_item" : 53
            }
            self.assertEqual(calculate_pages(53,6,10), pages)


class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def tearDown(self):
        #delete any records created during testing
        self.logout_user()
        mongo.db.users.delete_one({"name" : self.get_test_user_data()["username"]})
        mongo.db.recipes.delete_one({
            "title": self.get_test_recipe()["title"],
            "author": self.get_test_user_data()["username"]
        })


    #
    # Helper function
    #
    def get_test_recipe(self):
        test_recipe = {
            "pageid" : "",
            "title" : "Unit Test Recipe",
            "author" : "unit_testing_user",
            "description" : "Unit test recipe record",
            "image" : "none",
            "cuisine" : "vietnamese",
            "time" : 30,
            "servings" : 4,
            "rating" : [0.0,0,0,0,0,0],
            "ingredients" : ["Test Ingredient 1", "Test Ingredient 2"],
            "steps" : ["Test Step 1", "Test Step 2"],
            "comments" : []
        }
        return test_recipe


    def create_test_recipe(self):
        response = self.app.post("/add_recipe", data=self.get_test_recipe(),
            follow_redirects=True)
        return response


    def get_test_user_data(self):
        user = {
            "username": "unit_testing_user",
            "password": "testPassword123",
            "password-confirm": "testPassword123"
        }
        return user


    def register_user(self, user):
        return self.app.post("/register", data=user, follow_redirects=True)


    def login_user(self, user):
        return self.app.post("/login", data=user, follow_redirects=True)


    def logout_user(self):
        return self.app.get("/logout", follow_redirects=True)


    #
    # GET tests
    #
    def test_mainpage(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_recipe(self):
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

    #
    # POST tests
    #
    def test_search(self):
        response = self.app.get('/search', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Create a test recipe to search for
        self.register_user(self.get_test_user_data())
        self.create_test_recipe()
        #with self.app as client:
        with self.subTest():
            #cuisine search
            data = {"cuisine" : self.get_test_recipe()["cuisine"]}
            response = self.app.post('/search', data=data)
            self.assertEqual(response.status_code, 200)
            #For some reason self.assertIn() doesn't work here...
            assert self.get_test_recipe()["title"].encode('utf-8') in response.data
        with self.subTest():
            #servings search
            data = {"servings" : self.get_test_recipe()["servings"]}
            response = self.app.post('/search', data=data)
            self.assertEqual(response.status_code, 200)
            assert self.get_test_recipe()["title"].encode('utf-8') in response.data
        with self.subTest():
            #text search
            data = {"search-text" : self.get_test_recipe()["title"]}
            response = self.app.post('/search', data=data)
            self.assertEqual(response.status_code, 200)
            assert self.get_test_recipe()["title"].encode('utf-8') in response.data
        with self.subTest():
            #compound search
            data = {
                "search-text" : self.get_test_recipe()["title"],
                "servings" : self.get_test_recipe()["servings"],
                "cuisine" : self.get_test_recipe()["cuisine"],
            }
            response = self.app.post('/search', data=data)
            self.assertEqual(response.status_code, 200)
            assert self.get_test_recipe()["title"].encode('utf-8') in response.data


    def test_registration(self):
        user = self.get_test_user_data()
        with self.subTest():
            #Test non-matching password
            response = self.register_user({
                "username": user['username'],
                "password": user['password'],
                "password-confirm": ""
            })
            assert (b"Passwords don&#39;t match!" in response.data)
        with self.subTest():
            #Test Good user account
            response = self.register_user(user)
            assert ("User {user} registered!".format(
                user=self.get_test_user_data()['username']
            ).encode('utf-8') in response.data)
        with self.subTest():
            #Test duplicate user account
            self.logout_user()
            response = self.register_user(user)
            assert (b"That user name already exists" in response.data)


    def test_login(self):
        self.register_user(self.get_test_user_data())
        self.logout_user()
        with self.subTest():
            # Test bad username and Password
            user = {"username" : " ", "password" : " "}
            response = self.login_user(user)
            assert (b"Incorrect username or password" in response.data)
        with self.subTest():
            # Test bad Password
            user = {
                "username" : self.get_test_user_data()["username"],
                "password" : " "
            }
            response = self.login_user(user)
            assert (b"Incorrect username or password" in response.data)
        with self.subTest():
            # Test valid login
            response = self.login_user(self.get_test_user_data())
            assert ("User {user} Logged in!".format(
                user=self.get_test_user_data()['username']
            ).encode('utf-8') in response.data)
        with self.subTest():
            # Test login if already logged in
            response = self.login_user(self.get_test_user_data())
            assert (b"User logged in!" in response.data)


    def test_logout(self):
        self.register_user(self.get_test_user_data())
        self.logout_user()
        with self.subTest():
            # Test logout if no logged in user
            response = self.logout_user()
            assert (b"You need to be logged in to access that page!" in response.data)
        with self.subTest():
            # Test logout if user logged in
            self.login_user(self.get_test_user_data())
            response = self.logout_user()
            assert ("User {user} Logged out".format(
                user=self.get_test_user_data()['username']
            ).encode('utf-8') in response.data)


    def test_add_recipe(self):
        with self.subTest():
            # Test adding recipe without logged in user
            response = self.create_test_recipe()
            assert (b"You need to be logged in to access that page!" in response.data)
        with self.subTest():
            # Test adding recipe with logged in user
            self.register_user(self.get_test_user_data())
            response = self.create_test_recipe()
            assert (self.get_test_recipe()["title"].encode('utf-8') in response.data)



if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2, exit=False)
