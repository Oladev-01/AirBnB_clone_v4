#!/usr/bin/python3

"""
view for City objects that handles all default
RESTful API
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def all_cities(state_id):
    """
    return a json of all the cities associated to a
    state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = storage.all(City)
    state_cities = []
    for city in all_cities.values():
        if city.state_id == state.id:
            state_cities.append(city.to_dict())
    return jsonify(state_cities)


@app_views.route("cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    return a json representation of a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    delete a city object from the storage
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
    add a new city object to the storage linked to
    a state
    """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if "name" not in json_data:
        abort(400, description="Missing name")
    json_data["state_id"] = state_id
    new_city = City(**json_data)
    new_city.save()
    return jsonify(new_city.to_dict())


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def modify_city(city_id):
    """
    update the city object identify by it's id
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in json_data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
