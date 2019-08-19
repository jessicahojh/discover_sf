from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Neighborhood, Restaurant_reaction, Place, Place_comment

import requests
import json
from pprint import pprint

import os 

from datetime import datetime

# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
# from flask_dropzone import Dropzone

# from flask.ext.sqlalchemy import SQLAlchemy

# from flask.ext.heroku import Heroku


app = Flask(__name__)

heroku = Heroku(app)
db = SQLAlchemy(app)

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
    return redirect(f"/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/neighborhoods")
def neighborhood_list():
    """Show list of neighborhoods."""

    neighborhood = Neighborhood.query.all()


    return render_template("neighborhoods.html", neighborhood=neighborhood)


@app.route("/neighborhoods/<int:neighborhood_id>", methods=['GET'])
def neighborhood_page(neighborhood_id):
    """Show info about a specific neighborhood."""

    neighborhood = Neighborhood.query.get(neighborhood_id)
    neighborhood_name = neighborhood.name
    description = neighborhood.description
    neighborhood_id = neighborhood.neighborhood_id

    images = neighborhood.image_url

    return render_template("specific_neighborhoods.html", neighborhood=neighborhood,
     neighborhood_name=neighborhood_name, description=description, 
     neighborhood_id=neighborhood_id, images=images)


@app.route("/neighborhoods/<int:neighborhood_id>/restaurants", methods=['GET'])
def restaurant_page(neighborhood_id):
    """Show list of the top 5 restaurants in specific neighborhood."""

    neighborhood = Neighborhood.query.get(neighborhood_id)
    neighborhood_name = neighborhood.name
    neighborhood_id = neighborhood.neighborhood_id
    

    data = yelp_api(neighborhood_name)

    comments = Restaurant_reaction.query.filter(Restaurant_reaction.neighborhood_id == neighborhood_id).all()
      

    return render_template("restaurants.html", data=data,
     neighborhood_name=neighborhood_name, neighborhood_id=neighborhood_id,
    comments=comments)


@app.route("/neighborhoods/restaurants.json", methods=['POST'])
def restaurant_page_reaction():
    """If a user is logged in, let them add a reaction/comment about restaurants.
    User only see the option to comment if they are logged in"""

    user_id = session.get("user_id")

    user = User.query.get(user_id)

    comment = request.form["comment"]
    neighborhood_id = request.form["neighborhood_id"]
    created_date = datetime.now()
    

    new_reaction = Restaurant_reaction(user_id=user_id, comment=comment,
    created_date=created_date, neighborhood_id=neighborhood_id)

    db.session.add(new_reaction)
    db.session.commit()

    # if were were to refresh and not use AJAX
    # return redirect("/neighborhoods/{}/restaurants".format(neighborhood_id))

    reaction = {
            "user_first_name": user.fname,
            "user_last_name": user.lname,
            "user_status": user.status,
            "comment": new_reaction.comment,
            "created_date": new_reaction.created_date.strftime("%B %d, %Y"),
            "neighborhood_id": new_reaction.neighborhood_id
            }  
        

    return jsonify(reaction)

    


@app.route("/neighborhoods/<int:neighborhood_id>/places", methods=['GET'])
def places_page(neighborhood_id):
    """Show list of places in specific neighborhood."""

    neighborhood = Neighborhood.query.get(neighborhood_id) #gets specific neighborhood object with the id
    neighborhood_name = neighborhood.name 
    neighborhood_id = neighborhood.neighborhood_id

    places = Place.query.filter(Place.neighborhood_id == neighborhood_id).all() #gets specific place object with the id
    # places is a list 
    place_id = Place.place_id
    image_url = Place.image_url
    p_lat = Place.p_lat
    p_long = Place.p_long

    return render_template("places.html", neighborhood_name=neighborhood_name, 
        neighborhood_id=neighborhood_id, places=places, place_id=place_id,
        image_url=image_url)

def comments_total_avg(place_id):

    comments = Place_comment.query.filter(Place_comment.place_id == place_id).order_by(Place_comment.created_date.desc()).all()


    sum_comments = sum(comment.rating for comment in comments) #list comprehension
    num_comments = len(comments)
    avg_rating = float(sum_comments)/num_comments
    avg_rating = "{0:.2f}".format(avg_rating) # 2 decimal places

    return (num_comments, avg_rating)

@app.route("/neighborhoods/<int:neighborhood_id>/places/<int:place_id>", methods=['GET'])
def specific_place_page(neighborhood_id, place_id):
    """Show specific place to visit in specific neighborhood."""

    neighborhood = Neighborhood.query.get(neighborhood_id)
    neighborhood_name = neighborhood.name 
    neighborhood_id = neighborhood.neighborhood_id

    place = Place.query.filter(Place.place_id == place_id).one()
    place_name = place.name
    description = place.description
    place_id = place.place_id
    image_url = place.image_url
    p_lat = place.p_lat
    p_long = place.p_long

    comments = Place_comment.query.filter(Place_comment.place_id == place_id).order_by(Place_comment.created_date.desc()).all()

    num_comments, avg_rating = comments_total_avg(place_id)

    # sum_comments = sum(comment.rating for comment in comments) #list comprehension
    # num_comments = len(comments)
    # avg_rating = float(sum_comments)/num_comments
    # avg_rating = "{0:.2f}".format(avg_rating) # 2 decimal places

    google_api_key = os.getenv('google_api_key')
    

    return render_template("specific_places.html", place_name=place_name, 
        description=description, neighborhood_id=neighborhood_id, place_id=place_id,
        comments=comments, avg_rating=avg_rating, num_comments=num_comments,
        google_api_key=google_api_key, image_url=image_url, neighborhood_name=neighborhood_name)


@app.route('/places-location.json')
def place_info():
    """JSON information about place location."""

    places = {
        place.place_id: {
            "place_id": place.place_id,
            "name": place.name,
            "neighborhood_id": place.neighborhood_id,
            "description": place.description,
            "p_lat": place.p_lat,
            "p_long": place.p_long,
            "image_url": place.image_url
        }
        
        for place in Place.query.all()}


    return jsonify(places)


@app.route("/neighborhoods/places.json", methods=['POST'])
def specific_place_comment():
    """If user is logged in, let them comment and rate place. User only see the 
    option to comment if they are logged in"""


    user_id = session.get("user_id")

    user = User.query.get(user_id)


    comment = request.form["comment"]
    place_id = request.form["place_id"]
    created_date = datetime.now()
    rating = request.form["rating"]


    new_comment = Place_comment(user_id=user_id, place_id=place_id, comment=comment,
    created_date=created_date, rating=rating)

    db.session.add(new_comment)
    db.session.commit()

    comments_total, avg_rating = comments_total_avg(place_id)


    reaction = {
            "user_first_name": user.fname,
            "user_last_name": user.lname,
            "user_status": user.status,
            "comment": new_comment.comment,
            "rating":new_comment.rating,
            "created_date": new_comment.created_date.strftime("%B %d, %Y"),
            "place_id": new_comment.place_id,
            "comments_total": comments_total,
            "avg_rating": avg_rating
            } 

    return jsonify(reaction)



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

    KEY = os.getenv('yelp_api_key')

    header = {"Authorization":"Bearer " + KEY}

    url_params = {
        'term': DEFAULT_TERM.replace(' ', '+'), # replace with + b/c url can't have spaces
        'location': DEFAULT_LOCATION.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'sort_by': REVIEW_COUNT
    }
    response = requests.get("https://api.yelp.com/v3/businesses/search", headers=header, params=url_params)
    data = response.json()

    return data

# @app.route("/testing_yelp_api")
# def yelp_api_page():

#     data = yelp_api("Hayes Valley")

#     return render_template("testing.html", data=data)
    
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    # app.run()
    app.run(host="0.0.0.0")


