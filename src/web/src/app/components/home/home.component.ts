import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { RiskModel } from '../../interfaces/data.interface';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  isGenerating = false;
  isRunningRiskAnalysis = false;
  isRunningEDA = false;
  isLoadingAlgorithms = false;
  isGeneratingCampaignFiles = false;
  generationComplete = false;
  generationStats: any = null;
  error: string | null = null;

  // Parameter selection properties
  selectedNumPayers: string = '1000';
  selectedStartDate: string = '2020-01-01';
  selectedEndDate: string = '2023-12-31';
  
  // Algorithm selection properties
  selectedAlgorithm: string = 'percentile';
  algorithms: RiskModel[] = [];
  
  // Risk estimation results
  riskEstimationResults: any = null;
  showCampaignDialog = false;
  
  // Campaign generation results
  campaignResults: any = null;
  downloadLinks: any[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadRiskModels();
  }

  loadRiskModels(): void {
    this.isLoadingAlgorithms = true;
    
    this.dataService.getRiskModels().subscribe({
      next: (response) => {
        this.algorithms = response.models;
        this.isLoadingAlgorithms = false;
        // Set default selection if algorithms are loaded and no selection exists
        if (this.algorithms.length > 0 && !this.selectedAlgorithm) {
          this.selectedAlgorithm = this.algorithms[0].id;
        }
      },
      error: (error) => {
        this.isLoadingAlgorithms = false;
        console.error('Error loading risk models:', error);
        // Fallback to default algorithms if API fails
        this.algorithms = [
          {
            id: 'percentile',
            name: 'Percentile Based',
            short_name: 'Percentile',
            description: 'Bottom 60% = Low(0), Next 30% = Medium(1), Top 10% = High(2)'
          }
        ];
      }
    });
  }

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
    if (!this.selectedAlgorithm) {
      this.error = 'Please select an algorithm first.';
      return;
    }
    
    this.isRunningRiskAnalysis = true;
    this.error = null;
    this.riskEstimationResults = null;

    this.dataService.runRiskEstimation(this.selectedAlgorithm).subscribe({
      next: (response) => {
        this.isRunningRiskAnalysis = false;
        this.riskEstimationResults = response;
        
        if (response.success) {
          // Show dialog asking about campaign files generation
          this.showCampaignDialog = true;
        }
      },
      error: (error) => {
        this.isRunningRiskAnalysis = false;
        this.error = 'Failed to run risk estimation. Please ensure data is generated first.';
        console.error('Error running risk estimation:', error);
      }
    });
  }

  // Handle campaign generation dialog
  generateCampaignFiles(): void {
    this.isGeneratingCampaignFiles = true;
    this.showCampaignDialog = false;
    
    this.dataService.generateCampaignFiles().subscribe({
      next: (response) => {
        this.isGeneratingCampaignFiles = false;
        this.campaignResults = response;
        
        if (response.success && response.files_generated) {
          this.downloadLinks = response.files_generated;
        }
      },
      error: (error) => {
        this.isGeneratingCampaignFiles = false;
        this.error = 'Failed to generate campaign files.';
        console.error('Error generating campaign files:', error);
      }
    });
  }

  // Decline campaign generation
  declineCampaignGeneration(): void {
    this.showCampaignDialog = false;
  }

  // Download campaign file
  downloadFile(url: string, filename: string): void {
    try {
      const link = document.createElement('a');
      link.href = `http://localhost:5000${url}`;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading file:', error);
      this.error = 'Failed to download file. Please try again.';
    }
  }

  // Clear error messages
  clearError(): void {
    this.error = null;
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