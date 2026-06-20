"""
POST /api/extract-profile — extract a user profile from text
POST /api/evaluate — evaluate a profile against all schemes
"""
from fastapi import APIRouter
from models import ProfileExtractRequest, EvaluateRequest, UserProfile, MatchResult
from profile_extractor import extract_profile_from_text
from eligibility_engine import evaluate_all_schemes
from i18n import translate_match_result

router = APIRouter()


@router.post("/extract-profile", response_model=UserProfile)
async def extract_profile(request: ProfileExtractRequest):
    """Extract a structured profile from free-form text."""
    return await extract_profile_from_text(request.text)


@router.post("/evaluate", response_model=list[MatchResult])
async def evaluate(request: EvaluateRequest):
    """Evaluate a profile against all schemes and return match results."""
    results = evaluate_all_schemes(request.profile)
    lang = request.lang or "en"
    if lang == "en":
        return results
    return [translate_match_result(r, lang) for r in results]

