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
  
  // Algorithm selection properties
  selectedAlgorithm: string = 'percentile';
  algorithms = [
    {
      id: 'percentile',
      name: 'Percentile Based',
      short_name: 'Percentile',
      description: 'Bottom 60% = Low(0), Next 30% = Medium(1), Top 10% = High(2)'
    },
    {
      id: 'threshold', 
      name: 'Fixed Threshold',
      short_name: 'Threshold',
      description: 'Fixed probability thresholds: <0.3=Low, 0.3-0.6=Medium, >0.6=High'
    },
    {
      id: 'kmeans',
      name: 'K-Means Clustering', 
      short_name: 'K-Means',
      description: 'K-means clustering of probabilities into 3 risk groups'
    },
    {
      id: 'svm',
      name: 'Support Vector Machine',
      short_name: 'SVM', 
      description: 'Support Vector Machine classifier trained on probability-based risk labels'
    },
    {
      id: 'knn',
      name: 'K-Nearest Neighbors',
      short_name: 'KNN',
      description: 'K-Nearest Neighbors classifier with optimal k and distance weighting'
    }
  ];

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

  selectAlgorithm(algorithmId: string): void {
    this.selectedAlgorithm = algorithmId;
  }

  runRiskAnalysis(): void {
    this.isRunningRiskAnalysis = true;
    this.error = null;

    this.dataService.runRiskAnalysis(this.selectedAlgorithm).subscribe({
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