import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import {GeneratorComponent} from "./main-page/generator/generator.component";
import {HistoryComponent} from "./history-page/history/history.component";


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, GeneratorComponent, HistoryComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'client';
}
