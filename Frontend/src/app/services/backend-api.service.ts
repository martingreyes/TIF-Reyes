import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import {AppConfigService} from './app-config.service'

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  constructor(
    private http: HttpClient,
    private configService: AppConfigService
  ) {}

  private getBackUrl(): string {
    return this.configService.getConfig().backendUrl;
  }

  getInfo() {
    return this.http.get(`${this.getBackUrl()}/api/info`);
  }

  getProductosByCategory(categoria: string): Observable<any> {
    const params = new HttpParams().set('categoria', categoria);
    return this.http.get(`${this.getBackUrl()}/api/productos`, { params });
  }

  getProductosByDescription(description: string): Observable<any> {
    if (!description?.trim()) {
      return throwError(() => new Error('Debe ingresar un término de búsqueda'));
    }
    
    return this.http.get(`${this.getBackUrl()}/productos`, {
      params: new HttpParams().set('api/descripcion', description)
    });
  }
}