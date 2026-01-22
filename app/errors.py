from flask import jsonify


def registrar_errores(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Solicitud incorrecta (Bad Request)"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "No autorizado. Token faltante o inválido"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Error interno del servidor"}), 500

    # Captura genérica de excepciones para evitar HTML
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "error": "Error inesperado",
            "mensaje": str(e)  # En producción, quitar 'str(e)' para no revelar detalles
        }), 500