import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { Payment, PaginatedApiResponse } from '../../interfaces/data.interface';

@Component({
  selector: 'app-payments',
  templateUrl: './payments.component.html',
  styleUrls: ['./payments.component.css']
})
export class PaymentsComponent implements OnInit {
  payments: Payment[] = [];
  loading: boolean = false;
  error: string = '';
  
  // Pagination properties
  currentPage: number = 1;
  totalPages: number = 0;
  totalPayments: number = 0;
  perPage: number = 30;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.loadPayments();
  }

  loadPayments(page: number = 1): void {
    this.loading = true;
    this.error = '';
    this.currentPage = page;

    this.dataService.getPayments(page, this.perPage).subscribe({
      next: (response: PaginatedApiResponse<Payment>) => {
        console.log('Payments API Response:', response);
        
        if (response.success && response.data) {
          this.payments = response.data;
          this.totalPayments = response.total || 0;
          this.totalPages = response.total_pages || 0;
          this.currentPage = response.page || 1;
          this.loading = false;
        } else {
          this.error = 'Failed to load payments data';
          this.loading = false;
        }
      },
      error: (error) => {
        console.error('Error loading payments:', error);
        this.error = 'Failed to load payments data. Please try again.';
        this.loading = false;
      }
    });
  }

  // Pagination methods
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.loadPayments(page);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.loadPayments(this.currentPage + 1);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.loadPayments(this.currentPage - 1);
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
    const date = new Date(dateString);
    return date.toLocaleDateString('en-CA');
  }

  getStatusBadgeClass(status: string): string {
    const classes = {
      'Paid': 'bg-success',
      'Pending': 'bg-warning',
      'Late': 'bg-danger',
      'Missed': 'bg-dark',
      'Processing': 'bg-info'
    };
    return classes[status as keyof typeof classes] || 'bg-secondary';
  }

  getPaymentMethodBadgeClass(method: string): string {
    const classes = {
      'Auto-Pay': 'bg-primary',
      'Online Banking': 'bg-info',
      'Mobile App': 'bg-success', 
      'Phone': 'bg-warning',
      'Check': 'bg-secondary'
    };
    return classes[method as keyof typeof classes] || 'bg-secondary';
  }

  getDaysLateClass(daysLate: number): string {
    if (!daysLate || daysLate === 0) return 'text-success';
    if (daysLate <= 15) return 'text-warning';
    return 'text-danger';
  }

  formatDaysLate(daysLate: number): string {
    if (!daysLate || daysLate === 0) return 'On Time';
    return `${daysLate} days`;
  }

  getBorrowerName(payment: any): string {
    if (payment.first_name && payment.last_name) {
      return `${payment.first_name} ${payment.last_name}`;
    } else if (payment.first_name) {
      return payment.first_name;
    } else if (payment.last_name) {
      return payment.last_name;
    }
    return 'Unknown Borrower';
  }
}