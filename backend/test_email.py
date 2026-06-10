import requests
import json
# Script de validación para comprobar la autenticación
# y el envío de correos mediante la API externa.
BASE_URL = "https://dev-sites.similtech.co/api-email"
USERNAME = "proceso_pruebas"
PASSWORD = "das487d32_*"

def test_envio_correo():
    # 1. Obtener token
    token_response = requests.post(f"{BASE_URL}/api/token", json={
        "username": USERNAME,
        "password": PASSWORD
    })
    token = json.loads(token_response.text)['token']
    print(f"Token obtenido: {token[:30]}...")

    # 2. Enviar correo
    payload = {
        "configParams": {
            "idUser": "parqueadero_app",
            "idMessage": "test_correo_001"
        },
        "receivers": {
            "emailOrigen": "",
            "to": ["nelson27ayala@gmail.com"],
            "copyTo": [],
            "hiddenCopyTo": []
        },
        "email": {
            "subject": "Prueba envío correo - Parqueadero",
            "urlHeader": "",
            "urlFooter": "",
            "message": "<h2>Prueba exitosa</h2><p>El servidor de correo está funcionando correctamente.</p>",
            "url_files": []
        }
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/email/sendEmail", json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.text}")

if __name__ == "__main__":
    test_envio_correo()