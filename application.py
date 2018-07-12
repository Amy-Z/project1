import os
import requests, json
import datetime

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin, current_user, login_user

app = Flask(__name__)


# GET https://api.darksky.net/forecast/7855d67ac23813386f3dd20216cda119/[time],[summary],[dewPoint],[humidity],[pressure]
# weather = requests.get("https://api.darksky.net/forecast/7855d67ac23813386f3dd20216cda119/[time],[summary],[dewPoint],[humidity],[temperature],[pressure]")

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


@app.route("/login_r")
def redlogin():
    return render_template("login.html")


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


# def login_required(f):
#     @wrap(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash("You need to login first")
#         return redirect(url_for('login.html'))
#     return wrap


@app.route("/login", methods=["POST"])
def login():

    logname = request.form.get("username")
    logpass = request.form.get("password")
    if db.execute("SELECT username,password FROM registration WHERE username = '%s' AND password = '%s'" % (logname, logpass)).rowcount==1:
        return render_template("search.html")
    else:
        return render_template("error.html")
    sess = session.get("user_id")
    if sess == None:
        return render_template("error.html")
    db.commit()
    return render_template("search.html")


@app.route("/search", methods=["POST"])
def search():
    usrinput = str(request.form.get("search"))
    locations = db.execute("SELECT zipcode,city FROM locations WHERE zipcode LIKE '" + usrinput.upper() + "%' OR city LIKE '" + usrinput.upper() + "%'").fetchall()
    return render_template("search.html", locations=locations)


@app.route("/search/<string:zipcode>")
def location(zipcode):
    locations = db.execute("SELECT * FROM locations WHERE zipcode = :zipcode",{"zipcode":str(zipcode)}).fetchone()
    apilatlong = db.execute("SELECT lat,long FROM locations WHERE zipcode = :zipcode",{"zipcode":str(zipcode)}).fetchone()
    weather = requests.get("https://api.darksky.net/forecast/7855d67ac23813386f3dd20216cda119/" + str(apilatlong.lat) + "," + str(apilatlong.long) + "?exclude=currently,minutely,hourly,alerts,flags")
    # if weather.requests.status_code != 200:
    #     raise Exception("Error.")
    parse = weather.json()
    summ = parse["daily"]["summary"]
    time = parse["daily"]["data"][0]["time"]
    time = datetime.datetime.fromtimestamp(time).strftime('%m-%d-%Y %H:%M:%S')
    temphigh = parse["daily"]["data"][0]["temperatureHigh"]
    templow = parse["daily"]["data"][0]["temperatureLow"]
    dew = parse["daily"]["data"][0]["dewPoint"]
    hum = parse["daily"]["data"][0]["humidity"]
    press = parse["daily"]["data"][0]["pressure"]
    cloud = parse["daily"]["data"][0]["cloudCover"]
    print(weather.text)
    return render_template("locations.html", locations=locations, summ=summ, time=time, temphigh=temphigh, templow=templow, dew=dew, hum=hum, press=press, cloud=cloud)

@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('home.html'))


@app.route("/api/locations/<int:location>")
def zip_api(zipcode):

    # Get all passengers.
    info = location.zipcode
    zips = []
    for izp in zips:
        locations.append(zipcode.city)
    return jsonify({
            "place_name": zipcode.city,
            "state": zipcode.state,
            "latitude": zipcode.latitude,
            "longitude": zipcode.longitude,
            "zip": zipcode.zipcode,
            "population": zipcode.population
        })



# @app.route("/api/<zipcode>", method=["GET"])
# def apizip():
#     GET(weather)


# @app.route("/location", methods=["POST"])
# def location():
#     usrclick = str(request.form.get('moreinfo'))
#     locations = db.execute("SELECT zipcode FROM locations WHERE zipcode = :zipcode",{"zipcode":zipcode}).fetchall()
#     # locations = db.execute("SELECT zipcode FROM locations WHERE zipcode == " + " '" + usrclick + "'")
#     # zipcode=[dict(zipcode=row[1]) for row in locations.fetchall()]
#     return render_template("locations.html", locations=locations)

# @app.route("/logout")
# def logout():
#     session["logged_in"] = False
#     return home()

if __name__ == '__main__':
    index();

