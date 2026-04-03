import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { ProgramOfStudy } from '../../interfaces/data.interface';

@Component({
  selector: 'app-programs',
  templateUrl: './programs.component.html',
  styleUrls: ['./programs.component.css']
})
export class ProgramsComponent implements OnInit {
  programs: ProgramOfStudy[] = [];
  loading = true;
  error: string | null = null;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadPrograms();
  }

  loadPrograms(): void {
    this.loading = true;
    this.error = null;

    this.dataService.getPrograms().subscribe({
      next: (response) => {
        if (response.success) {
          this.programs = response.data;
        } else {
          this.error = response.message || 'Failed to load programs';
        }
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load programs. Please try again.';
        this.loading = false;
        console.error('Error loading programs:', error);
      }
    });
  }

  getBadgeClass(degreeLevel: string): string {
    const classes = {
      'Associate': 'bg-info',
      'Bachelor': 'bg-success',
      'Master': 'bg-warning',
      'Doctorate': 'bg-primary'
    };
    return classes[degreeLevel as keyof typeof classes] || 'bg-secondary';
  }
}