// env.service.ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EnvService {
  public apiUrl = '';

  constructor() {
    this.loadEnvironment();
  }

  private loadEnvironment() {
    const env = (window as any).env;
    this.apiUrl = env?.apiUrl || '';
  }
}