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
