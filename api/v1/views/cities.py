#!/usr/bin/python3
"""Module handles all default RestFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.base_model import BaseModel
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                strict_slashes=False)
def get_citiesState(state_id):
    """Retrieves a city object"""
    state = storage.get(State, state_id)
    cities_list = []
    if state:
        for city in state.cities:
            cities_list.append(city.to_dict())
            return jsonify(cities_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                strict_slashes=False)
def delete_cities(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city in None:
        abort(404)
        city_dict = {}
        city.delete()
        storage.save()
        return jsonify(city_dict), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(404, 'Not a JSON')
    elif 'name' not in json_req:
        abort(404, 'Missing name')
    json_req['state_id'] = state_id
    new_city = City(**json_req)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                strict_slashes=False)
def update_city(city_id):
    """Update City object"""
    if city_id:
        json_req = request.get_json()
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if json_req is None:
            abort(404, "Not a JSON")
        for key, val in json_req.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        storage.save()
        return jsonify(city.to_dict()), 200
