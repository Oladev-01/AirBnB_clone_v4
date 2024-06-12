#!/usr/bin/python3

"""
cotains all the route for the cities api
"""

from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request


@app_views.route("cities/<city_id>/places/",
                 methods=["GET"], strict_slashes=False)
def all_places(city_id):
    """
    return all the places that is associated to a city
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = storage.all(Place).values()
    city_places = []
    for place in all_places:
        if (city.id == place.city_id):
            city_places.append(place.to_dict())
    return jsonify(city_places)


@app_views.route("places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    return a place with the specified id from the storage
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route("places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    delete a place with the specified id from the storage
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def add_place(city_id):
    """
    add a new place to a city from the storage
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data["city_id"] = city.id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    update a place object from the storage with the specified id
    """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    ignored_value = ["id", "user_id", "city_id",
                     "updated_at", "created_at"]
    for key, value in data.items():
        if key not in ignored_value:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
