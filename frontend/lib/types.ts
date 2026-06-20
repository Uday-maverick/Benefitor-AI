// Shared TypeScript types matching the FastAPI Pydantic models

export interface UserProfile {
  country?: string | null;
  age?: number | null;
  state?: string | null;
  district?: string | null;
  occupation?: string | null;
  annual_income?: number | null;
  category?: string | null;
  student_status?: boolean | null;
  farmer_status?: boolean | null;
  housing_status?: string | null;
  land_ownership?: boolean | null;
  disability_status?: boolean | null;
  senior_citizen_status?: boolean | null;
  gender?: string | null;
  bpl_card?: boolean | null;
  ration_card?: string | null;
}

export interface MatchResult {
  scheme_id: string;
  scheme_name: string;
  scheme_category: string;
  status: "Likely Eligible" | "Possibly Eligible" | "Likely Not Eligible";
  score: number;
  confidence: number;
  matched_rules: string[];
  missing_rules: string[];
  explanation: string;
  documents_required: string[];
  official_url: string;
}

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatResponse {
  reply: string;
  profile?: UserProfile | null;
  follow_up_question?: string | null;
  recommendations: MatchResult[];
  profile_complete: boolean;
}

export interface Scheme {
  id: string;
  name: string;
  category: string;
  summary: string;
  eligibility_rules: EligibilityRule[];
  documents_required: string[];
  official_url: string;
  benefit_amount?: string | null;
  ministry?: string | null;
}

export interface EligibilityRule {
  field: string;
  operator: string;
  value: unknown;
  label: string;
  weight: number;
  required: boolean;
}
