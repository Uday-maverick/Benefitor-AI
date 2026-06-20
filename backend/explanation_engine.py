"""
Explanation engine — generates human-readable, empathetic explanations
for eligibility results using LLM or template fallback.
"""
import logging
from models import UserProfile, MatchResult
from llm_provider import call_llm

logger = logging.getLogger(__name__)

EXPLANATION_PROMPT = """You are a compassionate welfare benefits advisor for Indian citizens. 
Write a clear, encouraging, and concise explanation (2-3 sentences) for the following eligibility result.

Scheme: {scheme_name}
Status: {status}
Matched criteria: {matched_rules}
Missing information: {missing_rules}
User profile: {profile_summary}

IMPORTANT rules:
- Never say "you are approved" or "you will get". Use "may qualify", "appears eligible", "potentially eligible".
- Be warm, simple, and encouraging.
- If status is "Likely Not Eligible", be gentle and suggest alternatives or missing requirements.
- Keep it under 60 words.

Write just the explanation text, no headers or bullet points."""


async def enrich_explanations(
    results: list[MatchResult], profile: UserProfile
) -> list[MatchResult]:
    """
    Enhance MatchResult explanations with LLM-generated natural language.
    Falls back to the rule-based explanation if LLM is unavailable.
    """
    profile_summary = _build_profile_summary(profile)
    enhanced = []

    for result in results:
        if result.status == "Likely Not Eligible":
            enhanced.append(result)
            continue

        prompt = EXPLANATION_PROMPT.format(
            scheme_name=result.scheme_name,
            status=result.status,
            matched_rules=", ".join(result.matched_rules) or "none identified",
            missing_rules=", ".join(result.missing_rules) or "none",
            profile_summary=profile_summary,
        )

        llm_text = await call_llm(prompt, temperature=0.4)
        if llm_text:
            result = result.model_copy(update={"explanation": llm_text.strip()})

        enhanced.append(result)

    return enhanced


def _build_profile_summary(profile: UserProfile) -> str:
    """Compact profile summary for LLM prompts."""
    parts = []
    if profile.age:
        parts.append(f"Age {profile.age}")
    if profile.occupation:
        parts.append(profile.occupation)
    if profile.state:
        parts.append(f"from {profile.state}")
    if profile.annual_income:
        parts.append(f"income ₹{profile.annual_income:,.0f}/year")
    if profile.category:
        parts.append(f"category: {profile.category.upper()}")
    if profile.student_status:
        parts.append("student")
    if profile.farmer_status:
        parts.append("farmer")
    if profile.senior_citizen_status:
        parts.append("senior citizen")
    if profile.disability_status:
        parts.append("person with disability")
    return ", ".join(parts) if parts else "profile not fully specified"


async def generate_chat_reply(
    profile: UserProfile,
    results: list[MatchResult],
    follow_up_question: str | None,
    is_first_message: bool = False,
) -> str:
    """
    Generate the main chat reply text that accompanies the results.
    """
    if follow_up_question:
        return follow_up_question

    eligible = [r for r in results if r.status in ("Likely Eligible", "Possibly Eligible")]

    if not eligible:
        return (
            "Based on what you've shared, I couldn't find schemes that clearly match your profile right now. "
            "This could be because some information is still missing. "
            "Could you tell me more about your occupation, income, or housing situation?"
        )

    scheme_names = ", ".join(r.scheme_name for r in eligible[:3])
    count = len(eligible)

    prompt = f"""You are a helpful welfare benefits advisor for Indian citizens.

The user has described their situation and we found {count} potentially relevant government scheme(s): {scheme_names}.

Write a warm, encouraging 2-sentence response acknowledging what you understood about them and 
letting them know you've found some relevant schemes. Keep it conversational and simple.
End with "Please see the results panel on the right for details."

Do not list the schemes — just mention there are {count} scheme(s) found."""

    reply = await call_llm(prompt, temperature=0.5)
    if reply:
        return reply.strip()

    # Template fallback
    return (
        f"Great news! Based on your profile, I found {count} government scheme(s) that may be relevant to you "
        f"({scheme_names}). "
        "Please see the results panel on the right for details and eligibility explanations."
    )
