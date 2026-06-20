"""
Profile extractor — converts free-form user text into a structured UserProfile.
Uses Gemini LLM when available, falls back to keyword-based heuristics.
"""
import re
import logging
from models import UserProfile
from llm_provider import call_llm_json, PROFILE_SCHEMA

logger = logging.getLogger(__name__)

# ─── LLM Extraction ───────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """You are a welfare benefits assistant for India and the United States. Extract structured information from the user's message below.

Extract these fields if mentioned:
- age (integer, years)
- state (Indian or US state name, e.g. California, Texas, Punjab, Maharashtra, string)
- district (string, e.g. city or county if in the US)
- occupation (string: student, farmer, labourer, self-employed, government-employee, unemployed, retired, other)
- annual_income (integer, in the user's currency - INR or USD - per year — convert if monthly given. Do not write currency symbols)
- category (string: general, obc, sc, st, minority)
- student_status (boolean: true if enrolled in school/college)
- farmer_status (boolean: true if engaged in farming)
- housing_status (string: pucca, kutcha, rented, homeless)
- land_ownership (boolean: true if owns agricultural land)
- disability_status (boolean)
- senior_citizen_status (boolean: true if age >= 60 or age >= 65)
- gender (string: male, female, other)
- bpl_card (boolean: true if has BPL/ration card or is considered low-income/below federal poverty level)

Return a JSON object with only the fields you can confidently extract. Use null for fields not mentioned.

User message: "{user_text}" """


FOLLOWUP_PROMPT = """You are a helpful welfare benefits assistant for India.

The user's profile so far is:
{profile_json}

Missing important fields: {missing_fields}

The conversation so far:
{history}

Ask ONE focused, friendly question in simple English to gather the most important missing information.
The question should feel natural and conversational, not like a form.
Keep it under 2 sentences. Do NOT ask multiple questions at once.

Respond with just the question text."""


async def extract_profile_from_text(text: str) -> UserProfile:
    """
    Extract a UserProfile from free-form text using LLM + heuristic fallback.
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
        try:
            return UserProfile(**clean)
        except Exception as e:
            logger.warning(f"Profile parse error: {e}")

    # ── Heuristic fallback ────────────────────────────────────────────────────
    logger.info("Using heuristic profile extraction fallback")
    return _heuristic_extract(text)


def _heuristic_extract(text: str) -> UserProfile:
    """Keyword-based fallback extraction when LLM is unavailable."""
    t = text.lower()
    profile_data: dict = {}

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

    # State detection (common Indian and US states)
    states = [
        "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
        "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka",
        "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya",
        "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim",
        "tamil nadu", "telangana", "tripura", "uttar pradesh", "uttarakhand",
        "west bengal", "delhi",
        "california", "texas", "new york", "florida", "illinois", "pennessee",
        "pennsylvania", "ohio", "georgia", "north carolina", "michigan",
        "washington", "massachusetts", "new jersey", "virginia", "colorado",
    ]
    for state in states:
        if state in t:
            profile_data["state"] = state.title()
            break

    return UserProfile(**profile_data)


def merge_profiles(base: UserProfile, update: UserProfile) -> UserProfile:
    """
    Merge two profiles — update fields win over None base fields.
    """
    base_dict = base.model_dump()
    update_dict = update.model_dump()
    merged = {k: (update_dict[k] if update_dict[k] is not None else base_dict[k]) for k in base_dict}
    return UserProfile(**merged)


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
    question = await call_llm_json.__wrapped__(prompt) if hasattr(call_llm_json, "__wrapped__") else None

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
