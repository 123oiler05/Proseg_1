from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from ..extensions import db
from ..models import User
from ..schemas import user_schema, users_schema
from ..security.passwords import hashear_contrasena

usuarios_bp = Blueprint('usuarios', __name__)


# --- CREAR (POST) ---
@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    json_data = request.get_json()

    try:
        # 1. Validar datos con Marshmallow
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # 2. Verificar duplicados (Email/Usuario)
    if User.query.filter((User.email == data['email']) | (User.nombre_usuario == data['nombre_usuario'])).first():
        return jsonify({"error": "El email o nombre de usuario ya existe"}), 400

    # 3. Hashear contraseña y crear modelo
    nuevo_usuario = User(
        nombre=data['nombre'],
        apellido=data['apellido'],
        edad=data['edad'],
        email=data['email'],
        nombre_usuario=data['nombre_usuario'],
        contrasena=hashear_contrasena(data['contrasena'])
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    # 4. Retornar datos limpios (sin contraseña)
    return user_schema.dump(nuevo_usuario), 201


# --- LEER TODOS (GET) ---
@usuarios_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    usuarios = User.query.all()
    return jsonify(users_schema.dump(usuarios)), 200


# --- LEER UNO (GET) ---
@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
@jwt_required()
def obtener_usuario(id):
    usuario = User.query.get_or_404(id)
    return user_schema.dump(usuario), 200


# --- ACTUALIZAR (PUT) ---
@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_usuario(id):
    usuario = User.query.get_or_404(id)
    data = request.get_json()

    # Actualización manual controlada
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.apellido = data.get("apellido", usuario.apellido)
    usuario.edad = data.get("edad", usuario.edad)
    usuario.email = data.get("email", usuario.email)
    usuario.nombre_usuario = data.get("nombre_usuario", usuario.nombre_usuario)

    # Nota: No permitimos cambiar contraseña aquí para mantener la seguridad simple.
    # Se debería hacer en un endpoint separado de "Cambiar Contraseña".

    db.session.commit()
    return user_schema.dump(usuario), 200


# --- ELIMINAR (DELETE) ---
@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"}), 200