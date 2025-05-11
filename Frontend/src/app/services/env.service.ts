// src/app/services/env.service.ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EnvService {
  public apiUrl = (window as any)['env']['apiUrl'] || 'http://localhost:5001';
}
