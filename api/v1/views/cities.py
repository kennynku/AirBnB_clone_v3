#!/usr/bin/python3
'''Includes the cities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """Recovers the list of all City objects of a State"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)
    return jsonify([city.to_dict() for city in obj_state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def single_city(city_id):
    """Recovers a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Returns an empty dictionary with the 200 status code"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Returns the new City with 201 status code"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if 'name' not in new_city:
        abort(400, "Missing name")

    obj = City(**new_city)
    setattr(obj, 'state_id', state_id)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Returns the City object with 200 status code"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'created_at', 'update_at', 'state_id']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)