from flask import Blueprint, request, jsonify
from .models import registrar_ingreso, registrar_salida, get_vehiculos_activos, get_todos_registros
from .email_service import enviar_correo_salida

bp = Blueprint('api', __name__, url_prefix='/api')
# Blueprint encargado de agrupar todos los endpoints relacionados con la gestión del parqueadero.
@bp.route('/vehiculos/activos', methods=['GET'])
def activos():
    """
    Obtiene todos los vehículos que actualmente
    permanecen dentro del parqueadero
    Returns:
        JSON: Lista de vehículos activos
    """
    try:
        vehiculos = get_vehiculos_activos()
        return jsonify(vehiculos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/vehiculos', methods=['GET'])
def todos():
    """
    Obtiene el historial completo de registros
    almacenados en el sistema.
    Returns:
        JSON: Lista de ingresos y salidas registradas
    """
    try:
        registros = get_todos_registros()
        return jsonify(registros), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/vehiculo/ingreso', methods=['POST'])
def ingreso():
    """
    Registra el ingreso de un vehículo al parqueadero
    Validaciones:
    - tipo_vehiculo obligatorio
    - placa obligatoria
    - tipo debe ser Carro o Moto
    Returns:
        JSON: Identificador del registro creado
    """
    try:
        # Obtiene los datos enviados desde el frontend.
        data = request.get_json()
        tipo = data.get('tipo_vehiculo')
        placa = data.get('placa', '').upper().strip()
        # Valida que los campos requeridos existan.
        if not tipo or not placa:
            return jsonify({"error": "tipo_vehiculo y placa son obligatorios"}), 400
        if tipo not in ['Carro', 'Moto']:
            return jsonify({"error": "tipo_vehiculo debe ser Carro o Moto"}), 400
        # Registra el ingreso del vehículo.
        id_registro = registrar_ingreso(tipo, placa)
        return jsonify({"mensaje": "Ingreso registrado", "id": id_registro}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/vehiculo/salida/<int:id_registro>', methods=['POST'])
def salida(id_registro):
    """
    Registra la salida de un vehículo del parqueadero
    Procesos realizados:
    - Cierra el registro activo
    - Calcula tiempo de permanencia
    - Calcula valor a pagar
    - Envía correo electrónico opcional
    Returns:
        JSON: Resumen completo de la estancia
    """
    try:
        # Obtiene el correo electrónico enviado desde la interfaz de usuario.
        data = request.get_json()
        email_destinatario = data.get('email', '')
        # Ejecuta la lógica de salida.
        registro = registrar_salida(id_registro)
        # Verifica que exista un registro activo.
        if not registro:
            return jsonify({"error": "Registro no encontrado o vehículo ya salió"}), 404
        # Si el usuario proporcionó correo, se envía automáticamente el resumen
        # de la estancia del vehículo.
        if email_destinatario:
            enviar_correo_salida(registro, email_destinatario)

        return jsonify(registro), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500