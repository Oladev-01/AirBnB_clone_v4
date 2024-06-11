#!/usr/bin/python3

"""
contains all route for the user
"""

from models.user import User
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request, make_response


@app_views.route("users", methods=["GET"], strict_slashes=False)
def get_users():
    """
    return all the users in the storage
    """
    all_users = storage.all(User).values()
    user_list = []
    for user in all_users:
        user_list.append(user.to_dict())

    return jsonify(user_list)


@app_views.route("users/<user_id>", methods=["GET"], strict_slashes=False)
def retrieve_user(user_id):
    """
    retrive a user with the specified id from the storage
    """

    user = storage.get(cls=User, id=user_id)
    if (user is not None):
        return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route("users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    delete a user with the specified id from the storage
    """

    user = storage.get(cls=User, id=user_id)
    if (user is not None):
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("users/", methods=["POST"], strict_slashes=False)
def add_user():
    """
    add a new user to the storage
    """

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return (new_user.to_dict()), 201


@app_views.route("users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    update a user from the storage with the specified id
    """

    user = storage.get(cls=User, id=user_id)
    if (user is None):
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    ignored_value = ["id", "email", "create_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_value:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
