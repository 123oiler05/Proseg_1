from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash


from extensions import db


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")





app = Flask(__name__)

print("esta app ")


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


from models import User

@app.route("/")
def home():
    return {"message": "API REST con MySQL funcionando"}

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.get_json()

    campos_obligatorios = [
        "nombre",
        "apellido",
        "edad",
        "email",
        "nombre_usuario",
        "contrasena"
    ]

    for campo in campos_obligatorios:
        if campo not in data or data[campo] is None:
            return jsonify({
                "error": f"El campo '{campo}' es obligatorio"
            }), 400


    contrasena_hash = generate_password_hash(data["contrasena"])

    nuevo_usuario = User(
        nombre=data["nombre"],
        apellido=data["apellido"],
        edad=data["edad"],
        email=data["email"],
        nombre_usuario=data["nombre_usuario"],
        contrasena=contrasena_hash
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify(nuevo_usuario.to_dict()), 201



@app.route("/ping", methods=["GET"])
def ping():
    return {"pong": True}

@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    usuarios = User.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200

@app.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario(id):
    usuario = User.query.get(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario.to_dict()), 200

@app.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    usuario = User.query.get(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()

    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.apellido = data.get("apellido", usuario.apellido)
    usuario.edad = data.get("edad", usuario.edad)
    usuario.email = data.get("email", usuario.email)
    usuario.nombre_usuario = data.get("nombre_usuario", usuario.nombre_usuario)

    db.session.commit()

    return jsonify(usuario.to_dict()), 200

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = User.query.get(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado"}), 200


print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)


