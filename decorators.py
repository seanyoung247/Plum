"""
Exposes custom decorators to simplify some defensive programming tasks.
"""

from functools import wraps
from flask import flash, redirect, url_for
from helpers import user_logged_in



def requires_logged_in_user(func):
    """ Disables a wrapped route if user is not logged in """
    @wraps(func)
    def route(*args, **kwargs):
        if user_logged_in():
            #If a user is logged in proceed with function
            return func(*args, **kwargs)

        #If user is not logged in, redirect to login page with error message
        flash("You need to be logged in to access that page!", category="error")
        return redirect(url_for("login"))

    return route


def requires_user_not_logged_in(func):
    """ Disables a wrapped route if a user is logged in """
    @wraps(func)
    def route(*args, **kwargs):
        if not user_logged_in():
            #If no user logged in, call the function
            return func(*args, **kwargs)

        #If user is logged in, redirect to home with error message
        flash("User logged in!", category="error")
        return redirect(url_for("home"))

    return route
