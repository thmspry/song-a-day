import { Routes } from '@angular/router';
import {GeneratorComponent} from "./generator/generator.component";
import {HistoryComponent} from "./history/history.component";

export const routes: Routes = [
  {
    path: '',
    component: GeneratorComponent,
    title: 'Generator'
  },
  {
    path: 'history',
    component: HistoryComponent,
    title: 'History'
  }
];
