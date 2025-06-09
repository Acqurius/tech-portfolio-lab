import { Component, Input } from '@angular/core';
import { CitySelectorComponent } from './components/city-selector/city-selector.component';

@Component({
  selector: 'app-hello',
  standalone: true,
   imports: [CitySelectorComponent],
  //template: `<p>Hello, {{ user }}! This is a simple Angular component.</p>`
  templateUrl: './hello.component.html'
})
export class HelloComponent {
  @Input() user = '';
  msg="by AI";
}