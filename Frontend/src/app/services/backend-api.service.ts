import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getInfo() {
    return this.http.get(`${this.apiUrl}/info`);
  }

  getProductosByCategory(categoria: string): Observable<any> {
    const params = new HttpParams().set('categoria', categoria);
    return this.http.get(`${this.apiUrl}/productos/`, { params });
  }

  getProductosByDescription(descripcion: string): Observable<any> {
    const params = new HttpParams().set('descripcion', descripcion);
    return this.http.get(`${this.apiUrl}/productos/`, { params });
  }
}
