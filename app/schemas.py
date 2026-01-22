from .extensions import ma
from .models import User
from marshmallow import fields, validate


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Permite cargar datos directamente al modelo
        # Excluimos campos que JAMÁS deben salir de la API (ni siquiera el hash)
        exclude = ('id',)  # Opcional: si no quieres mostrar el ID interno

    # --- POLÍTICA DE DATOS SENSIBLES ---

    # 1. Validación de Email: Asegura que tenga formato correcto
    email = fields.Email(required=True)

    # 2. Validación de Contraseña: Mínimo 6 caracteres
    # load_only=True: IMPORTANTE. Significa que la API acepta la contraseña para crear/login,
    # pero NUNCA la devolverá en un JSON de respuesta (GET/PUT).
    contrasena = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, error="La contraseña debe tener al menos 6 caracteres")
    )

    # 3. Validaciones extras
    edad = fields.Integer(validate=validate.Range(min=18, max=100, error="Debes ser mayor de edad"))

    # Campos de solo lectura (el usuario no puede cambiarlos manualmente enviando un JSON)
    id = fields.Integer(dump_only=True)


# Instancias para usar en las rutas
user_schema = UserSchema()  # Para un solo usuario
users_schema = UserSchema(many=True)  # Para listas de usuarios