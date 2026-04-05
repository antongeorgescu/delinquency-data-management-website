import { Component, OnInit, AfterViewInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { RiskModel } from '../../interfaces/data.interface';

declare var bootstrap: any;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {
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
  
  // EDA parameters
  selectedNClusters: string = '5';
  selectedNComponents: string = '10';
  
  // Risk estimation results
  riskEstimationResults: any = null;
  showRiskResults = false;
  showCampaignDialog = false;
  
  // EDA results
  edaResults: any = null;
  showEdaResults = false;
  
  // Campaign generation results
  campaignResults: any = null;
  showCampaignResults = false;
  downloadLinks: any[] = [];
  
  // Data generation explanation
  showDataGenerationExplanation = false;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadRiskModels();
    this.loadPersistedPanels();
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
            description: 'Bottom 60% = Low(0), Next 30% = Medium(1), Top 10% = High(2)',
            type: 'Statistical Distribution'
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

  // Load persisted panel states from localStorage
  loadPersistedPanels(): void {
    try {
      const savedRiskResults = localStorage.getItem('riskEstimationResults');
      const savedEdaResults = localStorage.getItem('edaResults');
      const savedCampaignResults = localStorage.getItem('campaignResults');
      
      if (savedRiskResults) {
        this.riskEstimationResults = JSON.parse(savedRiskResults);
        this.showRiskResults = true;
      }
      
      if (savedEdaResults) {
        this.edaResults = JSON.parse(savedEdaResults);
        this.showEdaResults = true;
      }
      
      if (savedCampaignResults) {
        this.campaignResults = JSON.parse(savedCampaignResults);
        this.showCampaignResults = true;
        if (this.campaignResults.files_generated) {
          this.downloadLinks = this.campaignResults.files_generated;
        }
      }
      
      // Refresh tooltips for persisted performance metrics
      if (this.riskEstimationResults) {
        setTimeout(() => this.refreshTooltips(), 300);
      }
    } catch (error) {
      console.warn('Error loading persisted panels:', error);
    }
  }

  // Save panel state to localStorage
  saveRiskResults(): void {
    if (this.riskEstimationResults) {
      localStorage.setItem('riskEstimationResults', JSON.stringify(this.riskEstimationResults));
    }
  }

  saveCampaignResults(): void {
    if (this.campaignResults) {
      localStorage.setItem('campaignResults', JSON.stringify(this.campaignResults));
    }
  }

  saveEdaResults(): void {
    if (this.edaResults) {
      localStorage.setItem('edaResults', JSON.stringify(this.edaResults));
    }
  }
  
  // Close panel methods
  closeGenerationSuccess(): void {
    this.generationComplete = false;
    this.generationStats = null;
  }

  closeRiskResults(): void {
    this.showRiskResults = false;
    localStorage.removeItem('riskEstimationResults');
    this.riskEstimationResults = null;
  }

  closeEdaResults(): void {
    this.showEdaResults = false;
    localStorage.removeItem('edaResults');
    this.edaResults = null;
  }

  closeCampaignResults(): void {
    this.showCampaignResults = false;
    localStorage.removeItem('campaignResults');
    this.campaignResults = null;
    this.downloadLinks = [];
  }

  toggleDataGenerationExplanation(): void {
    this.showDataGenerationExplanation = !this.showDataGenerationExplanation;
  }

  runRiskAnalysis(): void {
    if (!this.selectedAlgorithm) {
      this.error = 'Please select an algorithm first.';
      return;
    }
    
    this.isRunningRiskAnalysis = true;
    this.error = null;
    
    // Clear both panels when starting new risk analysis
    this.riskEstimationResults = null;
    this.showRiskResults = false;
    this.campaignResults = null;
    this.showCampaignResults = false;
    this.downloadLinks = [];
    localStorage.removeItem('riskEstimationResults');
    localStorage.removeItem('campaignResults');

    this.dataService.runRiskEstimation(this.selectedAlgorithm).subscribe({
      next: (response) => {
        this.isRunningRiskAnalysis = false;
        this.riskEstimationResults = response;
        this.showRiskResults = true;
        this.saveRiskResults();
        
        // Refresh tooltips for the performance metrics
        setTimeout(() => this.refreshTooltips(), 200);
        
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
        this.showCampaignResults = true;
        this.saveCampaignResults();
        
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

    // Parse the selected parameters
    const nClusters = parseInt(this.selectedNClusters, 10);
    const nComponents = parseInt(this.selectedNComponents, 10);

    this.dataService.runEDAReports(nClusters, nComponents).subscribe({
      next: (response) => {
        this.isRunningEDA = false;
        this.edaResults = response;
        this.showEdaResults = true;
        this.saveEdaResults();
        console.log('EDA completed:', response);
      },
      error: (error) => {
        this.isRunningEDA = false;
        this.error = 'Failed to run EDA. Please ensure data is generated first.';
        console.error('Error running EDA:', error);
      }
    });
  }

  // Helper method to convert object to array of key-value pairs for template display
  getParameterEntries(parameters: any): {key: string, value: any}[] {
    if (!parameters) return [];
    return Object.entries(parameters).map(([key, value]) => ({key, value}));
  }

  ngAfterViewInit(): void {
    // Initialize Bootstrap tooltips after view is rendered
    this.initializeTooltips();
  }

  // Initialize Bootstrap tooltips
  initializeTooltips(): void {
    // Small delay to ensure DOM is fully rendered
    setTimeout(() => {
      try {
        const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(tooltipTriggerEl => {
          new bootstrap.Tooltip(tooltipTriggerEl);
        });
      } catch (error) {
        console.warn('Bootstrap tooltips could not be initialized:', error);
      }
    }, 100);
  }

  // Re-initialize tooltips when risk results are updated (called after API responses)
  refreshTooltips(): void {
    // Dispose existing tooltips first
    try {
      const existingTooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
      existingTooltips.forEach(el => {
        const tooltip = bootstrap.Tooltip.getInstance(el);
        if (tooltip) {
          tooltip.dispose();
        }
      });
    } catch (error) {
      console.warn('Error disposing tooltips:', error);
    }
    
    // Re-initialize tooltips
    this.initializeTooltips();
  }
}