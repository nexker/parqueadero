import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActivosComponent } from './activos';

describe('Activos', () => {
  let component: ActivosComponent;
  let fixture: ComponentFixture<ActivosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ActivosComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ActivosComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
