import pymysql
import os
from dotenv import load_dotenv
# Carga las variables definidas en el archivo .env
load_dotenv()

def get_connection():
    """
    Crea y retorna una conexión a la base de datos MySQL.
    La configuración se obtiene desde variables de entorno
    para facilitar la portabilidad entre diferentes entornos
    (desarrollo, pruebas y producción).
    Returns:
        pymysql.Connection: Conexión activa a la base de datos.
    """
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'root1234'),
        database=os.getenv('DB_NAME', 'parqueadero'),
        cursorclass=pymysql.cursors.DictCursor,
        init_command="SET time_zone = '-05:00'"
    )