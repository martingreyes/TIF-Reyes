import { Component,Input,OnInit,Output, EventEmitter } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { MycartService } from '../services/mycart.service';
import { BackendApiService } from '../services/backend-api.service';


@Component({
  standalone: false,
  selector: 'app-tab4',
  templateUrl: 'tab4.page.html',
  styleUrls: ['tab4.page.scss']
})
export class Tab4Page implements OnInit{
  items: any[] = new Array(8);
  articulos: any
  categoria: any;
  item: any
  articulosYcantidad: any
  
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

  }


  loadProductos(categoria: string) {
    this.backendApi.getProductosByCategory(categoria).subscribe({
      next: (response: any) => {
        this.articulos = response.data; // Extrae solo el array de data
        console.log('Cantidad de productos de la categoria ', this.categoria, ' : ', response.cantidad_productos)
        console.log('Productos cargados:', this.articulos);
      },
      error: (error) => {
        console.error('Error al cargar productos:', error);
        alert("Estamos actualizando los precios. Intente acceder a " + categoria + " en minutos. Muchas gracias :)");
        this.router.navigateByUrl("");
      }
    });
  }

  @Output() refresh: EventEmitter<boolean> = new EventEmitter();

  addToCart(product: any) {
    this.mycartService.addToCart(product);
    this.refresh.emit(true);
  }


  home() {
    this.router.navigateByUrl("")
  }

}
