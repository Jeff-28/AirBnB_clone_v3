#!/usr/bin/python3
"""
Contains a view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def statesList():
    """Retrieves the list of all State objects"""
    statesList = []
    statesDict = storage.all('State')
    for key, state in statesDict.items():
        statesList.append(state.to_dict())
    return jsonify(statesList)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def state(state_id):
    """Retrieves State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id):
    """Deletes a State by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    """Creates a new State"""
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_req:
        abort(400, 'Missing name')
    newState = State(**json_req)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def updateState(state_id):
    """Updates a State object"""
    if state_id:
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        for key, value in json_req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
