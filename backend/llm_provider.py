"""
LLM provider abstraction layer.
Primary: Google Gemini (gemini-3.5-flash) via official google-genai SDK.
Falls back to rule-based templates if API key not set or rate-limited.

DESIGN PRINCIPLE: Only ONE LLM call per user turn.
The single call extracts the profile AND generates the reply in one shot.
All scheme matching and explanation generation is purely rule-based.
"""
import os
import json
import logging
from typing import Optional
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Model details
MODEL_NAME = "gemini-3.5-flash"

# Shared client instance (created lazily)
_client: Optional[genai.Client] = None


def _get_client() -> Optional[genai.Client]:
    """Get or create the Gemini client. Returns None if no API key."""
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key in ("your_openrouter_api_key_here", "your_gemini_api_key_here"):
        logger.info("No Gemini API key configured — using rule-based fallback")
        return None

    _client = genai.Client(api_key=api_key)
    return _client


async def call_llm(prompt: str, temperature: float = 0.3) -> Optional[str]:
    """
    Call Gemini with a prompt. Returns the text response or None on any failure.
    """
    client = _get_client()
    if not client:
        return None

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=1024,
            )
        )
        return response.text.strip()

    except Exception as e:
        logger.error(f"Gemini LLM call failed: {e}")
        return None


# JSON schema for the user profile extraction — tells Gemini exactly what to return
PROFILE_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "age": types.Schema(type=types.Type.INTEGER, nullable=True),
        "state": types.Schema(type=types.Type.STRING, nullable=True),
        "district": types.Schema(type=types.Type.STRING, nullable=True),
        "occupation": types.Schema(type=types.Type.STRING, nullable=True),
        "annual_income": types.Schema(type=types.Type.INTEGER, nullable=True),
        "category": types.Schema(type=types.Type.STRING, nullable=True),
        "student_status": types.Schema(type=types.Type.BOOLEAN, nullable=True),
        "farmer_status": types.Schema(type=types.Type.BOOLEAN, nullable=True),
        "housing_status": types.Schema(type=types.Type.STRING, nullable=True),
        "land_ownership": types.Schema(type=types.Type.BOOLEAN, nullable=True),
        "disability_status": types.Schema(type=types.Type.BOOLEAN, nullable=True),
        "senior_citizen_status": types.Schema(type=types.Type.BOOLEAN, nullable=True),
        "gender": types.Schema(type=types.Type.STRING, nullable=True),
        "bpl_card": types.Schema(type=types.Type.BOOLEAN, nullable=True),
        "ration_card": types.Schema(type=types.Type.STRING, nullable=True),
    },
)


async def call_llm_json(prompt: str, schema: Optional[types.Schema] = None) -> Optional[dict]:
    """
    Call the LLM and parse JSON from the response.
    Uses Gemini's native JSON response mode for guaranteed valid JSON output.
    When a schema is provided, uses response_schema for structured output.
    """
    client = _get_client()
    if not client:
        return None

    try:
        config_kwargs = {
            "temperature": 0.1,
            "max_output_tokens": 2048,
            "response_mime_type": "application/json",
        }
        if schema:
            config_kwargs["response_schema"] = schema

        response = await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        raw = response.text.strip()
        return json.loads(raw)

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {e}\nRaw: {raw[:500]}")
        return None
    except Exception as e:
        logger.error(f"Gemini JSON LLM call failed: {e}")
        return None

