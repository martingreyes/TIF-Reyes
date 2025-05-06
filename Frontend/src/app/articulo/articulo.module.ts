import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ArticuloComponent } from './articulo.component';

@NgModule({
  imports: [ CommonModule, FormsModule, IonicModule],
  declarations: [ArticuloComponent],
  exports: [ArticuloComponent]
})
export class ArticuloComponentModule {}