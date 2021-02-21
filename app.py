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


#Calculates overall rating from rating array
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
    if recipe:
        return render_template("recipe.html", recipe=recipe)
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
@app.route("/ajax_rating", methods=['GET', 'POST'])
def ajax_rating():
    #Check whether this user has already rated this recipe
    existing_interaction = mongo.db.ratings.find_one({
        "user_id"   : session['userid'],
        "recipe_id" : request.json['recipeId']
    })
    if existing_interaction:
        print("We need to update an existing rating")
    else:
        #Get the recipe's current rating
        recipe = mongo.db.recipes.find_one({"_id" : ObjectId(request.json['recipeId'])})
        rating = recipe['rating']
        #Update with the new vote and calculate the new average
        rating[int(request.json['rating'])] += 1
        calculate_rating(rating)
        #Update the recipe document with the new rating
        result = mongo.db.recipes.update_one({"_id" : ObjectId(request.json['recipeId'])},
        {
            "$set" : {
                "rating.0" : rating[0],
                "rating.{i}".format(i=request.json['rating']) :
                    int(rating[int(request.json['rating'])])
            }
        })
        #if the update was successful log the new interation
        if result.matched_count > 0:
            interaction = {
                "user_id"   : session['userid'],
                "recipe_id" : request.json['recipeId'],
                "rating"    : int(request.json['rating'])
            }
            mongo.db.ratings.insert_one(interaction)


    return "Recieved rating of {rating}".format(rating = request.json['rating'])


#Adds a comment to a recipe document from AJAX requests
@app.route("/ajax_comment", methods=['GET','POST'])
def ajax_comment():
    if request.method == "POST":
        if len(request.json['comment']) > 0:
            mongo.db.recipes.update_one({ "_id": ObjectId(request.json['recipeId']) },
            {
                "$push": { "comments" : {
                    "author" : { "name" : session["user"], "user_id" : session["userid"] },
                    "text"   : request.json['comment'] } }
            })
    #TODO: More meaningful return response
    return "Comment Received!"
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
