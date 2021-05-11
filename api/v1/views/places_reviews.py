#!/usr/bin/python3
"""Module handles all default RestFul API actions"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.city import City
from models.base_model import BaseModel
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get('Place', place_id)
    list_reviews = []
    if place is None:
        abort(404)
    for review in place.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    empty_dict = {}
    review.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(400, "Not a JSON")
    if "user_id" not in json_req:
        abort(400, "Missing user_id")
    user = storage.get('User', json_req["user_id"])
    if user is None:
        abort(404)
    if "text" not in json_req:
        abort(400, "Missing text")
    json_req["place_id"] = place_id
    new_review = Review(**json_req)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    json_req = request.get_json()
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if json_req is None:
        abort(400, "Not a JSON")
    for key, value in json_req.items():
        if key not in ["id", "created_at",
                       "updated_at", "user_id",
                       "place_id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
