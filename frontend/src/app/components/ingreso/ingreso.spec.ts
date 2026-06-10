import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IngresoComponent } from './ingreso';

describe('Ingreso', () => {
  let component: IngresoComponent;
  let fixture: ComponentFixture<IngresoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IngresoComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(IngresoComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
