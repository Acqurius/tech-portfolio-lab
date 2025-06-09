export interface Weather {
  temperature: number;
  humidity: number;
  windSpeed: number;
  description: string;
  city: string;
  country: string;
  timestamp: Date;
  condition: string;
}