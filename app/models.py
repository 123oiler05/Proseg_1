from .extensions import db


class User(db.Model):
    __tablename__ = 'users'  # Buena práctica: definir nombre de tabla explícito

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    nombre_usuario = db.Column(db.String(80), nullable=False, unique=True)
    contrasena = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "email": self.email,
            "nombre_usuario": self.nombre_usuario
        }