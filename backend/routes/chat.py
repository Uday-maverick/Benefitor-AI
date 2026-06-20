"""
POST /api/chat — main conversation endpoint.

LLM BUDGET: exactly 1 call per user turn (profile extraction).
Everything else — eligibility matching, explanations, chat reply — is
deterministic rule-based logic. This keeps us well within free-tier limits.
"""
import json
import logging
from fastapi import APIRouter
from models import ChatRequest, ChatResponse, UserProfile, MatchResult
from profile_extractor import extract_profile_from_text, merge_profiles, _heuristic_followup, SUPPORTED_COUNTRIES
from eligibility_engine import evaluate_all_schemes, get_missing_fields
from i18n import build_chat_reply_translated, translate_match_result

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── Rule-based explanation templates ────────────────────────────────────────

def _build_explanation(result: MatchResult, profile: UserProfile) -> str:
    """
    Generate a concise, human-friendly explanation using only rule data.
    No LLM required — keeps us to 1 call/turn.
    """
    name = result.scheme_name
    matched = result.matched_rules
    missing = result.missing_rules

    if result.status == "Likely Eligible":
        base = f"Based on your profile, you appear eligible for {name}."
        if matched:
            criteria = matched[0] if len(matched) == 1 else f"{matched[0]} and {len(matched)-1} other criteria"
            base += f" You meet the key requirement: {criteria.lower()}."
        if missing:
            base += f" You may still need to confirm: {missing[0].lower()}."
        return base

    if result.status == "Possibly Eligible":
        base = f"You may potentially qualify for {name}, though some information is still unclear."
        if missing:
            base += f" The main uncertainty is: {missing[0].lower()}."
        if matched:
            base += f" You do meet: {matched[0].lower()}."
        return base

    # Likely Not Eligible
    base = f"Based on current information, you may not qualify for {name}."
    if missing:
        base += f" The key unmet requirement is: {missing[0].lower()}."
    return base


def _build_chat_reply(
    profile: UserProfile,
    results: list[MatchResult],
    missing: list[str],
    is_first_message: bool,
) -> str:
    """
    Generate a conversational reply using only template logic. Zero LLM calls.
    """
    eligible = [r for r in results if r.status in ("Likely Eligible", "Possibly Eligible")]
    count = len(eligible)

    if not eligible:
        if len(missing) >= 5:
            # Ask for the most important missing field
            return _heuristic_followup(missing[:3])
        return (
            "Based on what you've shared, I couldn't find schemes that clearly match your profile right now. "
            "Could you tell me more about your occupation, income, or housing situation?"
        )

    # Build a warm, personalised response from profile data
    parts = []
    if profile.state:
        parts.append(f"in {profile.state}")
    if profile.occupation:
        parts.append(f"as a {profile.occupation}")
    if profile.annual_income:
        parts.append(f"with an annual income of ₹{profile.annual_income:,.0f}")

    context = ", ".join(parts) if parts else "based on your profile"

    scheme_names = ", ".join(r.scheme_name for r in eligible[:2])
    tail = f" and {count - 2} more" if count > 2 else ""

    return (
        f"I've reviewed your situation {context}. "
        f"I found {count} government scheme{'s' if count > 1 else ''} you may qualify for — "
        f"including {scheme_names}{tail}. "
        "Check the results panel on the right for full eligibility details and required documents."
    )


# ─── Main endpoint ────────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Single-turn chat endpoint.
    LLM calls per request: exactly 1 (profile extraction via call_llm_json).
    All other logic is deterministic.
    """

    # ── 1. Build context text (filter out system/profile messages for LLM context) ──
    chat_history = [m for m in request.conversation_history if m.role != "system"]
    history_text = "\n".join(
        f"{m.role.title()}: {m.content}"
        for m in chat_history[-6:]
    )
    full_text = f"{history_text}\nUser: {request.message}" if history_text else request.message

    # ── 2. Extract profile — THE only LLM call ────────────────────────────────
    new_profile = await extract_profile_from_text(full_text)

    # ── 3. Merge with previous turn's profile ─────────────────────────────────
    prev_profile_data: dict = {}
    for msg in request.conversation_history:
        if msg.role == "system" and msg.content.startswith("{"):
            try:
                prev_profile_data = json.loads(msg.content)
            except Exception:
                pass

    if prev_profile_data:
        base = UserProfile(**{k: v for k, v in prev_profile_data.items() if k in UserProfile.model_fields})
        merged = merge_profiles(base, new_profile)
    else:
        merged = new_profile

    # ── 3.5. Unsupported country check ────────────────────────────────────────
    user_country = (merged.country or "").lower().strip()
    if user_country and user_country not in SUPPORTED_COUNTRIES:
        from i18n import CHAT_REPLY_TEMPLATES
        lang = request.lang or "en"
        t_dict = CHAT_REPLY_TEMPLATES.get(lang, CHAT_REPLY_TEMPLATES["en"])
        # Format country name nicely for display
        display_country = user_country.replace("_", " ").title()
        unsupported_reply = t_dict["unsupported_country"].format(country=display_country)
        return ChatResponse(
            reply=unsupported_reply,
            profile=merged,
            follow_up_question=None,
            recommendations=[],
            profile_complete=False,
        )

    # ── 4. Evaluate schemes (rule-based, instant, country-filtered) ───────────
    results = evaluate_all_schemes(merged)
    missing = get_missing_fields(merged)

    # ── 5. Enrich & translate explanations ───────────────────────────────────
    lang = request.lang or "en"
    translated_results = [
        translate_match_result(r, lang)
        for r in results
    ]
    # Slice to return only top 5 best schemes
    translated_results = translated_results[:5]


    # ── 6. Build chat reply — template only, zero LLM ────────────────────────
    reply = build_chat_reply_translated(
        merged,
        translated_results,
        missing,
        is_first_message=len(request.conversation_history) == 0,
        lang=lang,
    )

    profile_complete = len(missing) <= 3

    return ChatResponse(
        reply=reply,
        profile=merged,
        follow_up_question=None,
        recommendations=translated_results,
        profile_complete=profile_complete,
    )
