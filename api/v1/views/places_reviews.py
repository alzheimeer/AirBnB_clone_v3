#!/usr/bin/python3
""" View State """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route("/states", methods=["GET"])
def statesAll():
    """Retrieves all states with a list of objects"""
    ll = []
    s = storage.all('State').values()
    for v in s:
        ll.append(v.to_dict())
    return jsonify(ll)


@app_views.route("/states/<id>", methods=["GET"])
def stateId(id):
    """id state retrieve json object"""
    ll = []
    s = storage.all('State').values()
    for v in s:
        if v.id == id:
            ll.append(v.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/states/<id>", methods=["DELETE"])
def stateDel(id):
    """delete state with id"""
    state = storage.get("State", id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def statePost():
    """ POST a new state"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    x = request.get_json()
    s = State(**x)
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'])
def statePut(id):
    """ Update a State object """
    ignore = {"id", "created_at", "updated_at"}
    state = storage.get("State", id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    for k, v in x.items():
        if k not in ignore:
            setattr(state, k, v)
    return jsonify(state.to_dict()), 200
