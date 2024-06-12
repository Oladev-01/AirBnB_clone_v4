#!/usr/bin/python3

"""
contains the view for Review objects that handles all
default RESTFul API actions
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """
    return all the reviews of a particular place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    all_reviews = storage.all(Review)
    reviews_list = []
    for review in all_reviews.values():
        if place_id == review.place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """
    return a review with a particular id
    """

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """
    delete a review with a particular id
    """

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def add_review(place_id):
    """
    add a new review to a place object
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if "user_id" not in json_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, json_data["user_id"])
    if user is None:
        abort(404)
    if "text" not in json_data:
        abort(400, description="Missing text")
    new_review = Review(**json_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def modify_review(review_id):
    """
    update the review object with the specified id
    """

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    try:
        json_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key == "user_id" or key == "place_id" or key == "id":
            continue
        elif key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(review, key, value)
    return jsonify(review.to_dict()), 200
