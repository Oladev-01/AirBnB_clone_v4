#!/usr/bin/python3

"""
view for User object that handles all default RESTful API
action
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """
    return all the users in the storage
    """

    all_users = storage.all(User)
    user_list = []

    for user in all_users.values():
        user_list.append(user.to_dict())

    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    return a particular User object with the specified id
    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    delete a user object specified with the id
    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """
    add a new User object to the storage
    """
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JOSN")
    if "email" not in json_data:
        abort(400, description="Missing email")
    if "password" not in json_data:
        abort(400, description="Missing password")
    new_user = User(**json_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def modify_user(user_id):
    """
    update a particular user object with the specified id
    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key == "id" or key == "email":
            continue
        elif key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
