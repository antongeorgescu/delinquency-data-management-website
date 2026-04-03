import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { DatabaseSummary } from '../../interfaces/data.interface';

@Component({
  selector: 'app-data-summary',
  templateUrl: './data-summary.component.html',
  styleUrls: ['./data-summary.component.css']
})
export class DataSummaryComponent implements OnInit {
  isLoading = false;
  dataSummary: DatabaseSummary | null = null;
  error: string | null = null;
  
  // Make Object.keys available in template
  Object = Object;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    console.log('DataSummaryComponent: ngOnInit called');
    this.loadDataSummary();
  }

  loadDataSummary(): void {
    console.log('DataSummaryComponent: loadDataSummary called');
    this.isLoading = true;
    this.error = null;
    this.dataSummary = null; // Reset previous data

    this.dataService.getDataBaseSummary().subscribe({
      next: (response) => {
        console.log('DataSummaryComponent: Full API response:', JSON.stringify(response, null, 2));
        console.log('DataSummaryComponent: response.success:', response.success);
        console.log('DataSummaryComponent: response.data:', response.data);
        
        this.isLoading = false;
        if (response && response.success === true) {
          this.dataSummary = response.data;
          console.log('DataSummaryComponent: dataSummary successfully set:', this.dataSummary);
        } else {
          const errorMsg = response?.error || response?.message || 'Failed to load database summary - success was false';
          this.error = errorMsg;
          console.error('DataSummaryComponent: API returned unsuccessful response:', errorMsg);
        }
      },
      error: (error) => {
        console.error('DataSummaryComponent: API call failed with error:', error);
        console.error('DataSummaryComponent: Error details:', JSON.stringify(error, null, 2));
        this.isLoading = false;
        this.error = `API call failed: ${error.message || error.status || 'Unknown error'}`;
      }
    });
  }

  refreshData(): void {
    this.loadDataSummary();
  }

  testConnection(): void {
    console.log('DataSummaryComponent: Testing connection to API...');
    this.dataService.testConnection().subscribe({
      next: (response) => {
        console.log('DataSummaryComponent: API connection test successful:', response);
        this.error = null; // Clear errors if connection test passes
      },
      error: (error) => {
        console.error('DataSummaryComponent: API connection test failed:', error);
        this.error = `Connection test failed: ${error.message || error}`;
      }
    });
  }

  getTableNames(): string[] {
    if (!this.dataSummary) return [];
    return Object.keys(this.dataSummary.database_structure);
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-CA', {
      style: 'currency',
      currency: 'CAD'
    }).format(amount);
  }

  formatNumber(num: number): string {
    return new Intl.NumberFormat('en-CA').format(num);
  }

  formatPercentage(value: number): string {
    return `${value.toFixed(1)}%`;
  }
}