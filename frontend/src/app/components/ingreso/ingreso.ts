import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VehiculoService } from '../../services/vehiculo';

@Component({
  selector: 'app-ingreso',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ingreso.html',
  styleUrls: ['./ingreso.css']
})
export class IngresoComponent {
  tipo = 'Carro';
  placa = '';
  mensaje = '';
  error = '';
  /**
  * Controla el estado de carga durante la petición HTTP.
  * Permite bloquear acciones duplicadas mientras se procesa
  * el registro del vehículo.
  */
  cargando = false;
  /**
  * VehiculoService:
  * Encapsula la comunicación con la API REST encargada
  * de gestionar los ingresos y salidas del parqueadero.
  * ChangeDetectorRef:
  * Permite actualizar manualmente la interfaz después
  * de operaciones asíncronas.
  */
  constructor(
    private vehiculoService: VehiculoService,
    private cdr: ChangeDetectorRef
  ) {}

  onTipoChange(event: Event) {
    this.tipo = (event.target as HTMLSelectElement).value;
  }

  onPlacaChange(event: Event) {
    this.placa = (event.target as HTMLInputElement).value;
  }
  /**
  * Registra el ingreso de un vehículo al parqueadero.
  * Flujo:
  * 1. Normaliza la placa eliminando espacios y convirtiéndola a mayúsculas.
  * 2. Valida que la placa haya sido ingresada.
  * 3. Envía la información al backend.
  * 4. Muestra al usuario el resultado de la operación.
  */
  registrar() {
    const placaLimpia = this.placa.trim().toUpperCase();

    if (!placaLimpia) {
      this.error = 'La placa es obligatoria';
      this.mensaje = '';
      return;
    }

    this.cargando = true;
    this.mensaje = '';
    this.error = '';
    this.cdr.detectChanges();

    this.vehiculoService.registrarIngreso({
      tipo_vehiculo: this.tipo,
      placa: placaLimpia
    }).subscribe({
      next: (res: any) => {
        this.mensaje = `✅ Ingreso registrado correctamente. ID: ${res.id}`;
        this.placa = '';
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        const msg = err?.error?.error || 'Error al registrar el ingreso';
        this.error = `❌ ${msg}`;
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }
}