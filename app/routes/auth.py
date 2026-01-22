from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
#from werkzeug.security import check_password_hash
from ..models import User
from ..security.passwords import verificar_contrasena

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    contrasena = data.get("contrasena")

    # 1. Buscar usuario por email
    usuario = User.query.filter_by(email=email).first()

    # 2. Verificar si existe y si la contraseña coincide
    if usuario and verificar_contrasena(usuario.contrasena, contrasena):
        # 3. Crear el token (identity suele ser el ID del usuario)
        access_token = create_access_token(identity=str(usuario.id))
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Credenciales inválidas"}), 401