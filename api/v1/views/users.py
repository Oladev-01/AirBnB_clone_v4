#!/usr/bin/python3

"""
a view for Amenity objects that handles all default
RESTFUL API actions
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """
    return all Amenity objects in the storage
    """
    all_amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in all_amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """
    return a particular Amenity object with the specified id
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete a particular Amenity object with specified id
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """
    Add a new Amenity object to the storage
    """
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if "name" not in json_data:
        abort(400, description="Missing name")
    new_amenity = Amenity(**json_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def modify_amenity(amenity_id):
    """
    update the amenity object specified with the id
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400)
    for key, value in json_data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
