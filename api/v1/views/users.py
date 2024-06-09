#!/usr/bin/python3

"""
view for User objects that handles all default RESTful
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def all_users():
    """
    return a json format of all users
    """

    all_users = storage.all(User)
    list_all_users = []
    for user in all_users.values():
        list_all_users.append(user.to_dict())
    return jsonify(list_all_users)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """
    return a specific user object with a particular id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    delete a user object from the storage with
    a particular id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        user.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """
    create a new user object and add to the storage
    """

    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if "email" not in json_data:
        abort(400, description="Missing email")
    if "password" not in json_data:
        abort(400, description="Missing password")
    new_user = User(**json_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/user/<user_id>", methods=["PUT"], strict_slashes=False)
def modify_user(user_id):
    """
    modify a user objecte from the storage
    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        elif key == "email":
            continue
        else:
            setattr(state, key, value)
    user.save()
    return jsonify(user.to_dict())
