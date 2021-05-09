#!/usr/bin/python3
"""
Contains a view for User objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def userList():
    """Retrieves the list of all User objects"""
    userList = []
    userDict = storage.all('User')
    for key, user in userDict.items():
        userList.append(user.to_dict())
    return jsonify(userList)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def user(user_id):
    """Retrieves User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    """Deletes a User by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """Creates a new User"""
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if 'email' not in json_req:
        abort(400, 'Missing email')
    if 'password' not in json_req:
        abort(400, 'Missing password')
    newUser = User(**json_req)
    newUser.save()
    return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def updateUser(user_id):
    """Updates a User object"""
    if user_id:
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        for key, value in json_req.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
