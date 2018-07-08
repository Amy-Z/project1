import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    registration = db.execute("SELECT * FROM registration").fetchall()
    return render_template("index.html", registration=registration)

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    db.execute("INSERT INTO registration (name, username, password) VALUES (:name, :username, :password)",
            {"name": name, "username": username, "password": password})

    db.commit()
    return render_template("success.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Not valid. Please try again.'
#         else:
#             return redirect(url_for('index'))
#     return render_template('login.html', error=error)

# @app.route("/users")
# def registrations():
#     """Lists all users."""

#     # Get all of the users in the database, send them to our users.html template.
#     registration = db.execute("SELECT * FROM registration").fetchall()
#     return render_template("registration.html", registrations=registrations)


if __name__ == '__main__':
    index();


    # Get information from registration form
    #registration = request.form.get("registration")
    #try:
    #    registration = str(request.form.get("registration"))
    #except NameError:
    #    return render_template("error.html", message="Invalid information.")