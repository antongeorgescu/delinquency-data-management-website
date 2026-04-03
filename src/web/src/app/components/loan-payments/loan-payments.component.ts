import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { LoanPayment } from '../../interfaces/data.interface';

@Component({
  selector: 'app-loan-payments',
  templateUrl: './loan-payments.component.html',
  styleUrls: ['./loan-payments.component.css']
})
export class LoanPaymentsComponent implements OnInit {
  loanPayments: LoanPayment[] = [];
  loading = true;
  error: string | null = null;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadLoanPayments();
  }

  loadLoanPayments(): void {
    this.loading = true;
    this.error = null;

    this.dataService.getLoanPayments().subscribe({
      next: (response) => {
        if (response.success) {
          this.loanPayments = response.data;
        } else {
          this.error = response.message || 'Failed to load loan payments';
        }
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load loan payments. Please try again.';
        this.loading = false;
        console.error('Error loading loan payments:', error);
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

  getStatusBadgeClass(status: string): string {
    const classes = {
      'Paid': 'status-paid',
      'Late': 'status-late',
      'Delinquent': 'status-delinquent',
      'Default': 'status-default'
    };
    return `badge ${classes[status as keyof typeof classes] || 'bg-secondary'}`;
  }
}