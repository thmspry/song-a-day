import {Component, Input} from '@angular/core';
import {EnvironmentVariable} from "../../model/EnvironmentVariable";

@Component({
  selector: 'app-environment-variable',
  standalone: true,
  imports: [],
  templateUrl: './environment-variable.component.html',
  styleUrl: './environment-variable.component.scss'
})
export class EnvironmentVariableComponent {
  @Input() variable!: EnvironmentVariable;
}
