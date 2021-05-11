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


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_palce_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get('Place', place_id)
    amenities_list = []
    if place is None:
        abort(404)
    for amenity in place.amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    amenity_dict = {}
    place.amenity_ids.remove(amenity)
    place.save()
    return jsonify(amenityto_dict), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    place.amenity_ids.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
