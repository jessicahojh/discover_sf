"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
#from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Neighborhood, Restaurant_reaction, Place, Place_comment

import requests
import json
from pprint import pprint

YELP_URL = "https://api.yelp.com/v3/businesses/search"


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]
    status = request.form["status"]

    new_user = User(fname=fname, lname=lname, email=email, password=password,
                    status=status)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added.")
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


# @app.route("/neighborhoods")
# def neighborhood_list():
#     """Show list of neighborhoods."""

#     neighborhood = Neighborhood.query.all()


#     return render_template("neighborhoods.html", neighborhood=neighborhood)


# @app.route("/neighborhoods/<int:neighborhood_id>", methods=['GET'])
# def neighborhood_page(neighborhood_id):
#     """Show info about a specific neighborhood."""

#     neighborhood = neighborhood.query.get(neighborhood_id)

#     return render_template("specific_neighborhoods.html", neighborhood=neighborhood)


@app.route("/neighborhoods/<int:neighborhood_id>/restaurants", methods=['GET'])
def restaurant_page(neighborhood_id):
    """Show list of the top 5 restaurants in specific neighborhood.

    If a user is logged in, let them add a reaction/comment."""

    neighborhood = Neighborhood.query.get(neighborhood_id)
    neighborhood_name = neighborhood.name


    data = yelp_api(neighborhood_name)

    return render_template("restaurants.html", data=data, neighborhood_name=neighborhood_name)



# @app.route("/neighborhoods/<int:neighborhood_id>/places", methods=['GET'])
# def places_page(places_id):
#     """Show list of places in specific neighborhood."""

#     neighborhood = neighborhood.query.get(neighborhood_id)
#     place = place.query.get(places_id)

#     return render_template("places.html")


# @app.route("/neighborhoods/<int:neighborhood_id>/places/<int:place_id>", methods=['GET'])
# def places_page(neighborhood_id):
#     """Show list of places in specific neighborhood.

#     if user is logged in, let them comment and rate."""

#     neighborhood = neighborhood.query.get(neighborhood_id)

#     return render_template("specific_places.html")

@app.route("/testing_yelp_api")
def yelp_api_page():

    data = yelp_api("Hayes Valley")

    return render_template("testing.html", data=data)


def yelp_api(neighborhood_name):
    """Requesting the 5 most popular restaurants in a neighborhood."""

    # API constants
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


    DEFAULT_TERM = 'restaurants'
    DEFAULT_LOCATION = neighborhood_name + ', San Francisco, CA'
    SEARCH_LIMIT = 5
    REVIEW_COUNT = 'review_count'

    header = {"Authorization":"Bearer put_key_here"}

    url_params = {
        'term': DEFAULT_TERM.replace(' ', '+'), # replace with + b/c url can't have spaces
        'location': DEFAULT_LOCATION.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'sort_by': REVIEW_COUNT
    }
    response = requests.get("https://api.yelp.com/v3/businesses/search", headers=header, params=url_params)
    data = response.json()

    return data
    
    

    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host="0.0.0.0")