"""
GET /api/schemes — returns all schemes
GET /api/schemes/{id} — returns a single scheme
"""
from fastapi import APIRouter, HTTPException
from models import Scheme
from schemes_db import SCHEMES, SCHEMES_BY_ID
from i18n import translate_scheme

router = APIRouter()


@router.get("/schemes", response_model=list[Scheme])
async def list_schemes(lang: str = "en"):
    """Return all available schemes."""
    if lang == "en":
        return SCHEMES
    return [translate_scheme(s, lang) for s in SCHEMES]


@router.get("/schemes/{scheme_id}", response_model=Scheme)
async def get_scheme(scheme_id: str, lang: str = "en"):
    """Return a single scheme by ID."""
    scheme = SCHEMES_BY_ID.get(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme '{scheme_id}' not found")
    if lang == "en":
        return scheme
    return translate_scheme(scheme, lang)

