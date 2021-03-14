import os
from flask import ( Flask, flash, render_template, redirect,
                    request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
from urllib.parse import urlparse
from datetime import date, datetime

from helpers import *
from decorators import requires_logged_in_user, requires_user_not_logged_in
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
DEBUGGING = (os.environ.get("DEBUGGING").lower() == "true")

mongo = PyMongo(app)


#
# App routes
#
@app.route("/")
def home():
    """Shows the home page"""
    #Finds the newest eight Recipes
    recipes = mongo.db.recipes.find().sort("_id", -1).limit(8)
    return render_template("home.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Shows the search page and results."""
    items_per_page = 10
    pages = {}
    query = {}
    form_query = []
    recipes = None
    items_per_page = 10

    if request.method == "POST":
        #Construct the search query
        if "cuisine" in request.form and request.form["cuisine"]:
            query["cuisine"] = request.form["cuisine"]
            form_query.append({
                "key" : "cuisine",
                "value" : request.form["cuisine"]
            })

        if "servings" in request.form and request.form["servings"]:
            query["servings"] = int(request.form["servings"])
            form_query.append({
                "key" : "servings",
                "value" : request.form["servings"]
            })

        if "time" in request.form and request.form["time"]:
            time = request.form["time"].split(":")
            minutes = ( (int(time[0]) * 60) + int(time[1]) )
            if minutes > 0:
                query["time"] = { "$lte" : minutes }
                form_query.append({
                    "key" : "time",
                    "value" : request.form["time"]
                })

        if "rating" in request.form and int(request.form["rating"]) > 0:
            rating = int(request.form["rating"])
            query["rating"] = { "$gte" : rating }
            form_query.append({
                "key" : "rating",
                "value" : request.form["rating"]
            })

        if "search-text" in request.form and request.form["search-text"]:
            query["$text"] = {
                "$search" : request.form["search-text"],
                "$caseSensitive" : False
            }
            form_query.append({
                "key" : "search-text",
                "value" : request.form["search-text"]
            })

        #Only search if at least one field has been passed.
        if query:
            #Get page details
            pages["items_per_page"] = items_per_page
            if "page" in request.form and request.form["page"]:
                pages["current_page"] = int(request.form["page"])
                pages["page_count"] = int(request.form["page_count"])
                pages["total_items"] = int(request.form["total_items"])
            else:
                pages["total_items"] = mongo.db.recipes.count_documents(query)
                pages["current_page"] = 0
                pages["page_count"] = int(pages["total_items"] / pages["items_per_page"])

            if pages["total_items"] > 0:
                #calculates the first and last items shown by the current page
                pages["first_item"] = (pages["current_page"] * pages["items_per_page"]) + 1
                last_item = (pages["current_page"] * pages["items_per_page"]) + pages["items_per_page"]
                if last_item < pages["total_items"]:
                    pages["last_item"] = last_item
                else:
                    pages["last_item"] = pages["total_items"]
                #Get the page
                recipes = mongo.db.recipes.find(query).skip(
                    pages["current_page"] * items_per_page).limit(items_per_page)


    #Get the cuisines for the category search
    cuisines = list(mongo.db.cuisines.find().sort("name", 1))
    return render_template("search.html", cuisines=cuisines, query=form_query, pages=pages, recipes=recipes)


@app.route("/recipe/<pageid>")
def recipe(pageid):
    """Shows the recipe page for the pageid passed."""
    recipe = mongo.db.recipes.find_one({"pageid": pageid})

    if recipe: #Valid recipe found
        #if a user is logged in, get user/recipe interation (if any)
        interaction = {}
        if user_logged_in():
            interaction = mongo.db.ratings.find_one({
                "user_id"   : ObjectId(session['userid']),
                "recipe_id" : recipe['_id']
            })
        #if the user hasn't interacted with this recipe yet, provide a dummy
        #interaction to populate favorite and rating with default values
        if not interaction:
            interaction = {"rating" : 0, "favorited" : False}

        return render_template("recipe.html", recipe=recipe, interaction=interaction)
    else: #No recipe found
        return abort(404)


@app.route("/add_recipe", methods=["GET", "POST"])
@requires_logged_in_user
def add_recipe():
    """Shows the add recipe form and adds new recipe documents to the database."""

    if request.method == "POST":
        #construct new recipe record
        recipe = compile_recipe_record(request.form)
        result = mongo.db.recipes.insert_one(recipe)
        #Add new recipe to user record
        recipe_token = {
            "_id"    : str(result.inserted_id),
            "title"  : recipe['title'],
            "pageid" : recipe['pageid'],
            "image"  : recipe['image']
        }
        mongo.db.users.update_one({"_id" : ObjectId(session['userid'])},
            {"$push" : {"recipes" : recipe_token}})
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
        "time"  : 0,
        "servings" : "0",
        "ingredients" : [],
        "steps" : []
    }
    #Get the cuisines list (to populate the cuisines selector)
    cuisines = mongo.db.cuisines.find().sort("name", 1)
    return render_template("edit_recipe.html", page=page, recipe=recipe, cuisines=cuisines)


@app.route("/edit_recipe/<pageid>", methods=["GET", "POST"])
@requires_logged_in_user
def edit_recipe(pageid):
    """Shows the edit recipe form and adds changes to existing recipe document."""

    #Get the recipe to be edited
    recipe = mongo.db.recipes.find_one({"pageid": pageid})
    #If the recipe can't be found, raise not found error
    if not recipe:
        return abort(404)

    #Check the currently logged in user has rights to edit this recipe
    if (session['user'] != recipe['author'] and session['userrole'] != "admin"):
        flash("You don't have authorisation to edit this recipe", category="error")
        return redirect(url_for("home"))

    if request.method == "POST":
        #Update the recipe record
        recipe = compile_recipe_record(request.form, recipe,
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


@app.route("/profile/<username>")
def profile(username):
    """Checks if user exists and returns their profile page."""
    user = mongo.db.users.find_one({"name" : username})
    if user:
        #Get list of recipes uploaded by this user
        recipes = mongo.db.recipes.find({"author" : username})
        #Get recipes favorited by this user
        favorites = mongo.db.ratings.aggregate([
            { "$match" : {"user_id" : user['_id'], "favorited" : True} },
            {
                "$lookup" : {
                    "from" : "recipes",
                    "localField" : "recipe_id",
                    "foreignField" : "_id",
                    "as": "favorites"
                }
            },
            {"$unwind" : "$favorites"},
            {"$replaceRoot" : {"newRoot" : "$favorites"}}
        ])

        return render_template("user_profile.html", user=user, recipes=recipes, favorites=favorites)
    else:
        return abort(404)


@app.route("/register", methods=["GET", "POST"])
@requires_user_not_logged_in
def register():
    """Shows the register user page and adds a new user to the database."""
    if request.method == "POST":
        #check username doesn't already exist in the db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})
        #if user exists, we need to redirect back to login to try again
        if existing_user:
            flash("That user name already exists", category="warning")
            return redirect(url_for("login"))

        #Ensure there's no typos in the password field:
        if (request.form.get("password") != request.form.get("password-confirm")):
            flash("Passwords don't match!", category="warning")
            return redirect(url_for("login"))

        register = {
            "name"     : request.form.get("username").lower(),
            "email"    : request.form.get("email").lower(),
            "password" : generate_password_hash(request.form.get("password")),
            "role"     : "user"
        }
        #register user and add them to the session cookie
        register["_id"] = mongo.db.users.insert_one(register).inserted_id
        log_user_in(register)

        flash("User " + session["user"] + " registered!", category="information")
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
@requires_user_not_logged_in
def login():
    """Shows the user login page and logs an existing user in."""
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


@app.route("/logout")
@requires_logged_in_user
def logout():
    """Logs the current user out."""
    flash("User " + session["user"] + " Logged out", category="information")
    #remove user from session
    log_user_out()

    return redirect(url_for("home"))


#
# AJAX/Update routes
#
@app.route("/ajax_rating", methods=['POST'])
@requires_logged_in_user
def ajax_rating():
    """Accepts an AJAX request for a recipe rating and updates the recipe document."""

    if "rating" not in request.json or "recipeId" not in request.json:
        return  {"new_rating" : 0}

    #Check whether this user has already rated this recipe
    existing_interaction = mongo.db.ratings.find_one({
        "user_id"   : ObjectId(session['userid']),
        "recipe_id" : ObjectId(request.json['recipeId'])
    })
    new_rating = int(request.json['rating'])
    if existing_interaction:    #User has rated this recipe before
        #What is the current rating provided by the user?
        old_rating = existing_interaction['rating']
        #Get the recipe record
        recipe = mongo.db.recipes.find_one({"_id" : ObjectId(request.json['recipeId'])})
        rating = recipe['rating']
        #Remove old rating vote and add the new one
        if rating[old_rating] > 0:
            rating[old_rating] -= 1
        rating[new_rating] += 1
        rating[0] = calculate_rating(rating)
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
        rating[0] = calculate_rating(rating)
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
                "user_id"   : ObjectId(session['userid']),
                "recipe_id" : ObjectId(request.json['recipeId']),
                "rating"    : new_rating,
                "favorited" : False
            }
            mongo.db.ratings.insert_one(interaction)

    return {"new_rating" : new_rating}


@app.route("/ajax_favorite", methods=['POST'])
@requires_logged_in_user
def ajax_favorite():
    """Accepts AJAX requests for a favorite toggle and updates the database."""
    #Checkboxes aren't included in the form data if unchecked.
    #So if the key is in the form data favorite is true, otherwise false
    favorite = ('favorite' in request.json)

    #Has the user already rated or favorited this recipe?
    existing_interaction = mongo.db.ratings.find_one({
        "user_id"   : ObjectId(session['userid']),
        "recipe_id" : ObjectId(request.json['recipeId'])
    })
    #Update existing record
    if existing_interaction:
        mongo.db.ratings.update_one({"_id" : existing_interaction['_id']},
            {"$set" : {"favorited" : favorite}})
    else:
        #Create a new interaction
        interaction = {
            "user_id"   : ObjectId(session['userid']),
            "recipe_id" : ObjectId(request.json['recipeId']),
            "rating"    : 0,
            "favorited" : favorite
        }
        mongo.db.ratings.insert_one(interaction)

    return {'favorite' : favorite}


@app.route("/ajax_comment", methods=['POST'])
@requires_logged_in_user
def ajax_comment():
    """Adds a comment to a recipe document from AJAX requests"""
    if "comment" in request.json and len(request.json['comment']) > 0:
        #Construct the new comment record:
        comment = {
            "author" : session["user"],
            "text"   : request.json['comment']
        }
        mongo.db.recipes.update_one({ "_id": ObjectId(request.json['recipeId']) },
            {"$push": { "comments" : comment }})
        return comment


@app.route("/ajax_checkusername", methods=['POST'])
def ajax_checkusername():
    """Checks if a username already exists in the database."""
    response = { "username" : "", "exists" : True }

    if "username" in request.json:
        #Search for this username
        existing_user = mongo.db.users.find_one(
            {"name": request.json["username"].lower()})
        response['username'] = request.json["username"]
        if existing_user:
            response['exists'] = True
        else:
            response['exists'] = False

    return response


#
# Error Handling
#
@app.errorhandler(404)
def not_found_error(error):
    """Called when a page can't be found."""
    #temporary error handling - just returns to home page with flash message
    flash("Page not found: 404", category="error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=DEBUGGING)
