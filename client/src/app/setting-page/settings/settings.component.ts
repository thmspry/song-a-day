import {Component, OnInit} from '@angular/core';
import {Observable, tap} from "rxjs";
import {ajax} from "rxjs/ajax";
import {EnvironmentVariable} from "../../model/EnvironmentVariable";
import {EnvironmentVariableComponent} from "../environment-variable/environment-variable.component";

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [
    EnvironmentVariableComponent
  ],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.scss'
})
export class SettingsComponent implements OnInit {
  protected environmentVariables: EnvironmentVariable[] | undefined;

  ngOnInit(): void {
    this.getEnvironmentVariables$().subscribe();
  }
  private getEnvironmentVariables$(): Observable<EnvironmentVariable[]> {
    return ajax.getJSON<EnvironmentVariable[]>('http://127.0.0.1:8000/api/env').pipe(tap((variables: EnvironmentVariable[]) => {
      this.environmentVariables = variables;
    }));
  }
}
