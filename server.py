"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Status, Neighborhood,
                    Restaurant_reaction, Place, Place_comment


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


@app.route("/neighborhoods")
def neighborhood_list():
    """Show list of neighborhoods."""

    neighborhood = Neighborhood.query.all()


    return render_template("neighborhoods.html", neighborhood=neighborhood)


@app.route("/neighborhoods/<int:neighborhood_id>", methods=['GET'])
def neighborhood_page(neighborhood_id):
    """Show info about a specific neighborhood."""

    neighborhood = neighborhood.query.get(neighborhood_id)

    return render_template("specific_neighborhoods.html", neighborhood=neighborhood)


@app.route("/neighborhoods/<int:neighborhood_id/restaurant>", methods=['GET'])
def restaurant_page(neighborhood_id):
    """Show list of the top 5 restaurants in specific neighborhood.

    If a user is logged in, let them add a reaction/comment."""

    neighborhood = neighborhood.query.get(neighborhood_id)

    return render_template("restaurants.html")


@app.route("/neighborhoods/<int:neighborhood_id/places>", methods=['GET'])
def places_page(places_id):
    """Show list of places in specific neighborhood."""

    neighborhood = neighborhood.query.get(neighborhood_id)
    place = place.query.get(places_id)

    return render_template("places.html")


@app.route("/neighborhoods/<int:neighborhood_id/places/<int:place_id>", methods=['GET'])
def places_page(neighborhood_id):
    """Show list of places in specific neighborhood.

    if user is logged in, let them comment and rate."""

    neighborhood = neighborhood.query.get(neighborhood_id)

    return render_template("specific_places.html")

    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of movie

    rating_scores = [r.score for r in movie.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    # Prediction code: only predict if the user hasn't rated it.

    if (not user_rating) and user_id:
        user = User.query.get(user_id)
        if user:
            prediction = user.predict_rating(movie)

    # Either use the prediction or their real rating

    if prediction:
        # User hasn't scored; use our prediction if we made one
        effective_rating = prediction

    elif user_rating:
        # User has already scored for real; use that
        effective_rating = user_rating.score

    else:
        # User hasn't scored, and we couldn't get a prediction
        effective_rating = None

    # Get the eye's rating, either by predicting or using real rating

    the_eye = (User.query.filter_by(email="the-eye@of-judgment.com")
                         .one())
    eye_rating = Rating.query.filter_by(
        user_id=the_eye.user_id, movie_id=movie.movie_id).first()

    if eye_rating is None:
        eye_rating = the_eye.predict_rating(movie)

    else:
        eye_rating = eye_rating.score

    if eye_rating and effective_rating:
        difference = abs(eye_rating - effective_rating)

    else:
        # We couldn't get an eye rating, so we'll skip difference
        difference = None

    # Depending on how different we are from the Eye, choose a
    # message

    BERATEMENT_MESSAGES = [
        "I suppose you don't have such bad taste after all.",
        "I regret every decision that I've ever made that has " +
            "brought me to listen to your opinion.",
        "Words fail me, as your taste in movies has clearly " +
            "failed you.",
        "That movie is great. For a clown to watch. Idiot.",
        "Words cannot express the awfulness of your taste."
    ]

    if difference:
        beratement = BERATEMENT_MESSAGES[int(difference)]

    else:
        beratement = None

    return render_template(
        "movie.html",
        movie=movie,
        user_rating=user_rating,
        average=avg_rating,
        prediction=prediction,
        eye_rating=eye_rating,
        difference=difference,
        beratement=beratement
        )


@app.route("/movies/<int:movie_id>", methods=['POST'])
def movie_detail_process(movie_id):
    """Add/edit a rating."""

    # Get form variables
    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    # Check for an existing rating
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    # Update an existing rating or if there isn't one yet, create one.
    if rating:
        rating.score = score
        flash("Rating updated.")

    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        flash("Rating added.")
        db.session.add(rating)

    db.session.commit()

    return redirect("/movies/{movie_id}")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")