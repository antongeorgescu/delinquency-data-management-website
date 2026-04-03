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

  // Parameter selection properties
  selectedNumPayers: string = '1000';
  selectedStartDate: string = '2020-01-01';
  selectedEndDate: string = '2023-12-31';

  constructor(private dataService: DataService) {}

  generateData(): void {
    this.isGenerating = true;
    this.generationComplete = false;
    this.error = null;

    // Create parameters object from selected values
    const parameters = {
      num_payers: parseInt(this.selectedNumPayers, 10),
      start_date: this.selectedStartDate,
      end_date: this.selectedEndDate
    };

    this.dataService.generateData(parameters).subscribe({
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