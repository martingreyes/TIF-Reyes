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

export class Tab2Page implements OnInit{
  cartItems: any[] = [];
  cantidades: any[] = []
  totales: any[] = []
  nulos: any[] = []
  isModalOpen = false;
  tiendaObjKey: string | undefined;
  data: any[] = []
  supers: any[] = ["Atomo","Blowmax","ModoMarket","Segal","Supera"]
  facturas2: any[] = [{"Atomo":[]},{"Blowmax":[]},{"ModoMarket":[]},{"Segal":[]},{"Supera":[]},]

  ngOnInit() {
    this.cartItems = this.mycartService.getCartItems();
    this.mycartService.cartUpdated.subscribe((cartItems: any[]) => {
      this.cartItems = cartItems;
    });    
    this.getFacturas()
    this.calcularTotal()
    this.ordenarFacturas()
  }

  
  getFacturas() {

    for (let x = 0; x < this.cartItems.length; x++) {
      let quantity =  this.cartItems[x].quantity
      this.cantidades.push(quantity)

      for (let i = 0; i < Object.keys(this.cartItems[x]).length - 1; i++) {  
        switch (this.cartItems[x][i].tienda) {
          case 'Atomo':
            this.facturas2[0].Atomo.push(this.cartItems[x][i])
            break;
          case 'Blowmax':
            this.facturas2[1].Blowmax.push(this.cartItems[x][i])
            break;
          case 'ModoMarket':
            this.facturas2[2].ModoMarket.push(this.cartItems[x][i])
            break;
          case 'Segal':
            this.facturas2[3].Segal.push(this.cartItems[x][i])
            break;
          case 'Supera':
            this.facturas2[4].Supera.push(this.cartItems[x][i])
            break;
        }
      }
    }

    let p_ids: any[] = [];
    let nombre_productos: any[] = [];

    for (let x = 0; x < this.facturas2.length; x++) {

      const tienda = this.facturas2[x];

      Object.keys(tienda).forEach((nombreTienda) => {
    
        const productos = tienda[nombreTienda];
    
        productos.forEach((producto: any) => {

          if (!p_ids.includes(producto.p_id)) {
              p_ids.push(producto.p_id);
              nombre_productos.push(producto.producto);
            }

        });
      });
    }


    for (let x = 0; x < this.facturas2.length; x++) {

      const tienda = this.facturas2[x];
    
      Object.keys(tienda).forEach((nombreTienda) => {
      

            const productos = tienda[nombreTienda];
            let p_ids_supermercado: any[] = [];
            productos.forEach((producto: any) => {
    
            p_ids_supermercado.push(producto.p_id)
            });

            let faltantes = p_ids.filter(p_id => !p_ids_supermercado.includes(p_id));
  
            for (let i = 0; i < faltantes.length; i++) {
              let posicion = p_ids.indexOf(faltantes[i])
          
              let nombre_product = nombre_productos[posicion]
              let product = {
                marca: null,
                p_id: faltantes[i],
                precio: null,
                producto: nombre_product,
                tienda: nombreTienda,
                url: null,
                volumen: null
            }
              productos.splice(posicion,0,product)
            }
        });

      }  
  }


  calcularTotal() {

    for (let x = 0; x < this.facturas2.length; x++) {

      const tienda = this.facturas2[x];
    
      Object.keys(tienda).forEach((nombreTienda) => {
            const productos = tienda[nombreTienda];
            let suma = 0
            let nulo = 0
            let indice_producto = 0
            productos.forEach((producto: any) => {
              console.log(producto.tienda)
              if (producto.precio === null) {
                console.log("precio",producto.precio,"es null")
                nulo = nulo + 1
              }
              suma = suma + producto.precio*this.cantidades[indice_producto]
              indice_producto = indice_producto + 1
            });
            this.totales.push(suma)
            this.nulos.push(nulo)
        });
      }  
  }


  ordenarFacturas() {
    for (let x = 0; x < this.supers.length; x++) {
      this.data.push([this.supers[x],this.nulos[x],this.totales[x]])
    }

   this.data.sort((a, b) => {
      // Ordenar por el segundo elemento ascendente
      if (a[1] !== b[1]) {
          return a[1] - b[1];
      } else {
          // Si los segundos elementos son iguales, ordenar por el tercer elemento ascendente
          return a[2] - b[2];
      }
  });

    console.log(this.data)
    let orden: any = {};
    for (let x = 0; x < this.data.length; x++) {
      orden[this.data[x][0]] = x
    }
    console.log(orden)

    this.facturas2.sort((a, b) => {
      const keyA = Object.keys(a)[0];
      const keyB = Object.keys(b)[0];
      return orden[keyA] - orden[keyB];
  });

    console.log(this.facturas2)

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



  constructor(
    private mycartService: MycartService,
    private router: Router,
  ) {}

  getKey(obj: any): string {
    return Object.keys(obj)[0];
  }
  
  getTiendaUrl(tiendaObj: any): string {
    const tienda = this.getKey(tiendaObj); // Obtener el nombre de la tienda

    // Asignar la URL correspondiente según el nombre de la tienda
    switch (tienda) {
        case 'Atomo':
            return 'https://atomoconviene.com/atomo-ecommerce/';
        case 'ModoMarket':
            return 'https://www.modomarket.com';
        case 'Blowmax':
            return 'https://blowmax.com.ar';
        case 'Segal':
            return 'https://www.casa-segal.com';
        case 'Supera':
            return 'https://supera.com.ar';
        default:
            return '#'; // En caso de que no haya una URL definida para la tienda
    }
}

obtenerUltimaPalabra(cadena: string): string {
  const palabras = cadena.split(' ');
  return palabras[0];
}

setOpen(isOpen: boolean, key?: string) {
  this.isModalOpen = isOpen;
  this.tiendaObjKey = key;

}

home() {
  this.router.navigateByUrl("")
}

  
}
