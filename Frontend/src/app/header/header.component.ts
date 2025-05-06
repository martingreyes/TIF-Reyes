import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  standalone: false,
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent  implements OnInit {

  constructor(
    private router: Router
  ) {}

  ngOnInit() {}

  home() {
    this.router.navigateByUrl("")
  }

  info() {
    this.router.navigateByUrl("/tabs/tab3")
  }



}