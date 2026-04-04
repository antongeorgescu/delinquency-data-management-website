import { Component } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  isGenerating = false;
  isRunningRiskAnalysis = false;
  isRunningEDA = false;
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

  runRiskAnalysis(): void {
    this.isRunningRiskAnalysis = true;
    this.error = null;

    this.dataService.runRiskAnalysis().subscribe({
      next: (response) => {
        this.isRunningRiskAnalysis = false;
        console.log('Risk analysis completed:', response);
        // You might want to show a success message or update UI based on response
      },
      error: (error) => {
        this.isRunningRiskAnalysis = false;
        this.error = 'Failed to run risk analysis. Please ensure data is generated first.';
        console.error('Error running risk analysis:', error);
      }
    });
  }

  runEDA(): void {
    this.isRunningEDA = true;
    this.error = null;

    this.dataService.runEDA().subscribe({
      next: (response) => {
        this.isRunningEDA = false;
        console.log('EDA completed:', response);
        // You might want to show a success message or update UI based on response
      },
      error: (error) => {
        this.isRunningEDA = false;
        this.error = 'Failed to run EDA. Please ensure data is generated first.';
        console.error('Error running EDA:', error);
      }
    });
  }
}