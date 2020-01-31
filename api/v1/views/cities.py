#!/usr/bin/python3
""" View State """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route("/states/<id>/cities", methods=["GET"])
def cityAll(id):
    """id state retrieve json object with his cities"""
    ll = []
    s = storage.all('State').values()
    ss = storage.all('City').values()
    for v in s:
        if v.id == id:
            for vv in ss:
                if vv.state_id == id:
                    ll.append(vv.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/cities/<id>", methods=["GET"])
def cityId(id):
    """id city retrieve json object"""
    ll = []
    s = storage.all('City').values()
    for v in s:
        if v.id == id:
            ll.append(v.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/cities/<id>", methods=["DELETE"])
def cityDel(id):
    """delete city with id"""
    city = storage.get("City", id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<id>/cities', methods=['POST'])
def cityPost(id):
    """ POST a new state"""
    if storage.get("State", id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    x['state_id'] = str(id)
    if "name" not in x:
        return jsonify({"error": "Missing name"}), 400
    s = City(**x)
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/cities/<id>', methods=['PUT'])
def cityPut(id):
    """ Update a State object """
    ignore = ["id", "update_at", "created_at", "state_id"]
    city = storage.get("City", id)
    if city is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    for k, v in x.items():
        if k not in ignore:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
