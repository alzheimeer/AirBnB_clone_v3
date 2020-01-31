#!/usr/bin/python3
""" View State """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    states_list = []
    states_objs = storage.all('State').values()
    for element in states_objs:
        states_list.append(element.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def stateId(state_id):
    """id state retrieve json object"""
    s = storage.all('State').values()
    for v in s:
        if v.id == state_id:
            return jsonify(v.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=["DELETE"], strict_slashes=False)
def stateDel(state_id):
    """delete state with id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def statePost():
    """ POST a new state"""
    x = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")
    if not state_data.get('name'):
        abort(400, "Missing name")
    s = State(**x)
    storage.new(statePost)
    storage.save()
    return jsonify(statePost.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def statePut(state_id):
    """Update a State object"""
    x = request.get_json()
    if x is None:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for k, v in x.items():
        if k not in ignore:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
