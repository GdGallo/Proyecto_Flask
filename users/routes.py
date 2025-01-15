from flask import request, jsonify
from . import users_bp
from .controllers import create_user, get_users, update_user, delete_user

@users_bp.route('/users', methods=['POST'])
def create():
    data = request.get_json()
    return create_user(data)

@users_bp.route('/users', methods=['GET'])
def list_users():
    return get_users()

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = request.get_json()
    return update_user(user_id, data)

@users_bp.route('/users/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    return delete_user(user_id)