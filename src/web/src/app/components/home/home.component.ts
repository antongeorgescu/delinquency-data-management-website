import { Component } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  isGenerating = false;
  generationComplete = false;
  generationStats: any = null;
  error: string | null = null;

  constructor(private dataService: DataService) {}

  generateData(): void {
    this.isGenerating = true;
    this.generationComplete = false;
    this.error = null;

    this.dataService.generateData().subscribe({
      next: (response) => {
        this.isGenerating = false;
        this.generationComplete = true;
        this.generationStats = response.statistics;
      },
      error: (error) => {
        this.isGenerating = false;
        this.error = 'Failed to generate data. Please try again.';
        console.error('Error generating data:', error);
      }
    });
  }
}