import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EnvService {
  public apiUrl: string;

  constructor() {
    const host = window.__env.BACKEND_HOST;
    const port = window.__env.BACKEND_PORT;

    if (!host || !port) {
      console.error('BACKEND_HOST o BACKEND_PORT no están definidos en window.process.env');
      this.apiUrl = ''; // Evita crash por null
    } else {
      this.apiUrl = `http://${host}:${port}`;  
    }
  }
}
