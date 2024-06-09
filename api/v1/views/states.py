#!/usr/bin/python3

"""
view for State objects that handles all default RESTful 
"""

from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route("/states", strict_slashes=False)
def all_states():
    """
    return a json format of all states
    """

    all_states =  storage.all(State)
    list_all_states = []
    for state in all_states.values():
        list_all_states.append(state.to_dict())
    return jsonify(list_all_states)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """
    return a specific state object with a particular id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    delete a state object from the storage with
    a particular id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """
    create a new state object and add to the storage
    """

    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if "name" not in json_data:
        abort(400, description="Missing name")
    new_state = State(**json_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def modify_state(state_id):
    """
    modify a state objecte from the storage
    """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
