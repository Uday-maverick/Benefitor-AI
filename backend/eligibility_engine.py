"""
Rule-based deterministic eligibility engine.
Evaluates a UserProfile against all schemes and returns MatchResult objects.
"""
from models import UserProfile, Scheme, MatchResult, EligibilityRule
from schemes_db import SCHEMES


def _evaluate_rule(rule: EligibilityRule, profile: UserProfile) -> tuple[bool, bool]:
    """
    Returns (matched: bool, data_available: bool).
    - matched: True if the rule passes
    - data_available: False if the profile field is None (can't evaluate)
    """
    value = getattr(profile, rule.field, None)

    if value is None:
        # Data not available — treat as unknown
        return False, False

    op = rule.operator

    if op == "is_true":
        return bool(value) is True, True
    elif op == "is_false":
        return bool(value) is False, True
    elif op == "eq":
        return value == rule.value, True
    elif op == "neq":
        return value != rule.value, True
    elif op == "gt":
        return float(value) > float(rule.value), True
    elif op == "gte":
        return float(value) >= float(rule.value), True
    elif op == "lt":
        return float(value) < float(rule.value), True
    elif op == "lte":
        return float(value) <= float(rule.value), True
    elif op == "in":
        return str(value).lower() in [str(v).lower() for v in rule.value], True
    elif op == "not_in":
        return str(value).lower() not in [str(v).lower() for v in rule.value], True

    return False, False


def evaluate_scheme(profile: UserProfile, scheme: Scheme) -> MatchResult:
    """
    Evaluate a UserProfile against a single Scheme.
    Returns a MatchResult with status, score, and explanation data.
    """
    matched_rules: list[str] = []
    missing_rules: list[str] = []
    failed_required: list[str] = []

    total_weight = 0.0
    matched_weight = 0.0

    for rule in scheme.eligibility_rules:
        matched, available = _evaluate_rule(rule, profile)

        total_weight += rule.weight

        if not available:
            # Profile data missing for this rule
            missing_rules.append(rule.label)
        elif matched:
            matched_rules.append(rule.label)
            matched_weight += rule.weight
        else:
            if rule.required:
                failed_required.append(rule.label)

    # Calculate score
    score = matched_weight / total_weight if total_weight > 0 else 0.0

    # Determine confidence based on how much data we have
    known_rules = len(matched_rules) + len(failed_required)
    total_rules = len(scheme.eligibility_rules)
    confidence = known_rules / total_rules if total_rules > 0 else 0.0

    # Determine status
    if failed_required:
        status = "Likely Not Eligible"
    elif missing_rules and score < 0.5:
        status = "Possibly Eligible"
    elif score >= 0.7:
        status = "Likely Eligible"
    elif score >= 0.4:
        status = "Possibly Eligible"
    else:
        status = "Likely Not Eligible"

    # Build explanation template (will be enhanced by LLM layer)
    if status == "Likely Eligible":
        explanation = (
            f"You appear to meet the key eligibility criteria for {scheme.name}. "
            f"Matched criteria: {'; '.join(matched_rules)}."
        )
    elif status == "Possibly Eligible":
        parts = []
        if matched_rules:
            parts.append(f"You meet some criteria: {'; '.join(matched_rules)}.")
        if missing_rules:
            parts.append(f"More information is needed on: {'; '.join(missing_rules)}.")
        explanation = " ".join(parts) or f"Partial match for {scheme.name}."
    else:
        explanation = (
            f"Based on the information provided, you may not qualify for {scheme.name}. "
            f"Criteria not met: {'; '.join(failed_required)}."
        )

    return MatchResult(
        scheme_id=scheme.id,
        scheme_name=scheme.name,
        scheme_category=scheme.category,
        status=status,
        score=round(score, 3),
        confidence=round(confidence, 3),
        matched_rules=matched_rules,
        missing_rules=missing_rules,
        explanation=explanation,
        documents_required=scheme.documents_required,
        official_url=scheme.official_url,
    )


def evaluate_all_schemes(profile: UserProfile) -> list[MatchResult]:
    """
    Evaluate a UserProfile against all known schemes.
    Returns results sorted by score (highest first).
    """
    results = [evaluate_scheme(profile, scheme) for scheme in SCHEMES]
    results.sort(key=lambda r: (r.score, r.confidence), reverse=True)
    return results


def get_missing_fields(profile: UserProfile) -> list[str]:
    """
    Returns a list of UserProfile field names that are still None
    and are important for determining eligibility.
    """
    important_fields = [
        "age", "state", "occupation", "annual_income",
        "student_status", "farmer_status", "housing_status",
        "senior_citizen_status", "disability_status",
    ]
    return [f for f in important_fields if getattr(profile, f, None) is None]
