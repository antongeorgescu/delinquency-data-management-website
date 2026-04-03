import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { UserProfile } from '../../interfaces/data.interface';

@Component({
  selector: 'app-user-profiles',
  templateUrl: './user-profiles.component.html',
  styleUrls: ['./user-profiles.component.css']
})
export class UserProfilesComponent implements OnInit {
  userProfiles: UserProfile[] = [];
  loading = true;
  error: string | null = null;
  
  // Pagination properties
  currentPage = 1;
  perPage = 30;
  totalPages = 0;
  totalRecords = 0;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadUserProfiles();
  }

  loadUserProfiles(): void {
    this.loading = true;
    this.error = null;

    this.dataService.getUserProfiles(this.currentPage, this.perPage).subscribe({
      next: (response) => {
        if (response.success) {
          this.userProfiles = response.data;
          this.totalRecords = response.total;
          this.totalPages = response.total_pages;
          this.currentPage = response.page;
        } else {
          this.error = response.message || 'Failed to load user profiles';
        }
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load user profiles. Please try again.';
        this.loading = false;
        console.error('Error loading user profiles:', error);
      }
    });
  }

  // Pagination methods
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadUserProfiles();
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.goToPage(this.currentPage - 1);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.goToPage(this.currentPage + 1);
    }
  }

  getPageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    
    return pages;
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-CA', { 
      style: 'currency', 
      currency: 'CAD' 
    }).format(amount);
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}