from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Crea y configura la instancia principal de la aplicación Flask.
    Configuraciones realizadas:
    - Inicialización de la aplicación.
    - Habilitación de CORS para permitir peticiones desde el frontend Angular.
    - Registro de las rutas definidas mediante Blueprints.
    Returns:
        Flask: Instancia configurada de la aplicación.
    """
    app = Flask(__name__)
    CORS(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app