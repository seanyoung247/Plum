from flask import session
from secrets import token_urlsafe
from urllib.parse import urlparse
from datetime import date, datetime

def user_logged_in():
    """Returns whether a user is currently logged in"""
    if session.get("user") is None:
        return False
    else:
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
    else:
        return 0


def create_recipe_record(form_data, recipe = {}, new_pageid = True):
    """Creates a new recipe record from formdata and any existing recipe document"""
    #carry over any existing values that shouldn't be reset
    if recipe == {}:
        new_pageid = True
        rating = [0.0,0,0,0,0,0]
        comments = []
        recipe_date = datetime.strftime(date.today(),'%d/%m/%Y')
        author = session['user']
    else:
        rating = recipe['rating']
        comments = recipe['comments']
        recipe_date = recipe['date']
        author = recipe['author']

    #Generate pageid field
    if new_pageid:
        pageid = urlparse(
            (form_data.get('title') + "-" + token_urlsafe(8)).replace(" ", "-")
        ).path
    else:
        pageid = recipe['pageid']

    #construct new recipe record
    time = form_data.get("time").split(":")
    recipe = {
        "pageid" : pageid,
        "title" : form_data.get('title'),
        "author" : author,
        "date" : recipe_date,
        "description" : form_data.get('description'),
        "image" : form_data.get('image'),
        "cuisine" : form_data.get('cuisine'),
        "time" : ( (int(time[0]) * 60) + int(time[1]) ),
        "servings" : int(form_data.get('servings')),
        "rating" : rating,
        "ingredients" : form_data.getlist('ingredients'),
        "steps" : form_data.getlist('steps'),
        "comments" : comments
    }
    return recipe
