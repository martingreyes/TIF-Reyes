import { Component, OnInit} from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BackendApiService } from '../services/backend-api.service'; 

@Component({
  standalone: false,
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page {
  lastUpdate: any
  supermarkets: any

  constructor(
    private router: Router,
    private backendApi: BackendApiService, // Inyecta el servicio
    private route: ActivatedRoute
  ) {
    this.route.queryParams.subscribe(() => {
      this.loadLastInfo(); // Cambia a la nueva función
    });
  }

  ngOnInit() {
  }

  home() {
    this.router.navigateByUrl("")
  }

  loadLastInfo() {
    this.backendApi.getInfo().subscribe({
      next: (response: any) => {
        this.lastUpdate = response.lastUpdate;
        this.supermarkets = response.supermercados
      },
      error: (error) => {
        console.error('Error fetching last update:', error);
      }
    });
  }

}
