import { Component, OnInit } from '@angular/core';

@Component({
  standalone: false,
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent implements OnInit {
  isModalOpen = false;

  constructor() {}

  ngOnInit() {
    this.checkLastVisit();
  }

  setOpen(isOpen: boolean) {
    this.isModalOpen = isOpen;
  }

  checkLastVisit() {
    const lastVisit = localStorage.getItem('lastVisit');
    const currentTime = new Date().getTime();

    if (!lastVisit) {
      // Si no hay registro de la última visita
      this.isModalOpen = true;
    } else {
      const lastVisitTime = new Date(lastVisit).getTime();
      const time = 60 * 60 * 8000; // 8 horas en milisegundos
   

      if (currentTime - lastVisitTime > time) {
        // Si ha pasado más de una hora desde la última visita
        this.isModalOpen = true;
      }
    }

    // Actualizar la fecha de la última visita
    localStorage.setItem('lastVisit', new Date().toISOString());
  }
}

