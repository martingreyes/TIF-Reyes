import { Component, OnInit, Input } from '@angular/core';

@Component({
  standalone: false,
  selector: 'app-articulo',
  templateUrl: './articulo.component.html',
  styleUrls: ['./articulo.component.scss'],
})
export class ArticuloComponent implements OnInit {
  @Input() item: any;
  @Input() categoria: any;
  @Input() cantidad: any;

  constructor() { }

  ngOnInit(): void {
  }

  increment() {
    this.cantidad++;
  }

  decrement() {
    if (this.cantidad > 0) {
      this.cantidad--;
    }
  }

  remove() {
    
  }
}