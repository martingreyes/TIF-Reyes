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
    // Configuramos el debounce para las búsquedas
    this.searchSubject.pipe(
      debounceTime(500), // Espera 500ms después de la última tecla
      distinctUntilChanged() // Solo ejecuta si el valor cambió
    ).subscribe(searchTerm => {
      this.searchProducts();
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
    this.searchSubject.next(event.target.value);
  }

  loadProductos(description: string) {
    this.loading = true; // Activa spinner
    
    this.backendApi.getProductosByDescription(description).subscribe({
      next: (response: any) => {
        this.articulos = response.data;
        this.loading = false; // Desactiva spinner
      },
      error: (error) => {
        console.error('Error al cargar productos:', error);
        this.loading = false; // Desactiva spinner incluso en error
        this.articulos = []; // Vacía los resultados
        
        if (error.error?.error === "Debe proporcionar al menos un parámetro") {
          alert("Por favor ingrese un término de búsqueda válido");
        } else {
          alert("Error al buscar productos. Intente nuevamente.");
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
