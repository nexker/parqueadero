import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VehiculoService } from '../../services/vehiculo';

@Component({
  selector: 'app-salida',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './salida.html',
  styleUrl: './salida.css'
})
export class SalidaComponent implements OnInit {
  vehiculos: any[] = [];
  idSeleccionado: number | null = null;
  email = '';
  resultado: any = null;
  mensaje = '';
  error = '';
  cargando = false;

  constructor(
    private vehiculoService: VehiculoService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.cargarActivos();
  }
  /**
  * Captura el vehículo seleccionado desde la interfaz
  * y almacena su identificador para el procesamiento
  * posterior de la salida.
  */
  onVehiculoChange(event: Event) {
    const val = (event.target as HTMLSelectElement).value;
    this.idSeleccionado = val ? Number(val) : null;
  }
  /**
  * Actualiza el correo electrónico ingresado por el usuario.
  * Este correo será utilizado para enviar el resumen de la estancia.
  */
  onEmailChange(event: Event) {
    this.email = (event.target as HTMLInputElement).value;
  }
  /**
  * Obtiene desde el backend los vehículos que actualmente
  * permanecen dentro del parqueadero.
  * Esta información se utiliza para poblar el listado
  * de selección de vehículos disponibles para salida.
  */
  cargarActivos() {
    this.vehiculoService.getVehiculosActivos().subscribe({
      next: (data) => {
        this.vehiculos = data;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Error al cargar vehículos';
        this.cdr.detectChanges();
      }
    });
  }
  /**
  * Registra la salida de un vehículo del parqueadero.
  * Flujo:
  * 1. Valida que exista un vehículo seleccionado.
  * 2. Envía la solicitud de salida al backend.
  * 3. Recibe el resumen de permanencia.
  * 4. Actualiza la lista de vehículos activos.
  * 5. Genera el envío del correo electrónico desde el backend.
  */
  registrarSalida() {
    if (!this.idSeleccionado) {
      this.error = 'Selecciona un vehículo';
      return;
    }
    this.cargando = true;
    this.mensaje = '';
    this.error = '';
    this.resultado = null;
    this.cdr.detectChanges();

    this.vehiculoService.registrarSalida(this.idSeleccionado, this.email).subscribe({
      next: (res: any) => {
        this.resultado = res;
        this.mensaje = '✅ Salida registrada correctamente';
        this.cargando = false;
        this.cargarActivos();
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        const msg = err?.error?.error || 'Error al registrar la salida';
        this.error = `❌ ${msg}`;
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }
}