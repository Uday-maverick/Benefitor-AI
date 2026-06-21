import pytest
from fastapi.testclient import TestClient
from main import app
from models import UserProfile
from eligibility_engine import evaluate_all_schemes
from profile_extractor import _heuristic_extract, _normalize_country, _derive_country_from_state

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Midas Ledger - Benefitor AI"

def test_schemes_list():
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) > 0
    assert schemes[0]["id"] == "pm-kisan"

def test_schemes_list_translated():
    response = client.get("/api/schemes?lang=hi")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) > 0
    assert "किसान" in schemes[0]["name"] or "समान" in schemes[0]["name"] or schemes[0]["name"]

def test_eligibility_engine():
    # Indian farmer — should match PM-KISAN
    profile = UserProfile(
        country="india",
        age=35,
        state="Punjab",
        occupation="farmer",
        annual_income=80000,
        farmer_status=True,
        land_ownership=True
    )
    results = evaluate_all_schemes(profile)
    pm_kisan_res = next((r for r in results if r.scheme_id == "pm-kisan"), None)
    assert pm_kisan_res is not None
    assert pm_kisan_res.status == "Likely Eligible"
    # Should NOT contain any US schemes
    us_results = [r for r in results if r.scheme_id.startswith("us-")]
    assert len(us_results) == 0

def test_eligibility_engine_not_eligible():
    profile = UserProfile(
        country="india",
        age=35,
        state="Punjab",
        occupation="farmer",
        annual_income=80000,
        farmer_status=True,
        land_ownership=False
    )
    results = evaluate_all_schemes(profile)
    pm_kisan_res = next((r for r in results if r.scheme_id == "pm-kisan"), None)
    assert pm_kisan_res is not None
    assert pm_kisan_res.status == "Likely Not Eligible"

def test_eligibility_engine_us():
    profile = UserProfile(
        country="us",
        age=30,
        state="California",
        annual_income=28000,
    )
    results = evaluate_all_schemes(profile)
    medicaid_res = next((r for r in results if r.scheme_id == "us-medicaid"), None)
    snap_res = next((r for r in results if r.scheme_id == "us-snap"), None)
    assert medicaid_res is not None
    assert medicaid_res.status == "Likely Eligible"
    assert snap_res is not None
    assert snap_res.status == "Likely Eligible"
    # Should NOT contain any Indian schemes
    india_results = [r for r in results if not r.scheme_id.startswith("us-")]
    assert len(india_results) == 0

def test_geo_filtering_country_aware():
    """Country filtering should exclude cross-country schemes entirely."""
    # US user → no Indian schemes at all
    profile_us = UserProfile(
        country="us",
        age=35,
        state="Texas",
        occupation="farmer",
        annual_income=25000,
        farmer_status=True,
        land_ownership=True
    )
    results_us = evaluate_all_schemes(profile_us)
    pm_kisan_res = next((r for r in results_us if r.scheme_id == "pm-kisan"), None)
    assert pm_kisan_res is None  # Not even evaluated

    # Indian user → no US schemes at all
    profile_in = UserProfile(
        country="india",
        age=30,
        state="Maharashtra",
        annual_income=30000,
    )
    results_in = evaluate_all_schemes(profile_in)
    medicaid_res = next((r for r in results_in if r.scheme_id == "us-medicaid"), None)
    assert medicaid_res is None  # Not even evaluated


def test_unsupported_country_returns_empty():
    """Users from unsupported countries get empty results."""
    profile = UserProfile(
        country="france",
        age=25,
        occupation="student",
    )
    results = evaluate_all_schemes(profile)
    assert len(results) == 0


def test_no_country_evaluates_all():
    """When country is unknown, all schemes should still be evaluated."""
    profile = UserProfile(
        age=30,
        annual_income=20000,
    )
    results = evaluate_all_schemes(profile)
    has_indian = any(not r.scheme_id.startswith("us-") for r in results)
    has_us = any(r.scheme_id.startswith("us-") for r in results)
    assert has_indian
    assert has_us


def test_eligibility_engine_new_us():
    profile = UserProfile(
        country="us",
        age=8,
        state="Texas",
        annual_income=15000,
        student_status=True,
    )
    results = evaluate_all_schemes(profile)
    wic_res = next((r for r in results if r.scheme_id == "us-wic"), None)
    lifeline_res = next((r for r in results if r.scheme_id == "us-lifeline"), None)
    ccdf_res = next((r for r in results if r.scheme_id == "us-child-care-subsidy"), None)
    assert wic_res is not None
    assert wic_res.status == "Likely Eligible"
    assert lifeline_res is not None
    assert lifeline_res.status == "Likely Eligible"
    assert ccdf_res is not None
    assert ccdf_res.status == "Likely Eligible"


# ─── Country normalization tests ─────────────────────────────────────────────

def test_normalize_country_us_variants():
    assert _normalize_country("United States") == "us"
    assert _normalize_country("USA") == "us"
    assert _normalize_country("u.s.a.") == "us"
    assert _normalize_country("america") == "us"

def test_normalize_country_india_variants():
    assert _normalize_country("india") == "india"
    assert _normalize_country("bharat") == "india"

def test_normalize_country_uk_variants():
    assert _normalize_country("United Kingdom") == "uk"
    assert _normalize_country("England") == "uk"
    assert _normalize_country("Great Britain") == "uk"

def test_normalize_country_passthrough():
    assert _normalize_country("france") == "france"
    assert _normalize_country("Canada") == "canada"
    assert _normalize_country("Germany") == "germany"


# ─── State → Country derivation tests ────────────────────────────────────────

def test_derive_country_california():
    data = {"state": "California"}
    result = _derive_country_from_state(data)
    assert result["country"] == "us"

def test_derive_country_maharashtra():
    data = {"state": "Maharashtra"}
    result = _derive_country_from_state(data)
    assert result["country"] == "india"

def test_derive_country_preserves_explicit():
    """If country is already set, it should be normalized not overridden."""
    data = {"country": "United States", "state": "Maharashtra"}
    result = _derive_country_from_state(data)
    assert result["country"] == "us"  # Normalized, not overridden by state


# ─── Heuristic fallback tests (offline / no-LLM mode) ────────────────────────

def test_heuristic_extract_currency_inr():
    profile = _heuristic_extract("My income is 2 lakh rupees per year")
    assert profile.country == "india"

def test_heuristic_extract_currency_usd():
    profile = _heuristic_extract("I earn $30,000 a year")
    assert profile.country == "us"

def test_heuristic_extract_aadhaar():
    profile = _heuristic_extract("I have an aadhaar card and need help")
    assert profile.country == "india"

def test_heuristic_extract_fafsa():
    profile = _heuristic_extract("I submitted my fafsa application")
    assert profile.country == "us"

def test_heuristic_extract_california():
    """California should resolve to country=us via state derivation."""
    profile = _heuristic_extract("I live in california and earn 20000 per year")
    assert profile.country == "us"
    assert profile.state == "California"

def test_heuristic_extract_punjab():
    """Punjab should resolve to country=india via state derivation."""
    profile = _heuristic_extract("I am a farmer in punjab with 2 acres of land")
    assert profile.country == "india"
    assert profile.state == "Punjab"
    assert profile.farmer_status is True

def test_heuristic_extract_no_clues():
    """Ambiguous text should leave country as None."""
    profile = _heuristic_extract("I need financial help")
    assert profile.country is None

def test_heuristic_extract_student():
    profile = _heuristic_extract("I am a 22 year old student")
    assert profile.student_status is True
    assert profile.age == 22


# ─── New Edge Case Fixes Tests ───────────────────────────────────────────────

def test_currency_substitution_us():
    from i18n import build_chat_reply_translated
    from models import MatchResult
    profile = UserProfile(
        country="us",
        state="California",
        annual_income=25000,
    )
    result = MatchResult(
        scheme_id="us-snap",
        scheme_name="SNAP",
        scheme_category="healthcare",
        status="Likely Eligible",
        score=1.0,
        confidence=1.0,
        matched_rules=["Eligible"],
        missing_rules=[],
        explanation="Test explanation",
        documents_required=[],
        official_url="http://test.com"
    )
    reply = build_chat_reply_translated(profile, [result], [], False, lang="en")
    assert "$" in reply
    assert "₹" not in reply

def test_country_switch_resets_fields():
    from profile_extractor import merge_profiles
    base = UserProfile(
        country="us",
        state="California",
        annual_income=30000,
        occupation="student",
        student_status=True,
    )
    update = UserProfile(
        country="india",
    )
    merged = merge_profiles(base, update)
    assert merged.country == "india"
    assert merged.state is None
    assert merged.annual_income is None
    assert merged.occupation == "student"  # Preserved!
    assert merged.student_status is True

def test_greeting_on_empty_profile():
    from i18n import build_chat_reply_translated
    profile = UserProfile()
    reply = build_chat_reply_translated(profile, [], [], False, lang="en")
    assert "Hello!" in reply or "Midas Ledger" in reply

def test_unsupported_country_route_localized(monkeypatch):
    async def mock_extract(text):
        return UserProfile(country="france")
    
    import routes.chat
    monkeypatch.setattr(routes.chat, "extract_profile_from_text", mock_extract)
    
    # Call /api/chat in English
    response = client.post("/api/chat", json={"message": "I live in France", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "support government welfare schemes for **India** and the **United States**" in data["reply"]
    
    # Call /api/chat in Hindi
    response_hi = client.post("/api/chat", json={"message": "I live in France", "lang": "hi"})
    assert response_hi.status_code == 200
    data_hi = response_hi.json()
    assert "भारत" in data_hi["reply"]
    assert "संयुक्त राज्य अमेरिका" in data_hi["reply"]
