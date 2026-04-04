export interface UserProfile {
  payer_id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  age: number;
  address: string;
  city: string;
  province: string;
  employment_status: string;
  annual_income_cad: number;
  marital_status: string;
}

export interface LoanInfo {
  loan_id: number;
  payer_id: number;
  program_id: number;
  loan_amount: number;
  interest_rate: number;
  loan_term_years: number;
  loan_term_months: number;
  loan_type: string;
  institution_name: string;
  institution_city: string;
  institution_province: string;
  education_value: number;
  down_payment: number;
  ltv_ratio: number;
  origination_date: string;
  disbursement_date: string;
  maturity_date: string;
  current_balance: number;
  loan_status: string;
  lender: string;
  program_duration_years: number;
  monthly_payment: number;
  grace_period_months: number;
  delinquency_risk: number;
  first_name?: string;
  last_name?: string;
}

export interface ProgramOfStudy {
  program_id: number;
  program_name: string;
  program_type: string;
  field_of_study: string;
  program_difficulty: string;
  duration_years: number;
  typical_tuition_cad: number;
  employment_rate_percent: number;
  avg_starting_salary_cad: number;
  accreditation_body: string;
  institution_type: string;
  university_name: string;
  requires_licensing: string;
  job_market_outlook: string;
}

export interface Payment {
  payment_id: number;
  first_name: string;
  last_name: string;
  due_date: string;
  paid_date: string;
  payment_due: number;
  amount_paid: number;
  principal_payment: number;
  interest_payment: number;
  escrow_payment: number;
  late_fee: number;
  total_amount_due: number;
  remaining_balance: number;
  status: string;
  days_late: number;
  payment_method: string;
  payment_processor: string;
  transaction_id: string;
  confirmation_number: string;
  payment_type: string;
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

export interface PaginatedApiResponse<T> {
  success: boolean;
  data: T[];
  count: number;
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
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