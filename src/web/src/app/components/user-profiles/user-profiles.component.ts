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

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadUserProfiles();
  }

  loadUserProfiles(): void {
    this.loading = true;
    this.error = null;

    this.dataService.getUserProfiles().subscribe({
      next: (response) => {
        if (response.success) {
          this.userProfiles = response.data;
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

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}