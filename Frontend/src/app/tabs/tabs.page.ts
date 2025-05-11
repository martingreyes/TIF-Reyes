import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MycartService } from '../services/mycart.service';
import { AlertController } from '@ionic/angular';

@Component({
  standalone: false,
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})
export class TabsPage implements OnInit {
  isModalOpen = false;
  articulos : any
  cartItems: any[] = [];
  items: { nombre: string, cantidad: number }[] = [
    { nombre: 'Pokémon Yellow Pokémon Yellow', cantidad: 1 },
    { nombre: 'Pokémon Yellow', cantidad: 2 },
    { nombre: 'Pokémon Yellow Pokémon Yellow Pokémon Yellow', cantidad: 3 },
    { nombre: 'Pokémon Yellow', cantidad: 4 },
    { nombre: 'Pokémon Yellow Pokémon Yellow', cantidad: 1 },
    { nombre: 'Pokémon Yellow', cantidad: 2 },
    { nombre: 'Pokémon Yellow Pokémon Yellow Pokémon Yellow', cantidad: 3 },
    { nombre: 'Pokémon Yellow', cantidad: 4 },
    { nombre: 'Pokémon Yellow Pokémon Yellow', cantidad: 1 },
    { nombre: 'Pokémon Yellow', cantidad: 2 },
    { nombre: 'Pokémon Yellow Pokémon Yellow Pokémon Yellow', cantidad: 3 },
    { nombre: 'Pokémon Yellow', cantidad: 4 },
    { nombre: 'Pokémon Yellow Pokémon Yellow', cantidad: 1 },
    { nombre: 'Pokémon Yellow', cantidad: 2 },
    { nombre: 'Pokémon Yellow Pokémon Yellow Pokémon Yellow', cantidad: 3 },
    { nombre: 'Pokémon Yellow', cantidad: 4 },
    // Agrega más objetos según sea necesario
  ];

  constructor(
    private router: Router,
    private mycartService: MycartService,
    public alertController: AlertController

  ) {}

  ngOnInit() {
    this.cartItems = this.mycartService.getCartItems();
    this.mycartService.cartUpdated.subscribe((cartItems: any[]) => {
      this.cartItems = cartItems;
    });
  }

  setOpen(isOpen: boolean) {
    this.isModalOpen = isOpen;
  }

  incrementItem(productId: any) {
    this.mycartService.incrementQuantity(productId);
  }

  decrementItem(productId: any) {
    this.mycartService.decrementQuantity(productId);
  }

  emptyCart() {
    let cartStatus = confirm('¿Estás seguro que quieres vaciar el carrito ?');
    if (cartStatus) {
      this.mycartService.clearCart();
      document.location.href = '';
    }
  }

  getTotalQuantity(): number {
    return this.mycartService.getTotalQuantity();
  }

  mostrarAlerta() {
    // this.presentAlert('Carrito Vacío', 'Tu carrito está vacío. Agrega productos para continuar.');
    alert("Tu carrito está vacío. Agrega productos para continuar.")
  }

  goToTab2() {
    this.isModalOpen = false;
    this.router.navigate(['/tabs/tab2']);
  }

  async presentAlert(header: string, message: string) {
    const alert = await this.alertController.create({
      header: header,
      message: message,
      buttons: ['OK']
    });

    await alert.present();
  }

}
