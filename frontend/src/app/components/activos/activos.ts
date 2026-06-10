import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VehiculoService } from '../../services/vehiculo';

@Component({
  selector: 'app-activos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './activos.html',
  styleUrl: './activos.css'
})
export class ActivosComponent implements OnInit, OnDestroy {
  vehiculos: any[] = [];
  error = '';
  /**
  * actualizar periódicamente la lista de vehículos.
  */
  private intervalo: any;
  /**
  * Servicio encargado de la comunicación con la API REST, permitiendo 
  * consultar los vehículos activos registradosen el parqueadero.
  * ChangeDetectorRef:
  * Utilizado para forzar la actualización de la interfaz
  * cuando se reciben datos asíncronos desde el backend.
  */
  constructor(
    private vehiculoService: VehiculoService,
    private cdr: ChangeDetectorRef
  ) {}
  /**
  * Al iniciar el componente se realiza una consulta inicial
  * de los vehículos activos y posteriormente se configura una
  * actualización automática cada 5 segundos para mantener
  * la información sincronizada con el estado del parqueadero.
  */
  ngOnInit() {
    this.cargar();
    this.intervalo = setInterval(() => this.cargar(), 5000);
  }

  ngOnDestroy() {
    clearInterval(this.intervalo);
  }

  cargar() {
    this.vehiculoService.getVehiculosActivos().subscribe({
      next: (data) => {
        this.vehiculos = data;
        this.error = '';
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Error al cargar vehículos activos';
        this.cdr.detectChanges();
      }
    });
  }
}