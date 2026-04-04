import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { ProgramOfStudy, PaginatedApiResponse } from '../../interfaces/data.interface';

@Component({
  selector: 'app-programs',
  templateUrl: './programs.component.html',
  styleUrls: ['./programs.component.css']
})
export class ProgramsComponent implements OnInit {
  programs: ProgramOfStudy[] = [];
  loading: boolean = false;
  error: string = '';
  
  // Pagination properties
  currentPage: number = 1;
  totalPages: number = 0;
  totalPrograms: number = 0;
  perPage: number = 30;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.loadPrograms();
  }

  loadPrograms(page: number = 1): void {
    this.loading = true;
    this.error = '';
    this.currentPage = page;

    this.dataService.getPrograms(page, this.perPage).subscribe({
      next: (response: PaginatedApiResponse<ProgramOfStudy>) => {
        console.log('Programs API Response:', response);
        
        if (response.success && response.data) {
          this.programs = response.data;
          this.totalPrograms = response.total || 0;
          this.totalPages = response.total_pages || 0;
          this.currentPage = response.page || 1;
          this.loading = false;
        } else {
          this.error = 'Failed to load programs data';
          this.loading = false;
        }
      },
      error: (error) => {
        console.error('Error loading programs:', error);
        this.error = 'Failed to load programs data. Please try again.';
        this.loading = false;
      }
    });
  }

  // Pagination methods
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.loadPrograms(page);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.loadPrograms(this.currentPage + 1);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.loadPrograms(this.currentPage - 1);
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

  formatPercentage(rate: number): string {
    if (rate === null || rate === undefined) return '0.00%';
    return `${rate.toFixed(2)}%`;
  }

  formatYears(years: number): string {
    if (years === null || years === undefined) return 'N/A';
    return `${years} years`;
  }

  getDifficultyBadgeClass(difficulty: string): string {
    const classes = {
      'Easy': 'bg-success',
      'Moderate': 'bg-warning',
      'Hard': 'bg-danger',
      'Very Hard': 'bg-dark'
    };
    return classes[difficulty as keyof typeof classes] || 'bg-secondary';
  }

  getTypeBadgeClass(type: string): string {
    const classes = {
      'Undergraduate': 'bg-info',
      'Graduate': 'bg-primary',
      'Postgraduate': 'bg-success',
      'Certificate': 'bg-warning'
    };
    return classes[type as keyof typeof classes] || 'bg-secondary';
  }
}