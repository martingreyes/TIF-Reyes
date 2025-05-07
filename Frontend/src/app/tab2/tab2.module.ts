import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Tab2Page } from './tab2.page';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';
import { HeaderComponentModule } from '../header/header.module';

import { Tab2PageRoutingModule } from './tab2-routing.module';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    Tab2PageRoutingModule,
    HeaderComponentModule
  ],
  declarations: [Tab2Page],
  schemas:[CUSTOM_ELEMENTS_SCHEMA]
})
export class Tab2PageModule {}
