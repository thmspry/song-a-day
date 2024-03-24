import { Routes } from '@angular/router';
import {GeneratorComponent} from "./main-page/generator/generator.component";
import {HistoryComponent} from "./history-page/history/history.component";
import {SettingsComponent} from "./setting-page/settings/settings.component";

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
  },
  {
    path: 'settings',
    component: SettingsComponent,
    title: 'Settings'
  }
];
