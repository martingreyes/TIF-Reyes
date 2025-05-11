import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MycartService } from '../services/mycart.service';
import { BackendApiService } from '../services/backend-api.service';
import { debounceTime, distinctUntilChanged, Subject } from 'rxjs';

@Component({
  standalone: false,
  selector: 'app-tab5',
  templateUrl: 'tab5.page.html',
  styleUrls: ['tab5.page.scss']
})
export class Tab5Page implements OnInit {
  loading: boolean = false
  items: any[] = new Array(8);
  articulos: any;
  categoria: any;
  item: any;
  articulosYcantidad: any;
  showToast = false;
  searchTerm: string = '';
  private searchSubject = new Subject<string>();

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient,
    private mycartService: MycartService,
    private backendApi: BackendApiService
  ) {
    this.route.queryParams.subscribe(async params => {
      this.categoria = params['categoria'];
      this.articulos = await this.loadProductos(this.categoria);
    });
  }

  ngOnInit() {
    this.searchSubject.pipe(
      debounceTime(500),
      distinctUntilChanged()
    ).subscribe(term => {
      if (term && term.trim().length > 0) {
        this.loadProductos(term.trim());
      } else {
        this.loadProductos(this.categoria || '');
      }
    });
  }
  

  searchProducts() {
    if (this.searchTerm && this.searchTerm.trim().length > 0) {
      this.loadProductos(this.searchTerm.trim());
    } else {
      // Si el buscador está vacío, carga la categoría por defecto
      this.loadProductos(this.categoria || '');
    }
  }

  onSearchInput(event: any) {
    const value = event.target.value;
    this.searchSubject.next(value);
  }
  

  loadProductos(searchParam: string) {
    // Evita peticiones vacías
    if (!searchParam) {
      this.articulos = [];
      return;
    }

    this.loading = true;
    
    this.backendApi.getProductosByDescription(searchParam).subscribe({
      next: (response: any) => {
        this.articulos = response.data || [];
        this.loading = false;
      },
      error: (error) => {
        console.error('Error:', error);
        this.loading = false;
        this.articulos = [];
        
        if (this.searchTerm.trim().length > 0) {
          if (error.status === 423) {
            alert("Estamos actualizando los precios. Intente realizar la búsqueda de nuevo en minutos. Muchas gracias :)");
          } else {
            alert(error.error?.message || "Error al buscar productos");
          }
        }
      }
    });
    



  }

  @Output() refresh: EventEmitter<boolean> = new EventEmitter();

  addToCart(product: any) {
    this.mycartService.addToCart(product);
    this.refresh.emit(true);
    this.showToastMessage()
  }

  showToastMessage() {
    this.showToast = true;
    setTimeout(() => {
      this.showToast = false;
    }, 3000);
  }


  home() {
    this.router.navigateByUrl("")
  }

}
