export interface UserProfile {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  created_at: string;
}

export interface LoanInfo {
  id: string;
  user_id: string;
  loan_amount: number;
  interest_rate: number;
  loan_type: string;
  created_at: string;
  first_name?: string;
  last_name?: string;
  email?: string;
}

export interface ProgramOfStudy {
  id: string;
  program_name: string;
  degree_level: string;
  duration_months: number;
}

export interface LoanPayment {
  id: string;
  loan_id: string;
  payment_amount: number;
  payment_date: string;
  status: string;
  loan_amount?: number;
  loan_type?: string;
  first_name?: string;
  last_name?: string;
  email?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T[];
  count: number;
  error?: string;
  message?: string;
}

export interface GenerationStats {
  user_profiles: number;
  loan_info: number;
  programs_of_study: number;
  loan_payments: number;
}

export interface DatabaseSummary {
  database_structure: { [tableName: string]: Array<{ name: string; type: string; primary_key: boolean }> };
  sample_user_profiles: Array<any>;
  employment_income_analysis: Array<any>;
  provincial_analysis: Array<any>;
  loan_amount_analysis: Array<any>;
  program_analysis: Array<any>;
  payment_status_analysis: Array<any>;
  payment_trends_analysis: Array<any>;
  summary: {
    total_tables: number;
    tables_analyzed: number;
    analysis_complete: boolean;
  };
}

export interface DatabaseSummaryResponse {
  success: boolean;
  message: string;
  data: DatabaseSummary;
  error?: string;
}