import os
from flask import ( Flask, flash, render_template, redirect,
                    request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
@app.route


#User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    #Don't need to log in if user is already logged in..
    if user_logged_in():
        return redirect("home")

    if request.method == "POST":
        #check username doesn't already exist in the db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})
        #if user exists, we need to redirect back to login to try again
        if existing_user:
            flash("That user name already exists", category="warning")
            return redirect(url_for("login"))

        register = {
            "name": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "role": "user"
        }
        mongo.db.users.insert_one(register)
        #put the new user into the session cookie
        session["user"] = request.form.get("username").lower()
        flash("User " + session["user"] + " registered!", category="information")
        return redirect(url_for("home"))

    return render_template("login.html")


#User login
@app.route("/login", methods=["GET", "POST"])
def login():
    #Don't need to log in if user is already logged in..
    if user_logged_in():
        return redirect("home")

    if request.method == "POST":
        #check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})

        if existing_user:
            #ensure password matches
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
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
# AJAX routes
#


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=DEBUGGING)
