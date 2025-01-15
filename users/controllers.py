from flask import jsonify
from extensions import db
from models import User

# Función para crear usuario
def create_user(data):
    # Si no hay X dato, manda un jsonify
    if not data.get('username') or not data.get('email') or not data.get('password'): 
        return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

    # Si el correo ya existe, manda un jsonify
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El correo ya está registrado.'}), 400

    # Creando un nuevo usuario en la base de datos y manda mensaje exitoso
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente.'}), 201

# Función para obtener todos los usuarios
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id, 
        'username': user.username,
        'email': user.email,
    } for user in users]
    return jsonify(user_list), 200

# Función para actualizar un usuario
def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    # Actualizar solo los campos que estén en el data
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    # Si se recibe una nueva contraseña, actualizarla
    if data.get('password'):
        user.password = data['password']

    db.session.commit()
    return jsonify({'message': 'Usuario actualizado exitosamente.'}), 200

# Función para eliminar un usuario
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado exitosamente.'}), 200
