#!/usr/bin/python3
"""Module for link between Place objects and Amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def retAinP(id):
    """ Retrieves [] of all Places amenities objects of a Place """
    ll = []
    place = storage.get("Place", str(id))
    if place is None:
        abort(404)
    amenities = place.amenities
    for x in amenities:
        ll.append(x.to_dict())
    return jsonify(ll)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delAinP(pid, aid):
    """Delete an amenity object from a place"""
    place = storage.get("Place", str(pid))
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", str(aid))
    if amenity is None:
        abort(404)
    amenities = place.amenity
    listA = [x.id for x in amenities]
    if amenity_id not in listA:
        abort(404)
    for x in amenities:
        if x.id == amenity_id:
            x.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def postAinP(pid, aid):
    """POST new amenity in id place """
    place = storage.get("Place", pid)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", aid)
    if amenity is None:
        abort(404)
    for x in place.amenities:
        if x.id == str(aid):
            return jsonify(x.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201