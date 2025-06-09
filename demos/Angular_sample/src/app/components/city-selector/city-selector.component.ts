import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-city-selector',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './city-selector.component.html',
  styleUrls: ['./city-selector.component.scss']
})
export class CitySelectorComponent {
  @Output() citySelected = new EventEmitter<string>();
  selectedCity = "Hsinchu Yes";
  cities: string[] = [
    'Taipei',
    'Kaohsiung',
    'Taichung',
    'Tainan',
    'Hsinchu',
    'Chiayi',
    'Keelung',
    'Taoyuan',
    'Miaoli',
    'Changhua',
    'Nantou',
    'Yunlin',
    'Pingtung',
    'Taitung',
    'Hualien',
    'Yilan',
    'Penghu',
    'Kinmen',
    'Lienchiang'
  ];

  selectCity(city: string): void {
    this.citySelected.emit(city);
  }
  
  onCityChange(city: string) {
    this.selectedCity = city;
  }
}