#!/usr/bin/python3
""" View Amenity """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity



@app_views.route("/amenities", methods=["GET"])
def amenityAll():
    """Retrieves all amenities with a list of objects"""
    ll = []
    s = storage.all('Amenity').values()
    for v in s:
        ll.append(v.to_dict())
    return jsonify(ll)


@app_views.route("/amenities/<id>", methods=["GET"])
def amenityId(id):
    """id Amenity retrieve json object"""
    ll = []
    s = storage.all('Amenity').values()
    for v in s:
        if v.id == id:
            ll.append(v.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/amenities/<id>", methods=["DELETE"])
def amenityDel(id):
    """delete Amenity with id"""
    amenity = storage.get("Amenity", id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def amenityPost():
    """ POST a new amenity"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    x = request.get_json()
    s = Amenity(**x)
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/amenities/<id>', methods=['PUT'])
def amenityPut(id):
    """ Update a amenity object """
    ignore = {"id", "created_at", "updated_at"}
    amenity = storage.get("Amenity", id)
    if amenity is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    for k, v in x.items():
        if k not in ignore:
            setattr(amenity, k, v)
    return jsonify(amenity.to_dict()), 200