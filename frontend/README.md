# Sistema de Gestión de Parqueadero

Aplicación web para gestionar el ingreso y salida de vehículos, calcular tarifas y notificar por correo electrónico.

## Tecnologías

- **Frontend:** Angular 22
- **Backend:** Python Flask
- **Base de datos:** MySQL 8
- **API externa:** Similtech Email API

## Estructura del proyecto

parqueadero/
├── frontend/        # Aplicación Angular
├── backend/         # API REST Flask
├── database.sql     # Script de base de datos
└── README.md

## Requisitos previos

- Python 3.x
- Node.js 18+
- MySQL 8.x
- Angular CLI (`npm install -g @angular/cli`)

## Configuración

### 1. Base de datos
Abrir MySQL Workbench y ejecutar el script `database.sql`.

### 2. Variables de entorno del backend

Renombra el archivo `backend/.env.example` a `backend/.env`.
Completa `DB_PASSWORD` con tu contraseña de MySQL.
Las demás credenciales ya están incluidas en el archivo de ejemplo.

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=TU_CONTRASEÑA_MYSQL
DB_NAME=parqueadero
API_EMAIL_URL=https://dev-sites.similtech.co/api-email
API_EMAIL_USER=TU_USUARIO_API_EMAIL
API_EMAIL_PASSWORD=TU_PASSWORD_API_EMAIL
API_EMAIL_ID_USER=parqueadero_app
```

> Las credenciales de la API de correo fueron proporcionadas junto con el enunciado de la prueba técnica. o enviadas al mismo correo de confirmaciond de la prueba tecnica.

## Instalación y ejecución

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors pymysql python-dotenv requests pytz
python run.py
```
El backend corre en `http://127.0.0.1:5000`

### Frontend
```bash
cd frontend
npm install
ng serve
```
El frontend corre en `http://localhost:4200`

## Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/vehiculos/activos | Lista vehículos activos en el parqueadero |
| POST | /api/vehiculo/ingreso | Registrar ingreso de vehículo |
| POST | /api/vehiculo/salida/{id} | Registrar salida y calcular cobro |

### Ejemplo ingreso
```json
POST /api/vehiculo/ingreso
{
  "tipo_vehiculo": "Carro",
  "placa": "ABC123"
}
```

### Ejemplo salida
```json
POST /api/vehiculo/salida/1
{
  "email": "correo@ejemplo.com"
}
```

## Tarifa
- **$50 por minuto** de permanencia

## Nota sobre el envío de correos
La integración con la API de correo está implementada y funcional. El sistema obtiene el token de autenticación y envía el payload correctamente, recibiendo respuesta `200` con mensaje de éxito. Si el correo no llega al destinatario, puede deberse a la configuración del servidor SMTP en el ambiente de pruebas.

## Autor
**Nelson Andrés Ayala Álvarez**  
Ingeniería de Sistemas — Universidad Libre