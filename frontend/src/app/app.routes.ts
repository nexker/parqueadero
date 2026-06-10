import { Routes } from '@angular/router';
import { IngresoComponent } from './components/ingreso/ingreso';
import { SalidaComponent } from './components/salida/salida';
import { ActivosComponent } from './components/activos/activos';

export const routes: Routes = [
  { path: '', redirectTo: 'ingreso', pathMatch: 'full' },
  { path: 'ingreso', component: IngresoComponent },
  { path: 'salida', component: SalidaComponent },
  { path: 'activos', component: ActivosComponent }
];