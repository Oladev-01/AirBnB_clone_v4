#!/usr/bin/python3

"""
a new view for Place objects that handles all default
RESTFul API actions
"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_city_places(city_id):
    """
    return all the places that is linked to
    a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = storage.all(Place)
    list_places = []
    for key, value in all_places.items():
        if value.city_id == city_id:
            list_places.append(value.to_dict())

    return jsonify(list_places)
