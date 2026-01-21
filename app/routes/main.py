from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return {"message": "API REST con MySQL funcionando (Modular)"}

@main_bp.route("/ping", methods=["GET"])
def ping():
    return {"pong": True}