import os
import sys

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

config = {
    # Run app in debug mode for auto-updating
    "DEBUG": True
}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chessish.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show A page on which you can play standard chess"""
    # Render chessboard
    username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]
    return render_template("index.html", username=username)


@app.route("/chess960")
@login_required
def chess960():
    username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]
    print('Hello, chess960!', file=sys.stderr)
    return render_template("chess960.html", username=username)


@app.route("/simulate",  methods=["GET", "POST"])
# @login_required
def simulate():
    """Simulates a game of chess based on an inputted pgn"""
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("pgn"):
            return apology("Invalid submission")

        # the following variable, 'pgn', holds the pgn string inputted by the user. You can use this variable in your simulation
        pgn = request.form.get("pgn")

        username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]
        return render_template("simulate.html", username=username, pgn=pgn)

    else:
        username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]

        return render_template("simulate.html", username=username)


@app.route("/pgnexport", methods=["GET", "POST"])
def pgnport():
    if request.method == "POST":
        pgnexp = request.form.get("pgnexport")
        print(pgnexp)
        print('Hello, pgn!', file=sys.stderr)
        if '#' in pgnexp:
            won = 'white victory'
            ai_level = '20'

        elif '0-1'in pgnexp:
            won = 'black victory'
            ai_level = '1'
        else:
            won = 'draw'
            ai_level = '20'

        db.execute("INSERT INTO games (user_id, pgn, ai_level, won) VALUES (:user_id, :pgn, :ai_level, :won)", user_id=session["user_id"], pgn=pgnexp, ai_level=ai_level, won=won)
        return redirect("/")

    else:
        return apology("Please attempt navigation via POST method")

@app.route("/history/<queried_username>")
@login_required
def history(queried_username):
    """Display a queried user's history of personal games"""

    # Query database for user's game
    rows = (db.execute("SELECT id FROM users WHERE username = ?", queried_username))
    if not rows:
        return apology("Invalid search")
    queried_id = rows[0]['id']

    # Get all of that user's games
    games = db.execute("SELECT * FROM games WHERE user_id = :id", id=queried_id)

    # Get current username
    username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]

    # Render history of games
    return render_template("history.html", games=games, username=username, queried_username=queried_username)


@app.route("/network")
@login_required
def network():
    """Display user's list of following, does not have any forms"""

    id = session["user_id"]

    # Get the person's current network
    network_list = db.execute("SELECT id, username, bio FROM users WHERE id IN (SELECT following FROM network WHERE (follower = :id AND status = 1))", id=id)
    if not network_list:
        apology("pain in the ass")

    # Get username
    username = (db.execute("SELECT username FROM users WHERE id  = :id", id=id))[0]["username"]

    return render_template("network.html", network_list=network_list, username=username)


@app.route("/follow", methods=["GET", "POST"])
@login_required
def follow():
    """Follow someone"""
    if request.method == "POST":

        id = session["user_id"]

        # Validate form submission
        if not request.form.get("name"):
            return apology("Invalid submission")

        # Get the queried user's id
        bud = db.execute("SELECT id FROM users WHERE username = :bud_name", bud_name=request.form.get("name"))
        if len(bud) != 1:
            return apology("unregistered account name")

        # Follow this dude
        sneak = db.execute("SELECT * FROM network WHERE (follower = :id AND following = :bud_id)", id=id, bud_id=bud[0]["id"])
        if len(sneak) != 0:
            return apology("you're already following him you dumbass")

        db.execute("INSERT INTO network (id, follower, following, status) VALUES (NULL, :id, :bud_id, 1);", id=id, bud_id=bud[0]["id"])

        return redirect("/network")

    else:
        # Get username
        username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]

        return render_template("follow.html", username=username)



@app.route("/unfollow", methods=["GET", "POST"])
@login_required
def unfollow():
    """Unfollow a dude from your specific list of following"""
    if request.method == "POST":

        id = session["user_id"]

        # Validate form submission
        if not request.form.get("name"):
            return apology("Invalid Submission")

        # Get the queried user's id
        bud = db.execute("SELECT id FROM users WHERE username = :bud_name", bud_name=request.form.get("name"))
        if len(bud) != 1:
            return apology("Person does not exist")

        # Unfollow this dude
        rows = db.execute("DELETE FROM network WHERE (follower = :self_id AND following = :bud_id);", self_id=id, bud_id=bud[0]["id"])
        if rows != 1:
            return apology("You don't follow this person")
        return redirect("/network")

    else:
        # Get username
        username = (db.execute("SELECT username FROM users WHERE id  = :id", id=session["user_id"]))[0]["username"]
        return render_template("unfollow.html", username=username)

@app.route("/test")
@login_required
def test():
    return render_template("test.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif not request.form.get("bio"):
            return apology("missing bio")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        try:
            id = db.execute("INSERT INTO users (username, hash, bio) VALUES (?, ?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("bio"))
        except ValueError:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:

        return render_template("register.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = :username", username=username):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
