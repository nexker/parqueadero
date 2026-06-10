CREATE DATABASE IF NOT EXISTS parqueadero;
USE parqueadero;

CREATE TABLE registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_vehiculo ENUM('Carro', 'Moto') NOT NULL,
    placa VARCHAR(6) NOT NULL,
    fecha_ingreso DATETIME NOT NULL,
    fecha_salida DATETIME NULL,
    minutos INT NULL,
    valor DECIMAL(10,2) NULL
);