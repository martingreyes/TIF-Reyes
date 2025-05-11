import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable, throwError } from 'rxjs';
import { EnvService } from './env.service';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient,
    private envService: EnvService
  ) {
    this.apiUrl = this.envService.apiUrl;
  }

  getInfo() {
    return this.http.get(`${this.apiUrl}/info`);
  }

  getProductosByCategory(categoria: string): Observable<any> {
    const params = new HttpParams().set('categoria', categoria);
    return this.http.get(`${this.apiUrl}/productos/`, { params });
  }

  getProductosByDescription(description: string): Observable<any> {
    // Verifica que la descripción no esté vacía
    if (!description || description.trim().length === 0) {
      return throwError(() => new Error('Debe ingresar un término de búsqueda'));
    }
    
    return this.http.get(`${this.apiUrl}/productos?descripcion=${encodeURIComponent(description)}`);
  }
}
