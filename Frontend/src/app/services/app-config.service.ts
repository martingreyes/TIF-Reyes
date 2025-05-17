import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

//AppConfig.d.ts
export interface AppConfig {
    backendUrl: string;
}

//AppConfigService.ts
@Injectable({
  providedIn: 'root'
})
export class AppConfigService {
    private config: AppConfig | undefined; 
    loaded = false;
    constructor(private http: HttpClient) {}
    loadConfig(): Promise<void> {
        return this.http
            .get<AppConfig>('/assets/app.config.json')
            .toPromise()
            .then(data => {
                this.config = data;
                this.loaded = true;
            });
    }
    
    getConfig(): AppConfig {
        if (!this.config) {
          throw new Error('Pepe')
        }
        return this.config;
    }
}