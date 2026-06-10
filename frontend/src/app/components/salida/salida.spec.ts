import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalidaComponent } from './salida';

describe('Salida', () => {
  let component: SalidaComponent;
  let fixture: ComponentFixture<SalidaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SalidaComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SalidaComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
