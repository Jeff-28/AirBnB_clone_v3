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
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    if storage.get(City, city_id) is None:
        abort(404)
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    if "user_id" not in my_dict:
        abort(400, "Missing user_id")
    user = storage.get('User', my_dict["user_id"])
    if user is None:
        abort(404)
    if "name" not in my_dict:
        abort(400, "Missing name")
    my_dict["city_id"] = city_id
    new_place = Place(**my_dict)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    for key, value in my_dict.items():
        if key not in ["id", "user_id", "city_id" "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
