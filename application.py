import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin, current_user, login_user

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
def home():
    return render_template("home.html")


@app.route("/index")
def index():

    # if not session.get("logged_in")
    # return render_template(login.html)

    registration = db.execute("SELECT * FROM registration").fetchall()
    return render_template("index.html", registration=registration)


@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    db.execute("INSERT INTO registration (name, username, password) VALUES (:name, :username, :password)",
            {"name": name, "username": username, "password": password})
    # hashpassword = generate_password_hash(p)
    db.commit()
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    logname = request.form.get("username") #login.
    logpass = request.form.get("password")
    if db.execute("SELECT username,password FROM registration WHERE username = '%s' AND password = '%s'" % (logname, logpass)).rowcount==1:
        return render_template("search.html")
    else:
        return render_template("error.html")
    db.commit()
    return render_template("search.html")


@app.route("/search", methods=["POST"])
def search():
    usrinput = str(request.form.get('zipcode'))
    locations = db.execute("SELECT * FROM locations WHERE zipcode LIKE '" + usrinput.upper() + "%' OR city LIKE '" + usrinput.upper() + "%'")
    ZipAndCity=[dict(zipcode=row[1],
                    city=row[2]) for row in locations.fetchall()]
    return render_template("search.html", zipcode=ZipAndCity)


@app.route("/location", methods=["POST"])
def location():
    return render_template("location.html", locations=locations)



# @app.route("/logout")
# def logout():
#     session["logged_in"] = False
#     return home()




# @app.route('/login', methods=['POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)


# @app.route('/login', method=['POST'])
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

#     # Get all of the users in the database, send them to our registration.html template.
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

