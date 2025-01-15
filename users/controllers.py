from flask import jsonify
from extensions import db
from models import User
from .schemas import UserSchema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

# Crear usuario
def create_user(data):
    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Verificar si el correo ya está registrado
    if User.query.filter_by(email=validated_data['email']).first():
        return jsonify({'error': 'El correo ya está registrado'}), 400

    # Crear nuevo usuario
    new_user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        password=generate_password_hash(validated_data['password']),  # Hashing de contraseña
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


# Obtener todos los usuarios
def get_users():
    users = User.query.all()
    return jsonify(user_list_schema.dump(users)), 200


# Actualizar un usuario
def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    try:
        validated_data = user_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Actualizar los datos del usuario
    user.username = validated_data.get('username', user.username)
    user.email = validated_data.get('email', user.email)

    if 'password' in validated_data:
        user.password = generate_password_hash(validated_data['password'])  # Hashing de contraseña

    db.session.commit()
    return jsonify({'message': 'Usuario actualizado exitosamente.'}), 200


# Eliminar un usuario
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado exitosamente.'}), 200
