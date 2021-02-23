import os
from flask import ( Flask, flash, render_template, redirect,
                    request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
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

#random pageid pad = token_urlsafe(8)
#01 formated number string: print(str(5).zfill(2))


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
    interaction = {"rating" : 0}
    if recipe:
        #if a user is logged in, get user/recipe interation (if any)
        if user_logged_in():
            interaction = mongo.db.ratings.find_one({
                "user_id"   : session['userid'],
                "recipe_id" : str(recipe['_id'])
            })

        return render_template("recipe.html", recipe=recipe, interaction=interaction)
    else:
        return abort(404)


#New recipe page
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    #Get the cuisines list (to populate the cuisines selector)
    cuisines = mongo.db.cuisines.find().sort("name", 1)
    return render_template("edit_recipe.html", cuisines=cuisines)


#Edit existing recipe
@app.route("/edit_recipe", methods=["GET", "POST"])
def edit_recipe():
    #Get the cuisines list (to populate the cuisines selector)
    cuisines = mongo.db.cuisines.find().sort("name", 1)
    #Get the recipe to be edited
    recipe = mongo.db.recipes.find_one({"pageid": pageid})
    return render_template("edit_recipe.html", recipe=recipe, cuisines=cuisines)


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
@app.route("/ajax_rating", methods=['GET', 'POST'])
def ajax_rating():
    #Check whether this user has already rated this recipe
    existing_interaction = mongo.db.ratings.find_one({
        "user_id"   : session['userid'],
        "recipe_id" : request.json['recipeId']
    })
    new_rating = int(request.json['rating'])
    if existing_interaction:    #User has rated this recipe before
        #What is the current rating provided by the user?
        print("updating")
        old_rating = existing_interaction['rating']
        #Get the recipe record
        recipe = mongo.db.recipes.find_one({"_id" : ObjectId(request.json['recipeId'])})
        rating = recipe['rating']
        #Remove old rating vote and add the new one
        rating[old_rating] -= 1
        rating[new_rating] += 1
        calculate_rating(rating)
        print(rating)
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
            print("Updated recipe successfully")
            existing_interaction['rating'] = new_rating
            result = mongo.db.ratings.update_one({"_id" : existing_interaction['_id']},
                {"$set" : {"rating" : new_rating}})
            if result.matched_count > 0:
                print("Updated interation successfully")

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
                "rating"    : new_rating
            }
            mongo.db.ratings.insert_one(interaction)

    return {"new_rating" : new_rating}


#Adds a comment to a recipe document from AJAX requests
@app.route("/ajax_comment", methods=['GET','POST'])
def ajax_comment():
    if request.method == "POST":
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
