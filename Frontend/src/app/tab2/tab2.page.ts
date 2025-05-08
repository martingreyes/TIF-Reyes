import { Component, OnInit } from '@angular/core';
import { register } from 'swiper/element/bundle';
import { MycartService } from '../services/mycart.service';
import { Router } from '@angular/router';

register();

@Component({
  standalone: false,
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page implements OnInit {
  cartItems: any[] = [];
  isModalOpen = false;
  tiendaObjKey: string | undefined;
  supermarketGroups: { [supermercado: string]: any[] } = {};
  sortedSupermarkets: { 
    supermercado: string, 
    productos: any[], 
    total: number, 
    missingProducts: number,
    url: string  // <- Nueva propiedad para la URL base
  }[] = [];

  // Mapeo de supermercados a sus URLs base
  private supermarketUrls: { [key: string]: string } = {
    'Atomo': 'https://atomoconviene.com/atomo-ecommerce/',
    'Modo Market': 'https://www.modomarket.com',
    'Blowmax': 'https://blowmax.com.ar',
    'Casa Segal': 'https://www.casa-segal.com',
    'Supera': 'https://supera.com.ar'
  };

  ngOnInit() {
    this.cartItems = this.mycartService.getCartItems();
    this.mycartService.cartUpdated.subscribe((cartItems: any[]) => {
      this.cartItems = cartItems;
      this.groupBySupermarket();
    });
    console.log('Carrito:',this.cartItems)
    this.groupBySupermarket();
  }

  constructor(
    private mycartService: MycartService,
    private router: Router,
  ) {}

  groupBySupermarket(): void {
    const allSupermarkets = new Set<string>();
    this.cartItems.forEach(item => {
      Object.keys(item).forEach(key => {
        if (key !== 'quantity' && item[key]?.supermercado) {
          allSupermarkets.add(item[key].supermercado);
        }
      });
    });

    this.supermarketGroups = {};
    allSupermarkets.forEach(supermercado => {
      this.supermarketGroups[supermercado] = [];
    });

    this.cartItems.forEach(item => {
      const firstProductKey = Object.keys(item).find(key => key !== 'quantity');
      const productName = firstProductKey ? item[firstProductKey]?.nombre : 'Producto sin nombre';
      const productId = firstProductKey ? item[firstProductKey]?.p_id : 0;
      const quantity = item.quantity;

      allSupermarkets.forEach(supermercado => {
        let productInSupermarket: any = null;
        Object.keys(item).forEach(key => {
          if (key !== 'quantity' && item[key]?.supermercado === supermercado) {
            productInSupermarket = item[key];
          }
        });

        if (productInSupermarket) {
          this.supermarketGroups[supermercado].push({
            nombre: productInSupermarket.nombre,
            p_id: productInSupermarket.p_id,
            precio: productInSupermarket.precio,
            url: productInSupermarket.url, // URL específica del producto
            quantity: quantity
          });
        } else {
          this.supermarketGroups[supermercado].push({
            nombre: productName,
            p_id: productId,
            precio: null,
            url: null,
            quantity: quantity
          });
        }
      });
    });

    // Calcular total, productos faltantes y asignar URL base
    this.sortedSupermarkets = Object.keys(this.supermarketGroups).map(supermercado => {
      const productos = this.supermarketGroups[supermercado];
      let total = 0;
      let missingProducts = 0;

      productos.forEach((producto: any) => {
        if (producto.precio !== null) {
          total += parseFloat(producto.precio) * producto.quantity;
        } else {
          missingProducts++;
        }
      });

      return {
        supermercado,
        productos,
        total,
        missingProducts,
        url: this.supermarketUrls[supermercado] || '#' // Asignar URL base
      };
    });

    // Ordenar (misma lógica anterior)
    this.sortedSupermarkets.sort((a, b) => {
      if (a.missingProducts === 0 && b.missingProducts === 0) {
        return a.total - b.total;
      } else if (a.missingProducts === 0) {
        return -1;
      } else if (b.missingProducts === 0) {
        return 1;
      } else {
        return b.missingProducts - a.missingProducts || b.total - a.total;
      }
    });

    console.log('Supermercados ordenados con URLs:', this.sortedSupermarkets);
  }

  getIconColor(index: number): string {
    // Asigna el color en función del índice
    switch (index) {
      case 0: return '#D4AF37'; // Oro
      case 1: return '#C0C0C0'; // Plata
      case 2: return '#CD7F32'; // Bronce
      default: return ''; // Sin color
    }
  }

  getIconName(index: number): string {
    // Asigna el nombre del icono en función del índice
    switch (index) {
      case 0: return 'trophy-sharp'; // Oro
      case 1: return 'trophy-sharp'; // Plata
      case 2: return 'trophy-sharp'; // Bronce
      
      default: return ''; // Sin icono
    }
  }

  formatPrice(precio: string): string {
    // Verificamos si el precio termina en ".00"
    if (precio.endsWith('.00')) {
      return precio.slice(0, -3); // Eliminamos los últimos 3 caracteres (".00")
    }
    return precio; // Dejamos el precio tal cual si tiene otros decimales
  }
  

  setOpen(isOpen: boolean, key?: string) {
    this.isModalOpen = isOpen;
    this.tiendaObjKey = key;
  }

  home() {
    this.router.navigateByUrl("");
  }
}