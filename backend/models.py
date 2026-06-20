"""
Pydantic data models for Benefitor AI.
"""
from typing import Optional
from pydantic import BaseModel, Field


# ─── User Profile ─────────────────────────────────────────────────────────────

class UserProfile(BaseModel):
    country: Optional[str] = None             # "india", "us", or other country name
    age: Optional[int] = None
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None          # student, farmer, labourer, self-employed, etc.
    annual_income: Optional[float] = None      # in INR
    category: Optional[str] = None            # general, obc, sc, st
    student_status: Optional[bool] = None
    farmer_status: Optional[bool] = None
    housing_status: Optional[str] = None      # pucca, kutcha, rented, homeless
    land_ownership: Optional[bool] = None
    disability_status: Optional[bool] = None
    senior_citizen_status: Optional[bool] = None
    gender: Optional[str] = None
    bpl_card: Optional[bool] = None           # Below Poverty Line card holder
    ration_card: Optional[str] = None         # none, white, yellow, pink, green


# ─── Scheme ───────────────────────────────────────────────────────────────────

class EligibilityRule(BaseModel):
    field: str                    # UserProfile field name
    operator: str                 # eq, neq, gt, gte, lt, lte, in, not_in, is_true, is_false
    value: object                 # expected value
    label: str                    # human-readable rule description
    weight: float = 1.0           # importance weight for scoring
    required: bool = True         # if False, it boosts score but doesn't disqualify


class Scheme(BaseModel):
    id: str
    name: str
    category: str                 # farmer, housing, healthcare, pension, education
    summary: str
    eligibility_rules: list[EligibilityRule]
    documents_required: list[str]
    official_url: str
    benefit_amount: Optional[str] = None
    ministry: Optional[str] = None


# ─── Match Result ─────────────────────────────────────────────────────────────

class MatchResult(BaseModel):
    scheme_id: str
    scheme_name: str
    scheme_category: str
    status: str                   # "Likely Eligible", "Possibly Eligible", "Likely Not Eligible"
    score: float                  # 0.0 – 1.0
    confidence: float             # 0.0 – 1.0
    matched_rules: list[str]
    missing_rules: list[str]
    explanation: str
    documents_required: list[str]
    official_url: str


# ─── API Request / Response ───────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str                     # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: list[ChatMessage] = Field(default_factory=list)
    lang: Optional[str] = "en"


class ChatResponse(BaseModel):
    reply: str
    profile: Optional[UserProfile] = None
    follow_up_question: Optional[str] = None
    recommendations: list[MatchResult] = Field(default_factory=list)
    profile_complete: bool = False


class ProfileExtractRequest(BaseModel):
    text: str


class EvaluateRequest(BaseModel):
    profile: UserProfile
    lang: Optional[str] = "en"

