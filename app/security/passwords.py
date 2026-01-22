from ..extensions import bcrypt

def hashear_contrasena(password_texto_plano):
    """
    Recibe una contraseña en texto plano y retorna el hash seguro usando Bcrypt.
    """
    # generate_password_hash devuelve bytes, usamos decode para guardarlo como string en la BD
    return bcrypt.generate_password_hash(password_texto_plano).decode('utf-8')

def verificar_contrasena(hash_guardado, password_texto_plano):
    """
    Compara el hash de la base de datos con la contraseña ingresada.
    Retorna True si coinciden.
    """
    return bcrypt.check_password_hash(hash_guardado, password_texto_plano)