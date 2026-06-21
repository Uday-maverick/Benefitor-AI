"""
Midas Ledger - Benefitor AI — FastAPI Application Entry Point
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Import routes
from routes.chat import router as chat_router
from routes.schemes import router as schemes_router
from routes.evaluate import router as evaluate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup / shutdown events."""
    llm_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not llm_key or llm_key in ("your_openrouter_api_key_here", "your_gemini_api_key_here"):
        logger.warning(
            "⚠️  GEMINI_API_KEY not set — running in rule-based fallback mode. "
            "Add your key to backend/.env to enable AI explanations."
        )
    else:
        logger.info("✅ Gemini API key detected — AI explanations enabled.")
    yield
    logger.info("Midas Ledger - Benefitor AI backend shutting down.")


# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Midas Ledger - Benefitor AI API",
    description="Explainable AI welfare benefits navigator for Indian citizens",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Next.js and any client (stateless API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ───────────────────────────────────────────────────────────────────
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(schemes_router, prefix="/api", tags=["Schemes"])
app.include_router(evaluate_router, prefix="/api", tags=["Evaluation"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "service": "Midas Ledger - Benefitor AI",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
