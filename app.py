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
def userLoggedIn():
    return false

#
# App routes
#
#Home page
@app.route("/")
def home():
    #Finds the newest eight Recipes
    recipes = mongo.db.recipes.find().sort("_id", -1).limit(8)
    return render_template("home.html", recipes=recipes)


#User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #check username doesn't already exist in the db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})
        #if user exists, we need to redirect back to login to try again
        if existing_user:
            #--- Flash message ---#
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
        #---FLASH MESSAGE HERE---#
        return redirect(url_for("home"))

    return render_template("login.html")


#User login
@app.route("/login", methods=["GET", "POST"])
def login():
    #---Should check if user is logged in.---
    if request.method == "POST":
        #check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("username").lower()})

        if existing_user:
            #ensure password matches
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                # --- flash message here --- #
                return redirect(url_for("home"))
            else:
                # --- flash message here --- #
                return redirect(url_for("login"))
        else:
            # --- flash message here --- #
            return redirect(url_for("login"))

    return render_template("login.html")


#User logout
@app.route("/logout")
def logout():
    #remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=DEBUGGING)
