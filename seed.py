import datetime
from sqlalchemy import func

from model import User, connect_to_db, db, Status, Neighborhood,
                    Restaurant_reaction, Place, Place_comment

from server import app


def load_users():
    """Load sample users into database."""

    liz = User(fname="Liz", lname="Law", email="liz@gmail.com", password="123", status_code="1")
    ash = User(fname="Ash", lname="Ma", email="ash@gmail.com", password="abc", status_code="1")
    tk = User(fname="Tk", lname="Kombarov", email="tk@gmail.com", password="aaa", status_code="1")
    jess = User(fname="Jess", lname="Ho", email="jess@gmail.com", password="bbb", status_code="1")
    chad = User(fname="Chad", lname="Bradley", email="chad@gmail.com", password="ccc", status_code="2")
    rachel = User(fname="Rachel", lname="Wang", email="rachel@gmail.com", password="haha", status_code="2")
    jon = User(fname="Jon", lname="Whiteaker", email="jon@gmail.com", password="wow", status_code="1")

    db.session.add(liz)
    db.session.add(ash)
    db.session.add(tk)
    db.session.add(jess)
    db.session.add(chad)
    db.session.add(rachel)
    db.session.add(jon)

    db.session.commit()

def load_statuses():
    """Load status options into database."""

    resident = Status(r_or_v="Resident")
    visitor = Status(r_or_v="Visitor")

    db.session.add(resident)
    db.session.add(visitor)

    db.session.commit()


def load_neighborhoods(neighborhood_filename):
    """Load nighborhoods from u.neighborhoodinto database."""

    for i, row in enumerate(open(neigborhood_filename)):
        row = row.rstrip()

        # unpack the row
        neighborhood_id, name, description = row.split("|")


        db.session.add(movie)

    db.session.commit()

def load_places_to_visit(places_filename):
    """Load places from u.place into database."""

    for i, row in enumerate(open(places_filename)):
        row = row.rstrip()

        # unpack the row
        place_id, name, neighborhood_id = row.split("|")


        db.session.add(movie)

    db.session.commit()



# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    neighborhood_filename = "seed_data/u.neighborhood"
    places_filename = "seed_data/u.place"

    load_neighborhoods(neighborhood_filename)
    load_places_to_visit(places_filename)

