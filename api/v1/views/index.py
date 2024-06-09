#!/usr/bin/python3
"""routing"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns JSON with status: OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats",methods=['GET'], strict_slashes=False)
def stats():
    """
    return the stats of all the objects in the
    database
    """
    stats = {"amenities" : storage.count(cls=Amenity),
             "cities" : storage.count(cls=City),
             "places" : storage.count(cls=Place),
             "reviews": storage.count(cls=Review),
             "states" : storage.count(cls=State),
             "users" : storage.count(cls=User)
             }
    return jsonify(stats)
