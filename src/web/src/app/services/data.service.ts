import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { 
  UserProfile, 
  LoanInfo, 
  ProgramOfStudy, 
  LoanPayment, 
  ApiResponse,
  PaginatedApiResponse,
  GenerationStats,
  DatabaseSummaryResponse 
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
  generateData(parameters?: { num_payers?: number; start_date?: string; end_date?: string }): Observable<{ success: boolean; statistics: GenerationStats; message: string }> {
    // Default parameters if none provided
    const defaultParams = {
      num_payers: 1000,
      start_date: '2020-01-01',
      end_date: '2023-12-31'
    };
    
    // Merge provided parameters with defaults
    const requestBody = { ...defaultParams, ...parameters };
    
    return this.http.post<{ success: boolean; statistics: GenerationStats; message: string }>(
      `${this.baseUrl}/generate-data`, 
      requestBody
    );
  }

  // Get user profiles with pagination
  getUserProfiles(page: number = 1, perPage: number = 30): Observable<PaginatedApiResponse<UserProfile>> {
    return this.http.get<PaginatedApiResponse<UserProfile>>(`${this.baseUrl}/get-user-profiles?page=${page}&per_page=${perPage}`);
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

  // Get database summary (explore database) - with raw response debugging
  getDataBaseSummary(): Observable<any> {
    console.log('DataService: Making request to:', `${this.baseUrl}/explore-database`);
    return this.http.get(`${this.baseUrl}/explore-database`, { 
      responseType: 'text',
      observe: 'response'
    }).pipe(
      map((response: any) => {
        console.log('DataService: Raw response received:', response);
        console.log('DataService: Response status:', response.status);
        console.log('DataService: Response headers:', response.headers);
        console.log('DataService: Response body (text):', response.body);
        
        try {
          const parsed = JSON.parse(response.body);
          console.log('DataService: Successfully parsed JSON:', parsed);
          return parsed;
        } catch (parseError) {
          console.error('DataService: JSON parse error:', parseError);
          console.error('DataService: Failed to parse body:', response.body);
          throw new Error('Failed to parse response JSON');
        }
      }),
      catchError((error) => {
        console.error('DataService: HTTP error occurred:', error);
        console.error('DataService: Full error object:', JSON.stringify(error, null, 2));
        throw error;
      })
    );
  }

  // Test endpoint to verify communication
  testConnection(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/test`);
  }
}