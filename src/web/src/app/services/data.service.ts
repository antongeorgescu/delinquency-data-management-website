import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  UserProfile, 
  LoanInfo, 
  ProgramOfStudy, 
  LoanPayment, 
  ApiResponse,
  GenerationStats 
} from '../interfaces/data.interface';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private baseUrl: string;

  constructor(private http: HttpClient) {
    // Use local Flask API server
    this.baseUrl = 'http://localhost:5000/api';
  }

  // Generate synthetic data
  generateData(): Observable<{ success: boolean; statistics: GenerationStats; message: string }> {
    return this.http.post<{ success: boolean; statistics: GenerationStats; message: string }>(
      `${this.baseUrl}/generate-data`, 
      {}
    );
  }

  // Get user profiles
  getUserProfiles(): Observable<ApiResponse<UserProfile>> {
    return this.http.get<ApiResponse<UserProfile>>(`${this.baseUrl}/get-user-profiles`);
  }

  // Get loan information
  getLoanInfo(): Observable<ApiResponse<LoanInfo>> {
    return this.http.get<ApiResponse<LoanInfo>>(`${this.baseUrl}/get-loan-info`);
  }

  // Get programs of study
  getPrograms(): Observable<ApiResponse<ProgramOfStudy>> {
    return this.http.get<ApiResponse<ProgramOfStudy>>(`${this.baseUrl}/get-programs`);
  }

  // Get loan payments
  getLoanPayments(): Observable<ApiResponse<LoanPayment>> {
    return this.http.get<ApiResponse<LoanPayment>>(`${this.baseUrl}/get-loan-payments`);
  }
}