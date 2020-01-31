#!/usr/bin/python3
""" View State """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
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


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_cities(state_id):
    """ POST a new cities, by typing the name and the id """
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    # Adding state_id as attribute
    content['state_id'] = str(state_id)
    # Imitating create in console
    city = City(**content)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_cities(city_id):
    """ Update a city object """
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key is not 'id' and \
           key is not 'state_id' and \
           key is not 'created_at' and \
           key is not 'updated_at':
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
