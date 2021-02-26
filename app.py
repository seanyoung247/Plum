import os
from flask import ( Flask, flash, render_template, redirect,
                    request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
from urllib.parse import urlparse
from datetime import date, datetime
if os.path.exists("env.py"):
    import env

DEBUGGING = True

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


#
# Helper functions
#
#Returns whether a user is currently logged in
def user_logged_in():
    if session.get("user") is None:
        return False
    else:
        return True


#Registers logged in user into the session cookie
def log_user_in(user):
    session["user"] = user["name"]
    session["userid"] = str(user["_id"])
    session["userrole"] = user["role"]


#Calculates overall rating from rating array.
#Uses a simple averaging formula. A refinement could be to replace this with
#a weighted formula. For instance giving greater weight for more popular options.
def calculate_rating(rating):
    cumulative = 0
    weight = 0
    for i in range(1,6):
        cumulative += rating[i] * i
        weight += rating[i]

    if weight > 0 and cumulative > 0:
        rating[0] = cumulative / weight
    else:
        rating[0] = 0


#Creates a recipe record object from form data
def create_recipe_record(form_data, recipe = {}, new_pageid = True):
    #carry over any existing values that shouldn't be reset
    if recipe == {}:
        new_pageid = True
        rating = [0.0,0,0,0,0,0]
        comments = []
        recipe_date = datetime.strftime(date.today(),'%d/%m/%Y')
    else:
        rating = recipe['rating']
        comments = recipe['comments']
        recipe_date = recipe['date']

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
        "author" : {"name" : session['user'], "user_id" : session['userid']},
        "date" : recipe_date,
        "description" : form_data.get('description'),
        "image" : form_data.get('image'),
        "cuisine" : form_data.get('cuisine'),
        "time" : {
            "total" : ( (int(time[0]) * 3600) + (int(time[1]) * 60) ),
            "hours" : time[0],
            "minutes" : time[1]
        },
        "servings" : form_data.get('servings'),
        "rating" : rating,
        "ingredients" : form_data.getlist('ingredients'),
        "steps" : form_data.getlist('steps'),
        "comments" : comments
    }

    return recipe


#
# App routes
#
#Home page
@app.route("/")
def home():
    #Finds the newest eight Recipes
    recipes = mongo.db.recipes.find().sort("_id", -1).limit(8)
    return render_template("home.html", recipes=recipes)


#Recipe page
@app.route("/recipe/<pageid>")
def recipe(pageid):
    recipe = mongo.db.recipes.find_one({"pageid": pageid})

    if recipe:
        #if a user is logged in, get user/recipe interation (if any)
        if user_logged_in():
            interaction = mongo.db.ratings.find_one({
                "user_id"   : session['userid'],
                "recipe_id" : str(recipe['_id'])
            })

        if not interaction:
            interaction = {"rating" : 0, "favorited" : False}

        return render_template("recipe.html", recipe=recipe, interaction=interaction)
    else:
        return abort(404)


#New recipe page
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    #Only logged in users can
    if not user_logged_in():
        flash("You need to be logged in to add recipes!", category="error")
        return redirect(url_for("home"))

    if request.method == "POST":
        #construct new recipe record
        recipe = create_recipe_record(request.form)
        mongo.db.recipes.insert_one(recipe)
        return redirect(url_for("recipe", pageid=recipe['pageid']))

    #Page specific variables
    page = {
        "name" : "Add Recipe",
        "route": url_for("add_recipe")
    }
    #Dummy recipe values
    recipe = {
        "_id" : "none",
        "title" : "",
        "description" : "",
        "image" : url_for('static', filename="images/categories/new-recipe.jpg"),
        "time"  : {"hours" : "00", "minutes" : "00"},
        "servings" : "0",
        "ingredients" : [],
        "steps" : []
    }
    #Get the cuisines list (to populate the cuisines selector)
    cuisines = mongo.db.cuisines.find().sort("name", 1)
    return render_template("edit_recipe.html", page=page, recipe=recipe, cuisines=cuisines)


#Edit existing recipe
@app.route("/edit_recipe/<pageid>", methods=["GET", "POST"])
def edit_recipe(pageid):
    #Only logged in users can edit recipes
    if not user_logged_in():
        flash("You need to be logged in to edit recipes!", category="error")
        return redirect(url_for("home"))

    #Get the recipe to be edited
    recipe = mongo.db.recipes.find_one({"pageid": pageid})
    #If the recipe can't be found, raise not found error
    if not recipe:
        return abort(404)

    #Check the currently logged in user has rights to edit this recipe
    if (session['userid'] != recipe['author']['user_id'] and session['userrole'] != "admin"):
        flash("You don't have authorisation to edit this recipe", category="error")
        return redirect(url_for("home"))

    if request.method == "POST":
        #Update the recipe record
        recipe = create_recipe_record(request.form, recipe,
            ( recipe['title'] != request.form.get('title') ))
        mongo.db.recipes.replace_one({"pageid" : pageid}, recipe)
        return redirect(url_for("recipe", pageid=recipe['pageid']))

    #Page specific variables
    page = {
        "name" : "Edit Recipe",
        "route": url_for("edit_recipe", pageid=pageid)
    }
    #Get the cuisines list (to populate the cuisines selector)
    cuisines = mongo.db.cuisines.find().sort("name", 1)
    return render_template("edit_recipe.html", page=page, recipe=recipe, cuisines=cuisines)


#User profile page
@app.route("/profile/<username>")
def profile(username):
    user = mongo.db.users.find_one({"name" : username})
    print(username)
    print(user)
    if user:
        return render_template("user_profile.html", user=user)
    else:
        return abort(404)


#User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    #Don't need to log in if user is already logged in..
    if user_logged_in():
        flash("User already logged in!", category="information")
        return redirect(url_for("home"))

    if request.method == "POST":
        #check username doesn't already exist in the db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})
        #if user exists, we need to redirect back to login to try again
        if existing_user:
            flash("That user name already exists", category="warning")
            return redirect(url_for("login"))

        register = {
            "name"     : request.form.get("username").lower(),
            "email"    : request.form.get("email").lower(),
            "password" : generate_password_hash(request.form.get("password")),
            "role"     : "user"
        }
        #register user and add them to the session cookie
        mongo.db.users.insert_one(register)
        registered_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})
        log_user_in(registered_user)
        flash("User " + session["user"] + " registered!", category="information")
        return redirect(url_for("home"))

    return render_template("login.html")


#User login
@app.route("/login", methods=["GET", "POST"])
def login():
    #Don't need to log in if user is already logged in..
    if user_logged_in():
        flash("User already logged in!", category="information")
        return redirect(url_for("home"))

    if request.method == "POST":
        #check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})

        if existing_user:
            #ensure password matches
            if check_password_hash(existing_user["password"], request.form.get("password")):
                log_user_in(existing_user)
                flash("User " + session["user"] + " Logged in!", category="information")
                return redirect(url_for("home"))
            else:
                flash("Incorrect username or password", category="warning")
                return redirect(url_for("login"))
        else:
            flash("Incorrect username or password", category="warning")
            return redirect(url_for("login"))

    return render_template("login.html")


#User logout
@app.route("/logout")
def logout():
    if user_logged_in():
        flash("User " + session["user"] + " Logged out", category="information")
        #remove user from session cookies
        session.pop("user")

    return redirect(url_for("home"))


#
# AJAX/Update routes
#
#Adds a rating to a recipe document from AJAX requests
@app.route("/ajax_rating", methods=['POST'])
def ajax_rating():
    if not user_logged_in():
        flash("You need to be logged in to rate recipes!", category="error")
        return redirect(url_for("home"))

    #Check whether this user has already rated this recipe
    existing_interaction = mongo.db.ratings.find_one({
        "user_id"   : session['userid'],
        "recipe_id" : request.json['recipeId']
    })
    new_rating = int(request.json['rating'])
    if existing_interaction:    #User has rated this recipe before
        #What is the current rating provided by the user?
        old_rating = existing_interaction['rating']
        #Get the recipe record
        recipe = mongo.db.recipes.find_one({"_id" : ObjectId(request.json['recipeId'])})
        rating = recipe['rating']
        #Remove old rating vote and add the new one
        rating[old_rating] -= 1
        rating[new_rating] += 1
        calculate_rating(rating)
        #Update the recipe document with the new rating
        result = mongo.db.recipes.update_one({"_id" : ObjectId(request.json['recipeId'])},
        {
            "$set" : {
                "rating.0" : rating[0],
                "rating.{i}".format(i=new_rating) : int(rating[new_rating]),
                "rating.{i}".format(i=old_rating) : int(rating[old_rating])
            }
        })
        #If update was successful, update interaction record
        if result.matched_count > 0:
            existing_interaction['rating'] = new_rating
            result = mongo.db.ratings.update_one({"_id" : existing_interaction['_id']},
                {"$set" : {"rating" : new_rating}})

    else:                       #User has not rated this recipe before
        #Get the recipe's current rating
        recipe = mongo.db.recipes.find_one({"_id" : ObjectId(request.json['recipeId'])})
        rating = recipe['rating']
        #Update with the new vote and calculate the new average
        rating[new_rating] += 1
        calculate_rating(rating)
        #Update the recipe document with the new rating
        result = mongo.db.recipes.update_one({"_id" : ObjectId(request.json['recipeId'])},
        {
            "$set" : {
                "rating.0" : rating[0],
                "rating.{i}".format(i=new_rating) : int(rating[new_rating])
            }
        })
        #if the update was successful log the new interation
        if result.matched_count > 0:
            interaction = {
                "user_id"   : session['userid'],
                "recipe_id" : request.json['recipeId'],
                "rating"    : new_rating,
                "favorited" : False
            }
            mongo.db.ratings.insert_one(interaction)

    return {"new_rating" : new_rating}


#Toggles user favoriting for this recipe
@app.route("/ajax_favorite", methods=['POST'])
def ajax_favorite():
    if not user_logged_in():
        flash("You need to be logged in to favorite recipes!", category="error")
        return redirect(url_for("home"))

    #Checkboxes aren't included in the form data if unchecked.
    #So if the key is in the data favorite is true, otherwise false
    favorite = ('favorite' in request.json)

    #Has the user already rated or favorited this recipe?
    existing_interaction = mongo.db.ratings.find_one({
        "user_id"   : session['userid'],
        "recipe_id" : request.json['recipeId']
    })
    #Update existing record
    if existing_interaction:
        mongo.db.ratings.update_one({"_id" : existing_interaction['_id']},
            {"$set" : {"favorited" : favorite}})
    else:
        #Create a new interaction
        interaction = {
            "user_id"   : session['userid'],
            "recipe_id" : request.json['recipeId'],
            "rating"    : 0,
            "favorited" : favorite
        }
        mongo.db.ratings.insert_one(interaction)

    return {'favorite' : favorite}


#Adds a comment to a recipe document from AJAX requests
@app.route("/ajax_comment", methods=['POST'])
def ajax_comment():
    if not user_logged_in():
        flash("You need to be logged in to comment on recipes!", category="error")
        return redirect(url_for("home"))

    if len(request.json['comment']) > 0:
        #Construct the new comment record:
        comment = {
            "author" : { "name" : session["user"], "user_id" : session["userid"] },
            "text"   : request.json['comment']
        }
        mongo.db.recipes.update_one({ "_id": ObjectId(request.json['recipeId']) },
            {"$push": { "comments" : comment }})
        return comment


#Checks if a username already exists
@app.route("/ajax_checkusername")
def ajax_checkusername():
    return "NOT YET IMPLIMENTED"


#
# Error Handling
#
#Not found. Raised by app when requested data not found in database
@app.errorhandler(404)
def not_found_error(error):
    #temporary error handling - just returns to home page with flash message
    flash("Page not found: 404", category="error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=DEBUGGING)
