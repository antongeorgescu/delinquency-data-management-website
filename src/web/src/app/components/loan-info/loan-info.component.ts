import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { LoanInfo } from '../../interfaces/data.interface';

@Component({
  selector: 'app-loan-info',
  templateUrl: './loan-info.component.html',
  styleUrls: ['./loan-info.component.css']
})
export class LoanInfoComponent implements OnInit {
  loanInfo: LoanInfo[] = [];
  loading = true;
  error: string | null = null;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadLoanInfo();
  }

  loadLoanInfo(): void {
    this.loading = true;
    this.error = null;

    this.dataService.getLoanInfo().subscribe({
      next: (response) => {
        if (response.success) {
          this.loanInfo = response.data;
        } else {
          this.error = response.message || 'Failed to load loan information';
        }
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load loan information. Please try again.';
        this.loading = false;
        console.error('Error loading loan info:', error);
      }
    });
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}