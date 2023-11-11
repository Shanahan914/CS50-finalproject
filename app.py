import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import login_required, apology

#think about helpers - finance used apology, login-required, lookup and usd

#configure app
app = Flask(__name__)

#configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#link to sql
database = "exercise.db"
db = sqlite3.connect(database, check_same_thread=False)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



#implementing my routes

@app.route("/")
@login_required
def index():
    #sql query of log table
    historycur = db.cursor()
    action = "SELECT * FROM log WHERE userid = ?"
    temp = historycur.execute(action, [session["user_id"]])
    history = temp.fetchall()
    # will need to populate history
    if history:
        return render_template("homepage.html", history=history)
    else:
        return render_template("homepage.html")


@app.route("/login", methods=['POST', 'GET'])
def login():

    # forget user identity
    session.clear()

    if request.method == "POST":
        print("post")
        # validation - check if missing
        username = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        if not username:
            return apology("Must provide email address")
        elif not password:
            return apology("Must provide password")
    
        # check details are correct
        curchk = db.cursor()
        action = "SELECT * FROM users WHERE username = ?"
        temp = curchk.execute(action, [username])
        res = temp.fetchall()
        print(res)
        print(res[0][1])
        # Ensure username exists and password is correct
        if len(res) != 1 or not check_password_hash(
            res[0][2], request.form.get("inputPassword")
        ):
            return apology("invalid username and/or password", 403)
                
        # Remember which user has logged in
        session["user_id"] = res[0][0]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("inputEmail")
        if not username:
            return apology("Username blank", 400)
        curchk = db.cursor()
        action = "SELECT name FROM users"
        temp = curchk.execute(action)
        res = temp.fetchall()
        print (res)
        users = []
        for i in range(len(res)):
            users.append(res[i])
        if username in users:
            return apology("Email already registered, please try again", 400)
        if request.form.get("inputPassword") != request.form.get("checkPassword"):
            return apology("passwords do not match", 400)
        hashed = generate_password_hash(request.form.get("inputPassword"))
        action = "INSERT INTO users (username, password, name) VALUES (?,?,?)"
        name = "Martin"
        cur = db.cursor()
        cur.execute(action, [username, hashed, name])
        db.commit()
        
        return redirect("/")
    else:
        print("get")
        return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    # get exercise data from sql
    db.row_factory = sqlite3.Row
    curchk = db.cursor()
    action = "SELECT * FROM exercises JOIN log on log.userid = exercises.userid WHERE exercises.userid = ?"
    temp = curchk.execute(action, [session["user_id"]])
    res = temp.fetchall()
    exercises = res
    print(exercises)
    return render_template("dashboard.html", exercises=exercises)
   

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == "POST":

        #this deals with adding a new workout
        curchk = db.cursor()
        action = "SELECT date FROM log WHERE userid = ?"
        temp = curchk.execute(action, [session["user_id"]])
        res = temp.fetchall()
        today = datetime.today().strftime('%Y-%m-%d')
        dates = []
        print(res)
        for i in range(len(res)):
            dates.append(res[i][0])
        print(dates)
        if today not in dates:
            print("not in dates±")
            action = "INSERT INTO log (date, userid) VALUES (?,?)"
            logcur = db.cursor()
            logcur.execute(action,[today, session["user_id"]])
            db.commit()
        #adds the exercise
        #### need to figure out how to get latest logid. 

        action = "SELECT max(id) FROM log WHERE userid = ?"
        temp = curchk.execute(action, [session["user_id"]])
        res = temp.fetchone()
        logid = res[0]
        action = "INSERT INTO exercises (name, sets, reps, weight, userid, logid) VALUES (?,?,?,?,?,?)"
        excur = db.cursor()
        excur.execute(action, [
            request.form.get("name"),
            request.form.get("sets"),
            request.form.get("reps"),
            request.form.get("weight"),
            session["user_id"],
            logid,
        ])
        db.commit()
        return render_template("add.html")
    else:
        return render_template("add.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")