import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  standalone: false,
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {

  arrayArticulos: any;

  constructor(
    private router: Router,
  ) {}

  async ver(categoria: string) {

    console.log(this.arrayArticulos)
    this.router.navigate(['/tabs/tab4'], { queryParams: { categoria: categoria } });
  }


}

