import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { EnvService } from './env.service';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  constructor(
    private http: HttpClient,
    private envService: EnvService
  ) {}

  private getApiUrl(): string {
    if (!this.envService.apiUrl) {
      throw new Error('API URL no está configurada');
    }
    return this.envService.apiUrl;
  }

  getInfo() {
    return this.http.get(`${this.getApiUrl()}/info`);
  }

  getProductosByCategory(categoria: string): Observable<any> {
    const params = new HttpParams().set('categoria', categoria);
    return this.http.get(`${this.getApiUrl()}/productos/`, { params });
  }

  getProductosByDescription(description: string): Observable<any> {
    if (!description?.trim()) {
      return throwError(() => new Error('Debe ingresar un término de búsqueda'));
    }
    
    return this.http.get(`${this.getApiUrl()}/productos`, {
      params: new HttpParams().set('descripcion', description)
    });
  }
}