import { Injectable, EventEmitter } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { identifierName } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class MycartService {
  cartUpdated: EventEmitter<any[]> = new EventEmitter<any[]>();

  // addToCart(product: any) {
  //   let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
  //   cartItems.push(product);
  //   localStorage.setItem('cartItems', JSON.stringify(cartItems));
  //   this.cartUpdated.emit(cartItems);
  // }

  addToCart(product: any) {
    let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    const existingProduct = cartItems.find((item: any) => item[0].p_id === product[0].p_id);
    if (existingProduct) {
      existingProduct.quantity++;
    } else {
      cartItems.push({ ...product, quantity: 1 }); // Añadir el producto con cantidad 1
    }
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    this.cartUpdated.emit(cartItems); // Emitir evento de actualización del carrito
  }

  removeFromCart(productId: any) {
    let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    const index = cartItems.findIndex((item: any) => item[0].p_id === productId);
    if (index !== -1) {
      cartItems.splice(index, 1);
      localStorage.setItem('cartItems', JSON.stringify(cartItems));
      this.cartUpdated.emit(cartItems);
    }
  }

  incrementQuantity(productId: any) {
    let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    const product = cartItems.find((item: any) => item[0].p_id === productId);
    if (product) {
      product.quantity++;
      localStorage.setItem('cartItems', JSON.stringify(cartItems));
      this.cartUpdated.emit(cartItems);
    }
  }

  decrementQuantity(productId: any) {
    let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    const product = cartItems.find((item: any) => item[0].p_id === productId);
    if (product) {
      product.quantity--;
      if (product.quantity < 1) {
        this.removeFromCart(productId);
      } else {
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
        this.cartUpdated.emit(cartItems);
      }
    }
  }

  getTotalQuantity(): number {
    let totalQuantity = 0;
    const cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    cartItems.forEach((item: { quantity: number; }) => {
      totalQuantity += item.quantity;
    });
    return totalQuantity;
  }

  getCartItems() {
    return JSON.parse(localStorage.getItem('cartItems') || '[]');
  }

  clearCart() {
    localStorage.removeItem('cartItems');
    this.cartUpdated.emit([]);
  }


}

