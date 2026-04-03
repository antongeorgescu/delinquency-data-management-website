import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { LoanInfo, PaginatedApiResponse } from '../../interfaces/data.interface';

@Component({
  selector: 'app-loans',
  templateUrl: './loans.component.html',
  styleUrls: ['./loans.component.css']
})
export class LoansComponent implements OnInit {
  loans: LoanInfo[] = [];
  loading: boolean = false;
  error: string = '';
  
  // Pagination properties
  currentPage: number = 1;
  totalPages: number = 0;
  totalLoans: number = 0;
  perPage: number = 30;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.loadLoans();
  }

  loadLoans(page: number = 1): void {
    this.loading = true;
    this.error = '';
    this.currentPage = page;

    this.dataService.getLoans(page, this.perPage).subscribe({
      next: (response: PaginatedApiResponse<LoanInfo>) => {
        console.log('Loans API Response:', response);
        
        if (response.success && response.data) {
          this.loans = response.data;
          this.totalLoans = response.total || 0;
          this.totalPages = response.total_pages || 0;
          this.currentPage = response.page || 1;
          this.loading = false;
        } else {
          this.error = 'Failed to load loan data';
          this.loading = false;
        }
      },
      error: (error) => {
        console.error('Error loading loans:', error);
        this.error = 'Failed to load loan data. Please try again.';
        this.loading = false;
      }
    });
  }

  // Pagination methods
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.loadLoans(page);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.loadLoans(this.currentPage + 1);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.loadLoans(this.currentPage - 1);
    }
  }

  getPageNumbers(): number[] {
    const pages: number[] = [];
    const startPage = Math.max(1, this.currentPage - 2);
    const endPage = Math.min(this.totalPages, this.currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
    return pages;
  }

  // Helper methods for formatting
  formatCurrency(amount: number): string {
    if (amount === null || amount === undefined) return '$0.00';
    return new Intl.NumberFormat('en-CA', { 
      style: 'currency', 
      currency: 'CAD' 
    }).format(amount);
  }

  formatDate(dateString: string): string {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-CA');
    } catch (error) {
      return dateString;
    }
  }

  formatPercentage(rate: number): string {
    if (rate === null || rate === undefined) return '0.00%';
    return `${(rate * 100).toFixed(2)}%`;
  }

  formatInterestRate(rate: number): string {
    if (rate === null || rate === undefined) return '0.00';
    return rate.toFixed(2);
  }

  formatRiskLevel(risk: number): { text: string; class: string } {
    if (risk === null || risk === undefined) return { text: 'Unknown', class: 'bg-secondary' };
    
    if (risk < 0.3) return { text: 'Low', class: 'bg-success' };
    if (risk < 0.6) return { text: 'Medium', class: 'bg-warning' };
    if (risk < 0.8) return { text: 'High', class: 'bg-danger' };
    return { text: 'Critical', class: 'bg-dark' };
  }

  getBorrowerName(loan: LoanInfo): string {
    if (loan.first_name && loan.last_name) {
      return `${loan.first_name} ${loan.last_name}`;
    }
    return 'N/A';
  }
}