# Midas Ledger - Benefitor AI 🇮🇳

> Explainable AI Welfare Benefits Navigator for Indian Citizens — Built for Social Impact.

Midas Ledger - Benefitor AI helps citizens discover government welfare schemes they may qualify for through simple, natural conversations. By combining Large Language Models (LLMs) with a deterministic, rule-based eligibility engine, Midas Ledger - Benefitor AI delivers clear, trustworthy, and explainable benefit recommendations in 8 Indian languages.

---

## 🏗️ AI & Systems Architecture

### 1. Hybrid AI Architecture
Midas Ledger - Benefitor AI utilizes a **Hybrid AI Architecture** split into distinct execution layers to ensure both conversational intelligence and absolute rule safety:
* **Conversational Parsing (LLM Layer):** Uses Google Gemini (`gemini-3.5-flash` via the official `google-genai` SDK) to parse free-text natural language queries into a structured `UserProfile` object (e.g. extracting age, income, state, student status, housing type).
* **Deterministic Matching (Eligibility Engine):** A rule-based evaluation engine written in Python matching the user profile against simulated government criteria. This eliminates LLM hallucination in determining eligibility.
* **Explanation Generation (Empathetic AI):** When enabled by an API key, Gemini transforms raw match criteria scores and missing guidelines into contextualized, localized, and empathetic explanations and step-by-step application instructions.

```
       User Text Query (Natural Conversation)
                 │
                 ▼
     ┌────────────────────────┐
     │  Gemini 3.5 Flash LLM  │ ◄─── (Single-Turn API Budget Constraint)
     └───────────┬────────────┘
                 │ (Structured UserProfile JSON)
                 ▼
     ┌────────────────────────┐
     │ Deterministic Engine   │ ◄─── (100% Hallucination-Free Python Rules)
     └───────────┬────────────┘
                 │ (Scored Matches & Rule Audits)
                 ▼
     ┌────────────────────────┐
     │ Explanation Generator  │ ◄─── (Contextualized translation and next steps)
     └───────────┬────────────┘
                 │
                 ▼
   Empathetic Multilingual UI (Next.js 16 + Tailwind CSS)
```

### 2. Single-Turn API Design
To run efficiently and stay within free-tier API boundaries, the system makes **exactly one LLM call per user turn** for profile extraction. All scheme matching, translations, and chat responses leverage efficient template heuristics and deterministic rules unless explicitly generating full-text AI evaluations.

---

## 🛡️ Responsible AI & Privacy Guardrails

* **Hallucination Prevention:** The actual matching logic is entirely deterministic. The AI is restricted to structuring raw inputs and explaining results. It is impossible for the system to hallucinate an unauthorized scheme or falsify eligibility parameters.
* **Empathetic Explanations & Disclaimers:** All recommendations clearly use non-guarantee language ("May qualify", "Potentially eligible") and append a prominent warning that final approval lies solely with official government verification bodies.
* **Stateless Data Privacy (Zero PII):** We collect no Personally Identifiable Information (PII) like names, Aadhaar numbers, or contact details. All profile parameters (e.g. BPL status, income) are processed completely statelessly in-memory and are stored only in the user's browser `sessionStorage` to persist conversation history.

---

## 🛠️ Tools & Data Disclosure

* **AI Coding Assistants:** Built with pair-programming assistance from the Google DeepMind Antigravity IDE (utilizing Gemini 3.5 Flash).
* **Open-Source Libraries/Frameworks:**
  * **Frontend:** Next.js 16, React 19, Tailwind CSS 4, Lucide Icons, TypeScript.
  * **Backend:** FastAPI, Uvicorn, Pydantic 2, google-genai SDK, HTTPX, Pytest.
* **Data & Attribution:**
  * **Welfare Schemes Database:** Criteria for the 5 MVP schemes are simulated based on public guidelines from official government sites (e.g. [PM-KISAN](https://pmkisan.gov.in/), [PMAY](https://pmaymis.gov.in/), [Ayushman Bharat PM-JAY](https://pmjay.gov.in/), [NSAP](https://nsap.nic.in/), and [NSP](https://scholarships.gov.in/)).
  * **Synthetic Data:** The unit testing suite generates synthetic in-memory profiles to test engine correctness under extreme values. No personal or proprietary datasets were used.

---

## 🚀 Quick Start & Deployment Setup

### 1. Backend Setup (FastAPI)
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create your .env file
# Edit the file to supply your Google Gemini API Key
# (Get a free key from Google AI Studio: https://aistudio.google.com/)
cp .env.example .env  # or create a .env file directly

# Run backend development server
uvicorn main:app --reload --port 8000
```
* **API Documentation:** `http://localhost:8000/docs`
* **Test Suite:** Run backend tests with `pytest`

### 2. Frontend Setup (Next.js 16)
```bash
cd frontend

# Install packages
npm install

# Start development server
npm run dev
```
* **Web App URL:** `http://localhost:3000`
* **Production Build:** Build the optimized production bundle with `npm run build`

---

## 🔑 Environment Variables Configuration

### Backend (`backend/.env`)
```env
# Gemini API Key (Get a free API key from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Provider Configuration
LLM_PROVIDER=gemini
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📁 Project Structure

```
MVP/
├── .gitignore               # Root gitignore excluding dependencies and keys
├── PRD.md                   # Product Requirements Document
├── README.md                # Submission details and documentation
├── backend/
│   ├── main.py              # FastAPI application root
│   ├── models.py            # Pydantic data schemas
│   ├── schemes_db.py        # Welfare scheme parameters
│   ├── eligibility_engine.py # Rule matching evaluation logic
│   ├── llm_provider.py      # Google GenAI client integration
│   ├── profile_extractor.py # Gemini profile extractor
│   ├── i18n.py              # Backend multilingual mappings
│   ├── requirements.txt     # Python packages list
│   └── test_main.py         # Pytest coverage testing suite
└── frontend/
    ├── app/
    │   ├── page.tsx         # Chat interface dashboard
    │   ├── schemes/
    │   │   ├── page.tsx     # Browse all schemes
    │   │   └── [id]/page.tsx # Scheme detail dashboard
    │   ├── layout.tsx       # Core styling provider
    │   └── globals.css      # Vanilla CSS styling custom rules
    ├── components/          # Reusable Next.js components
    ├── lib/                 # Next.js helpers (api, i18n, types, context)
    └── package.json         # Package configuration scripts
```

---

## 🌐 Covered Schemes (MVP)

| Scheme | Category | Primary Benefit |
| :--- | :--- | :--- |
| **PM-KISAN** | Farmer Support | ₹6,000 / year income support |
| **PMAY** | Housing | Up to ₹2.5 Lakh subsidy for home construction |
| **Ayushman Bharat** | Healthcare | ₹5 Lakh / year cashless family health cover |
| **NSAP** | Pension | ₹200 - ₹500 / month old age/widow pension |
| **NSP Scholar** | Education | ₹1,200 - ₹20,000+ / year academic scholarship |

---

## 🧪 Quick Test Demo Flow

1. Navigate to the Home screen (`http://localhost:3000`).
2. Input a query: *"I am a second-year college student from Maharashtra. My family's yearly income is 1.2 lakhs."*
3. Verify that the AI extracts the profile fields correctly on the right.
4. Click on any matched scheme card to view the eligibility score details, required documents list, and official portal links.
5. Choose from 8 languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Punjabi, or English) to instantly translate all scheme details and conversation replies.
6. Click **New Chat** (🔄) to reset the session storage and start a fresh profile.
