"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from sqlalchemy.sql import func


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User accounts on the website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

 
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email} password={self.password} status_code={self.status_code}>"


class Neighborhood(db.Model): # for referential integrity
    """Neighborhoods on the website."""

    __tablename__ = "neighborhoods"

    neighborhood_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Neighborhood neighborhood_id={self.neighborhood_id} name={self.name}>"



class Restaurant_reaction(db.Model):
    """Restaurant comments on the website."""

    __tablename__ = "restaurant_reactions"

    reaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))

    neighborhood = db.relationship("Neighborhood", backref="restaurant_reactions")

    # Define relationship to user
    user = db.relationship("User",
                    backref=db.backref("restaurant_reactions", order_by=reaction_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Restaurant_reaction reaction_id={self.reaction_id} user_id={self.user_id} comment={self.comment} date={self.date} neighborhood_id={self.neighborhood_id}>"

class Place(db.Model):  # for referential integrity
    """Places to visit on website."""

    __tablename__ = "places"

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))
    description = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(200), nullable=False) 

    neighborhood = db.relationship("Neighborhood", backref="places")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Place place_id={self.place_id} name={self.name}>"

class Place_comment(db.Model):
    """Places comments on the website."""

    __tablename__ = "place_comments"

    p_comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    place_id = db.Column(db.Integer, db.ForeignKey('places.place_id'))
    comment = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    rating = db.Column(db.Integer, nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref="place_comments")

    # Define relationship to place
    place = db.relationship("Place", backref="place_comments")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Place_comment p_comment_id={self.p_comment_id} user_id={self.user_id} place_id={self.place_id} comment={self.comment} date={self.date} rating={self.rating}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sanfrancisco'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")