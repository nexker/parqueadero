import requests
import os
from dotenv import load_dotenv
from datetime import datetime
# Carga las variables de entorno utilizadas para la
# autenticación y configuración del servicio de correo.
load_dotenv()

BASE_URL = os.getenv('API_EMAIL_URL')
USERNAME = os.getenv('API_EMAIL_USER')
PASSWORD = os.getenv('API_EMAIL_PASSWORD')
ID_USER = os.getenv('API_EMAIL_ID_USER')

def get_token():
    """
    Obtiene un token de autenticación desde la API de correos.
    El token es requerido para autorizar el envío de mensajes
    mediante los endpoints protegidos del servicio.
    Returns:
        str: Token de acceso válido.
    """
    response = requests.post(f"{BASE_URL}/api/token", json={
        "username": USERNAME,
        "password": PASSWORD
    })
    response.raise_for_status()
    token = response.text.strip().strip('"')
    print(f"TOKEN OBTENIDO: {token}")
    return token

def enviar_correo_salida(registro, email_destinatario):
    """
    Envía al usuario un correo electrónico con el resumen
    del vehículo en el parqueadero.
    La información enviada incluye:
    - Placa.
    - Tipo de vehículo.
    - Fecha de ingreso.
    - Fecha de salida.
    - Tiempo total de permanencia.
    - Valor total a pagar.
    Args:
        registro (dict): Información del registro de parqueo.
        email_destinatario (str): Correo del destinatario.
    """
    try:
        import json
        print(f"Intentando obtener token con usuario: {USERNAME}")
        # Solicita un token de autenticación para consumir el servicio de envío de correos.
        token_response = requests.post(f"{BASE_URL}/api/token", json={
            "username": USERNAME,
            "password": PASSWORD
        })
        print(f"Status token: {token_response.status_code}")
        token_data = json.loads(token_response.text)
        token = token_data['token']
        print(f"Token limpio: {token}")
        # Genera un identificador único para cada correo enviado.
        # Se utiliza la placa y la marca de tiempo actual.
        id_message = f"{registro['placa']}_{int(datetime.now().timestamp())}"
        # Construcción dinámica del contenido HTML enviado al usuario.
        mensaje = f"""
        <h2>Resumen de parqueo</h2>
        <p><b>Placa:</b> {registro['placa']}</p>
        <p><b>Tipo de vehículo:</b> {registro['tipo_vehiculo']}</p>
        <p><b>Ingreso:</b> {registro['fecha_ingreso']}</p>
        <p><b>Salida:</b> {registro['fecha_salida']}</p>
        <p><b>Tiempo total:</b> {registro['minutos']} minutos</p>
        <p><b>Valor a pagar:</b> ${registro['valor']:,}</p>
        """
        # Estructura requerida por la API externa
        # para el envío de correos electrónicos.
        payload = {
            "configParams": {
                "idUser": ID_USER,
                "idMessage": id_message
            },
            "receivers": {
                "emailOrigen": "",
                "to": [email_destinatario],
                "copyTo": [],
                "hiddenCopyTo": []
            },
            "email": {
                "subject": f"Salida del vehículo {registro['placa']} - Parqueadero",
                "urlHeader": "",
                "urlFooter": "",
                "message": mensaje,
                "url_files": []
            }
        }
        # Token requerido por la API para autorizar la operación de envío.
        headers = {"Authorization": f"Bearer {token}"}
        print(f"Enviando correo a: {email_destinatario}")
        response = requests.post(f"{BASE_URL}/api/email/sendEmail", json=payload, headers=headers)
        print(f"Status correo: {response.status_code}")
        print(f"Respuesta correo: {response.text}")
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False