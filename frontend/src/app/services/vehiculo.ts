import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VehiculoService {
    /**
    * URL base de la API REST encargada de la gestión
    * de ingresos y salidas de vehículos del parqueadero.
    */
    private apiUrl = 'http://127.0.0.1:5000/api';
    /**
    * Enviar información en formato JSON hacia el backend.
    */
    private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    constructor(private http: HttpClient) {}
    /**
    * Obtiene el listado de vehículos que actualmente
    * se encuentran dentro del parqueadero.
    * @returns Observable con la lista de vehículos activos.
    */
    getVehiculosActivos(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/vehiculos/activos`);
    }
    /**
    * Registra el ingreso de un vehículo al parqueadero.
    * La información enviada incluye los datos capturados
    * desde el formulario de entrada.
    * @param data Datos del vehículo a registrar.
    * @returns Observable con la respuesta del servidor.
    */
    registrarIngreso(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/vehiculo/ingreso`, data, { headers: this.headers });
    }
    /**
    * Registra la salida de un vehículo y envía el correo
    * electrónico donde se notificará el tiempo total de
    * permanencia dentro del parqueadero.
    * @param id Identificador único del registro del vehículo.
    * @param email Correo electrónico del destinatario.
    * @returns Observable con el resumen de la operación.
    */
    registrarSalida(id: number, email: string): Observable<any> {
        return this.http.post(`${this.apiUrl}/vehiculo/salida/${id}`, { email }, { headers: this.headers });
    }
}