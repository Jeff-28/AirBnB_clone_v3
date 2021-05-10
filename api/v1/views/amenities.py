#!/usr/bin/python3
"""Module handles all default RestFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.base_model import BaseModel
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amty_list = []
    for amty in storage.all('Amenity').values():
        amty_list.append(amty.to_dict())
    return jsonify(amty_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amty = storage.get(Amenity, amenity_id)
    if amty is None:
        abort(404)
    return jsonify(amty.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amty = storage.get(Amenity, amenity_id)
    if amty is None:
        abort(404)
    amty_dict = {}
    amty.delete()
    storage.save()
    return jsonify(amty_dict), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    elif 'name' not in json_req:
        abort(400, 'Missing name')
    newAmenity = Amenity(**json_req)
    newAmenity.save()
    return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """Updates an Amenity by id"""
    if amenity_id:
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        for key, value in json_req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
