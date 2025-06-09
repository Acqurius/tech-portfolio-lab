import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Weather } from '../../interfaces/weather.interface';

@Component({
  selector: 'app-weather-display',
  imports: [CommonModule],
  templateUrl: './weather-display.component.html',
  styleUrls: ['./weather-display.component.scss']
})
export class WeatherDisplayComponent {
  @Input() weatherData: Weather | null = null;

// weatherData: Weather = {
//   temperature: 50,
//   humidity: 50,
//   windSpeed: 50,
//   description: "test",
//   city: "hEllo",
//   country: "cotu",
//   timestamp: new Date("2025-06-05")
//   };

  constructor() {}

  // Method to format temperature
  getTemperature(): string {
    return this.weatherData ? `${this.weatherData.temperature} °C` : 'N/A';
  }

  // Method to format weather description
  getDescription(): string {
    return this.weatherData ? this.weatherData.description : 'No data available';
  }
  ngOnChanges() { console.log('weatherData:', this.weatherData); }
}