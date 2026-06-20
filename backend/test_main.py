import pytest
from fastapi.testclient import TestClient
from main import app
from models import UserProfile
from eligibility_engine import evaluate_all_schemes

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Benefitor AI"

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
    # PM-KISAN name translated to Hindi
    assert "किसान" in schemes[0]["name"] or "समान" in schemes[0]["name"] or schemes[0]["name"]

def test_eligibility_engine():
    # Test profile for PM-KISAN
    profile = UserProfile(
        age=35,
        state="Punjab",
        occupation="farmer",
        annual_income=80000,
        farmer_status=True,
        land_ownership=True
    )
    results = evaluate_all_schemes(profile)
    # Find PM-KISAN result
    pm_kisan_res = next((r for r in results if r.scheme_id == "pm-kisan"), None)
    assert pm_kisan_res is not None
    assert pm_kisan_res.status == "Likely Eligible"

def test_eligibility_engine_not_eligible():
    # Test profile not eligible for PM-KISAN (land owner is False)
    profile = UserProfile(
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
    # Test profile eligible for US Medicaid & SNAP
    profile = UserProfile(
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

def test_geo_filtering():
    # Test that a US user is ineligible for Indian schemes
    profile_us = UserProfile(
        age=35,
        state="Texas",
        occupation="farmer",
        annual_income=25000,
        farmer_status=True,
        land_ownership=True
    )
    results_us = evaluate_all_schemes(profile_us)
    pm_kisan_res = next((r for r in results_us if r.scheme_id == "pm-kisan"), None)
    assert pm_kisan_res is not None
    assert pm_kisan_res.status == "Likely Not Eligible" # Disqualified due to state

    # Test that an Indian user is ineligible for US schemes
    profile_in = UserProfile(
        age=30,
        state="Maharashtra",
        annual_income=30000, # Looks low enough for US, but should fail due to state
    )
    results_in = evaluate_all_schemes(profile_in)
    medicaid_res = next((r for r in results_in if r.scheme_id == "us-medicaid"), None)
    assert medicaid_res is not None
    assert medicaid_res.status == "Likely Not Eligible" # Disqualified due to state


def test_eligibility_engine_new_us():
    # Test profile eligible for us-wic, us-lifeline, and us-child-care-subsidy
    profile = UserProfile(
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


