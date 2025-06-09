import { Component } from '@angular/core';
import { HelloComponent } from './hello.component';
import { WeatherDisplayComponent } from './components/weather-display/weather-display.component';
import { Weather } from './interfaces/weather.interface';
import { CitySelectorComponent } from './components/city-selector/city-selector.component';



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HelloComponent,WeatherDisplayComponent,CitySelectorComponent],
  templateUrl: './app.component.html'
})
export class AppComponent {
  name = 'Angular';


  weatherData: Weather = {
  temperature: 50,
  humidity: 50,
  windSpeed: 50,
  description: "Test Data",
  city: "Taipei",
  country: "Taipei",
  timestamp: new Date("2025-06-05"),
  condition: "Condition Test"
  };
}