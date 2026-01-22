import os
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, jwt, bcrypt, ma  # <--- Importamos jwt también
from .routes.usuarios import usuarios_bp
from .routes.main import main_bp
from .routes.auth import auth_bp
from .errors import registrar_errores

# Importaremos el nuevo blueprint de auth más abajo

load_dotenv()


def create_app():
    app = Flask(__name__)

    # --- Configuración de Base de Datos ---
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Configuración de JWT (NUEVO) ---
    # En producción, pon esto en tu archivo .env
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "clave_super_secreta_cambiar_esto")

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    # --- Inicializar Extensiones ---
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)# <--- Inicializamos JWT
    ma.init_app(app)

    registrar_errores(app)
    # --- Registrar Blueprints ---
    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)

    # Registraremos el nuevo blueprint de autenticación aquí
    from .routes.auth import auth_bp  # Importación local para evitar ciclos
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app