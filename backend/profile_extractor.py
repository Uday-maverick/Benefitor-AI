"""
Profile extractor — converts free-form user text into a structured UserProfile.

DESIGN: LLM-first architecture.
  - The LLM handles ALL contextual understanding (universities, cities,
    currencies, documents, institutions → country mapping).
  - Hardcoded keyword lists are kept ONLY inside _heuristic_extract() as a
    degraded fallback when the LLM API is unavailable.
  - This avoids brittle hardcoded lists that can never cover every edge case
    the way a language model can.
"""
import re
import logging
from typing import Optional
from models import UserProfile
from llm_provider import call_llm_json, PROFILE_SCHEMA

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

# Supported countries (used by chat route to gate unsupported-country replies)
SUPPORTED_COUNTRIES = {"india", "us"}


# ─── LLM Prompts ─────────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """You are an intelligent welfare benefits assistant. Your job is to extract structured profile information from the user's message.

## STEP 1 — Determine the user's COUNTRY (most important)

Use your world knowledge to infer the user's country from ANY contextual clue:
- **Universities & institutions**: Know which country each university is in.
  Examples: CMU/Carnegie Mellon → US (Pittsburgh, PA). IIT/AIIMS → India. Oxford → UK. Sorbonne → France.
  You are NOT limited to these examples — use your knowledge of ALL universities worldwide.
- **States, cities, regions**: California → US. Maharashtra → India. Bavaria → Germany. Ontario → Canada.
- **Currency**: $, USD → US. ₹, INR, lakh, crore → India. €, EUR → Europe. £, GBP → UK.
- **Government documents & programs**: SSN, FAFSA, Medicare, SNAP, Section 8 → US. Aadhaar, PAN card, ration card, PM-KISAN → India.
- **Language/cultural clues**: If they mention "yojana", "sahay", or Hindi/regional Indian terms → India.
- **Explicit mentions**: "I live in France", "I'm Canadian", etc.

Country values:
- Set to "india" if user is in India
- Set to "us" if user is in the United States
- Set to the country name in lowercase (e.g. "france", "uk", "canada", "germany") if user is in another country
- Set to null ONLY if there are genuinely no clues at all

## STEP 2 — Extract profile fields

Extract these fields if mentioned (use null for fields not mentioned):
- country (string, as described above)
- age (integer, years)
- state (string — the state/province name within their country, e.g. "California", "Punjab", "Maharashtra")
- district (string — city, district, or county)
- occupation (string: student, farmer, labourer, self-employed, government-employee, unemployed, retired, other)
- annual_income (integer — annual income in their local currency. Convert monthly to annual. No currency symbols.)
- category (string: general, obc, sc, st, minority — applicable mainly for India)
- student_status (boolean: true if enrolled in any school, college, or university)
- farmer_status (boolean: true if engaged in farming/agriculture)
- housing_status (string: pucca, kutcha, rented, homeless)
- land_ownership (boolean: true if owns agricultural land)
- disability_status (boolean)
- senior_citizen_status (boolean: true if age >= 60)
- gender (string: male, female, other)
- bpl_card (boolean: true if has BPL/ration card or is below poverty line)

Return a JSON object with only the fields you can confidently extract.

User message: \"{user_text}\" """


FOLLOWUP_PROMPT = """You are a helpful welfare benefits assistant for India and the United States.

The user's profile so far is:
{profile_json}

Missing important fields: {missing_fields}

The conversation so far:
{history}

Ask ONE focused, friendly question in simple English to gather the most important missing information.
The question should feel natural and conversational, not like a form.
Keep it under 2 sentences. Do NOT ask multiple questions at once.
If the user's country is not yet known, prioritize asking which country they are based in.

Respond with just the question text."""


# ─── Country normalization ────────────────────────────────────────────────────
# This is NOT "intelligence" — just string normalization so downstream code can
# use simple == checks.  The LLM does the actual country detection.

def _normalize_country(country_raw: str) -> str:
    """Normalize LLM-returned country strings to canonical form."""
    c = country_raw.lower().strip()
    if c in ("united states", "usa", "u.s.", "u.s.a.", "america", "united states of america"):
        return "us"
    if c in ("bharat", "hindustan"):
        return "india"
    if c in ("united kingdom", "england", "great britain", "scotland", "wales", "northern ireland"):
        return "uk"
    return c


# Minimal Indian state set — only used for state→country derivation when the
# LLM returned a state but not a country.  NOT used for text scanning.
_INDIAN_STATES_SET = {
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka",
    "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya",
    "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim",
    "tamil nadu", "telangana", "tripura", "uttar pradesh", "uttarakhand",
    "west bengal", "delhi", "jammu and kashmir", "ladakh",
    "andaman and nicobar", "chandigarh", "dadra and nagar haveli",
    "daman and diu", "lakshadweep", "puducherry",
}


def _derive_country_from_state(profile_data: dict) -> dict:
    """
    If the LLM returned a country, normalize it.
    If it returned a state but no country, derive country from state name.
    """
    from schemes_db import US_STATES

    if profile_data.get("country"):
        profile_data["country"] = _normalize_country(profile_data["country"])
        return profile_data

    state = profile_data.get("state", "")
    if state:
        state_lower = state.lower().strip()
        if any(state_lower == s.lower() for s in US_STATES):
            profile_data["country"] = "us"
        elif state_lower in _INDIAN_STATES_SET:
            profile_data["country"] = "india"

    return profile_data


# ─── Main extraction (LLM-first) ─────────────────────────────────────────────

async def extract_profile_from_text(text: str) -> UserProfile:
    """
    Extract a UserProfile from free-form text.

    PRIMARY path: LLM does all the heavy lifting — country detection,
    occupation mapping, income conversion, etc.  We only normalize
    the country string and derive country from state as a safety net.

    FALLBACK path: keyword-based heuristics when LLM is unavailable.
    """
    data = await call_llm_json(
        EXTRACTION_PROMPT.format(user_text=text),
        schema=PROFILE_SCHEMA,
    )

    if data:
        # Clean and validate data
        clean = {k: v for k, v in data.items() if v is not None and k in UserProfile.model_fields}
        # Derive implicit flags
        if "age" in clean and clean["age"] and int(clean["age"]) >= 60:
            clean["senior_citizen_status"] = True
        if clean.get("occupation", "").lower() == "student":
            clean["student_status"] = True
        if clean.get("occupation", "").lower() == "farmer":
            clean["farmer_status"] = True
        # Normalize country + derive from state if LLM didn't set it
        clean = _derive_country_from_state(clean)
        try:
            return UserProfile(**clean)
        except Exception as e:
            logger.warning(f"Profile parse error: {e}")

    # ── Heuristic fallback (LLM completely unavailable) ───────────────────────
    logger.info("Using heuristic profile extraction fallback")
    return _heuristic_extract(text)


# ─── Heuristic fallback (offline / no-API-key mode) ──────────────────────────
# These keyword lists only run when the LLM is COMPLETELY unavailable.
# They are intentionally basic — the LLM is always better.

def _heuristic_extract(text: str) -> UserProfile:
    """Keyword-based fallback extraction when LLM is unavailable."""
    from schemes_db import US_STATES

    t = text.lower()
    profile_data: dict = {}

    # ── Country detection (basic keyword fallback) ────────────────────────────
    # Only a small set of high-confidence signals.  The LLM handles everything
    # else — we don't try to enumerate every university or city here.
    if re.search(r'₹|\binr\b|\brupees?\b|\blakh\b|\blakhs\b', t):
        profile_data["country"] = "india"
    elif re.search(r'\$|\busd\b|\bdollars?\b', t):
        profile_data["country"] = "us"
    elif any(kw in t for kw in ["aadhaar", "aadhar", "pan card", "ration card", "bpl card", "yojana"]):
        profile_data["country"] = "india"
    elif any(kw in t for kw in ["ssn", "social security", "fafsa", "ebt card", "medicaid", "snap"]):
        profile_data["country"] = "us"

    # Age
    age_match = re.search(r'\b(\d{1,2})\s*(?:year|yr)s?\s*old\b|\bage[d]?\s*(\d{1,2})\b', t)
    if age_match:
        profile_data["age"] = int(age_match.group(1) or age_match.group(2))

    # Income
    income_match = re.search(
        r'(?:income|earn|salary)[^\d]*(\d[\d,]*)\s*(?:lakh|lac|lakhs|lacs|thousand|k)?\s*(?:per\s*(year|month|annum))?',
        t
    )
    if income_match:
        amount = int(income_match.group(1).replace(",", ""))
        unit = income_match.group(0).lower()
        if "lakh" in unit or "lac" in unit:
            amount *= 100000
        elif "thousand" in unit or "k" in unit:
            amount *= 1000
        if "month" in unit:
            amount *= 12
        profile_data["annual_income"] = amount

    # Student
    if any(w in t for w in ["student", "studying", "school", "college", "university", "engineering", "medical", "class", "std "]):
        profile_data["student_status"] = True
        profile_data["occupation"] = "student"

    # Farmer
    if any(w in t for w in ["farmer", "farming", "agriculture", "kisan", "farm"]):
        profile_data["farmer_status"] = True
        profile_data["occupation"] = "farmer"

    # Land
    if any(w in t for w in ["acre", "bigha", "land", "field", "khet"]):
        profile_data["land_ownership"] = True

    # Senior citizen
    if any(w in t for w in ["senior", "elderly", "old age", "pensioner", "retired", "widow"]):
        profile_data["senior_citizen_status"] = True
    if profile_data.get("age") and profile_data["age"] >= 60:
        profile_data["senior_citizen_status"] = True

    # Disability
    if any(w in t for w in ["disabled", "disability", "handicapped", "differently abled", "divyang"]):
        profile_data["disability_status"] = True

    # Housing
    if any(w in t for w in ["kutcha", "thatched", "mud house", "kachha"]):
        profile_data["housing_status"] = "kutcha"
    elif any(w in t for w in ["rent", "rented", "tenant"]):
        profile_data["housing_status"] = "rented"
    elif any(w in t for w in ["homeless", "no house", "no home"]):
        profile_data["housing_status"] = "homeless"

    # Category
    for cat in ["sc", "st", "obc", "general", "minority"]:
        if re.search(rf'\b{cat}\b', t):
            profile_data["category"] = cat
            break

    # BPL
    if any(w in t for w in ["bpl", "below poverty", "ration card"]):
        profile_data["bpl_card"] = True

    # State detection
    us_states_lower = [s.lower() for s in US_STATES]
    all_states = list(_INDIAN_STATES_SET) + us_states_lower
    for state in all_states:
        if state in t:
            profile_data["state"] = state.title()
            break

    # Derive country from state if not already set
    profile_data = _derive_country_from_state(profile_data)

    return UserProfile(**profile_data)


# ─── Profile merging ─────────────────────────────────────────────────────────

def merge_profiles(base: UserProfile, update: UserProfile) -> UserProfile:
    """
    Merge two profiles — update fields win over None base fields.
    If country switches, clear country-specific fields of the base profile.
    """
    base_dict = base.model_dump()
    update_dict = update.model_dump()

    # Clear country-specific fields if switching country
    base_country = (base_dict.get("country") or "").lower().strip()
    update_country = (update_dict.get("country") or "").lower().strip()
    if base_country and update_country and base_country != update_country:
        country_specific_fields = {
            "state", "district", "annual_income", "category",
            "bpl_card", "ration_card", "land_ownership"
        }
        for f in country_specific_fields:
            base_dict[f] = None

    merged = {k: (update_dict[k] if update_dict[k] is not None else base_dict[k]) for k in base_dict}
    return UserProfile(**merged)


# ─── Follow-up question generation ───────────────────────────────────────────

async def generate_followup_question(
    profile: UserProfile,
    missing_fields: list[str],
    history: str,
) -> str:
    """
    Generate a single focused follow-up question for missing profile data.
    """
    import json as json_lib
    prompt = FOLLOWUP_PROMPT.format(
        profile_json=json_lib.dumps(profile.model_dump(exclude_none=True), indent=2),
        missing_fields=", ".join(missing_fields),
        history=history,
    )

    # Use direct LLM text call
    from llm_provider import call_llm
    raw = await call_llm(prompt, temperature=0.5)
    if raw:
        return raw.strip()

    # Heuristic fallback
    return _heuristic_followup(missing_fields)


def _heuristic_followup(missing_fields: list[str]) -> str:  # noqa: exported by chat.py
    """Fallback question generation."""
    questions = {
        "country": "Which country are you based in? We currently support government schemes for India and the United States.",
        "annual_income": "Could you tell me your approximate annual family income?",
        "state": "Which state do you live in?",
        "student_status": "Are you currently enrolled as a student?",
        "farmer_status": "Does your family engage in farming activities?",
        "land_ownership": "Does your family own any agricultural land?",
        "housing_status": "What type of housing do you currently live in (own house, rented, or temporary shelter)?",
        "senior_citizen_status": "Are you or any family member above 60 years of age?",
        "disability_status": "Does anyone in the household have a disability?",
        "age": "May I ask your age?",
        "category": "Do you belong to a reserved category such as SC, ST, or OBC?",
    }
    for field in missing_fields:
        if field in questions:
            return questions[field]
    return "Could you share a bit more about your family situation so I can find relevant benefits?"
