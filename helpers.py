"""
Exposes some simple functions for common tasks.
"""
from secrets import token_urlsafe
from urllib.parse import urlparse
from flask import session

def user_logged_in():
    """Returns whether a user is currently logged in"""
    if session.get("user") is None:
        return False

    return True


def log_user_in(user):
    """Registers logged in user into the session"""
    session["user"] = user["name"]
    session["userid"] = str(user["_id"])
    session["userrole"] = user["role"]


def log_user_out():
    """Removes the current user from the session"""
    session.pop("user")
    session.pop("userid")
    session.pop("userrole")


def encode_time(time):
    """ Converts a time string in HH:MM format into minutes """
    time_list = time.split(":")
    if len(time_list) >= 2:
        return (int(time_list[0]) * 60) + int(time_list[1])

    return 0


def calculate_pages(total_items, current_page, items_per_page):
    """ Calculates page details for result pagination """
    pages = {
        "items_per_page" : items_per_page,
        "current_page" : current_page,
        "total_items" : total_items,
        "page_count" : 0,
        "first_item" : 0,
        "last_item" : 0
    }
    if total_items > 0:
        pages["page_count"] = int(pages["total_items"] / pages["items_per_page"])

        #calculates the first and last items shown by the current page
        pages["first_item"] = (pages["current_page"] * pages["items_per_page"]) + 1
        last_item = ( (pages["current_page"] * pages["items_per_page"]) +
            pages["items_per_page"] )

        pages["last_item"] = pages["total_items"]
        if last_item < pages["total_items"]:
            pages["last_item"] = last_item

    return pages


def calculate_rating(rating):
    """Calculates overall rating from rating array."""
    #Uses a simple averaging formula. A refinement could be to replace this with
    #a weighted formula. For instance giving greater weight for more popular options.
    cumulative = 0
    weight = 0
    for i in range(1,6):
        cumulative += rating[i] * i
        weight += rating[i]

    if weight > 0 and cumulative > 0:
        return cumulative / weight

    return 0


def compile_recipe_record(form_data, recipe = None, new_pageid = True):
    """Creates a new recipe record from formdata and any existing recipe document"""
    #carry over any existing values that shouldn't be reset
    if recipe is None:
        recipe = {}
        new_pageid = True
        rating = [0.0,0,0,0,0,0]
        comments = []
        author = session['user']
    else:
        rating = recipe['rating']
        comments = recipe['comments']
        author = recipe['author']

    #Generate pageid field
    if new_pageid:
        pageid = urlparse(
            (form_data.get('title') + "-" + token_urlsafe(8)).replace(" ", "-")
        ).path
    else:
        pageid = recipe['pageid']

    #construct new recipe record
    recipe = {
        "pageid" : pageid,
        "title" : form_data.get('title'),
        "author" : author,
        "description" : form_data.get('description'),
        "image" : form_data.get('image'),
        "cuisine" : form_data.get('cuisine'),
        "time" : encode_time(form_data.get("time")),
        "servings" : int(form_data.get('servings')),
        "rating" : rating,
        "ingredients" : form_data.getlist('ingredients'),
        "steps" : form_data.getlist('steps'),
        "comments" : comments
    }
    return recipe
