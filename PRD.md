# Benefitor AI

## Product Requirements Document (PRD)

**Version:** 1.0
**Project Type:** AI for Social Impact
**Target Audience:** Hackathon Judges, Developers, Product Teams
**Status:** MVP Definition

---

# Executive Summary

Benefitor AI is an explainable AI-powered welfare benefits navigator designed to help Indian citizens discover government schemes they may be eligible for through natural language conversations.

Instead of forcing users to search through government portals, PDFs, and complex eligibility rules, Benefitor AI understands a user's situation, evaluates welfare schemes against their profile, explains why they may qualify, and guides them through the application process.

The system combines Large Language Models (LLMs), rule-based reasoning, and explainable recommendations to create a trustworthy and accessible welfare assistant.

---

# Problem Statement

Millions of Indians remain unaware of welfare schemes that could significantly improve their lives.

Current challenges include:

* Welfare information is scattered across multiple government portals.
* Eligibility criteria are difficult to understand.
* Rules are buried inside lengthy PDFs.
* Citizens often miss opportunities because they do not know which schemes apply to them.
* NGOs and caseworkers spend significant time answering repetitive eligibility questions.

The gap is not access to information alone—it is understanding, interpretation, and guidance.

---

# Vision

Create an AI-powered welfare assistant that:

* Understands citizens through natural conversation.
* Determines which schemes may be relevant.
* Explains eligibility clearly.
* Identifies missing information.
* Provides actionable next steps.
* Maintains transparency and trust.

---

# Goals

## Primary Goals

* Simplify welfare scheme discovery.
* Increase awareness of government benefits.
* Provide explainable recommendations.
* Reduce information barriers.

## Secondary Goals

* Support NGOs and social workers.
* Improve accessibility.
* Demonstrate responsible AI usage.
* Create a scalable foundation for future government integrations.

---

# Non-Goals

The MVP will NOT:

* Submit applications on behalf of users.
* Access Aadhaar services.
* Make final eligibility decisions.
* Replace government verification processes.
* Cover all Indian welfare schemes.

---

# Target Users

## Students

Seeking:

* Scholarships
* Financial assistance
* Educational support

## Farmers

Seeking:

* Agricultural subsidies
* Income support
* Insurance schemes

## Low-Income Families

Seeking:

* Healthcare assistance
* Housing benefits
* Food security schemes

## Senior Citizens

Seeking:

* Pension programs
* Social support benefits

## NGOs & Social Workers

Seeking:

* Faster welfare assessment
* Benefit discovery support

---

# MVP Scope

## Included Schemes

### PM-KISAN

Farmer income support.

### PMAY

Housing assistance.

### Ayushman Bharat

Healthcare support.

### NSAP

Social pension schemes.

### National Scholarship Portal Programs

Student-focused benefits.

---

# Core User Journey

## Step 1: User Describes Situation

Example:

> I am a second-year engineering student from West Bengal. My family income is around ₹1.5 lakh per year. My father is a farmer.

---

## Step 2: AI Extracts Structured Profile

Example:

```json
{
  "state": "West Bengal",
  "occupation": "Student",
  "annual_income": 150000,
  "farmer_family": true
}
```

---

## Step 3: Missing Information Detection

If important fields are missing:

Example:

> Do you belong to a reserved category?

Only one focused follow-up question should be asked at a time.

---

## Step 4: Eligibility Evaluation

The system evaluates all schemes.

Outputs:

* Likely Eligible
* Possibly Eligible
* Likely Not Eligible

---

## Step 5: Explainable Results

Example:

> You may qualify for the National Scholarship Program because your family income falls below the specified threshold and you are currently enrolled in higher education.

---

## Step 6: Application Guidance

Provide:

* Required documents
* Application links
* Missing requirements
* Suggested next steps

---

# AI Architecture

The system uses a Hybrid AI Architecture.

## Layer 1: Conversational Understanding

### Purpose

Convert free-form user text into structured data.

### Technology

* GPT
* Claude
* Gemini

### Output

Structured JSON profile.

---

## Layer 2: Rule-Based Eligibility Engine

### Purpose

Perform deterministic eligibility evaluation.

### Benefits

* Explainable
* Reliable
* Auditable
* Less hallucination risk

---

## Layer 3: Explanation Generator

### Purpose

Convert structured results into human-readable recommendations.

Example:

> Based on the information provided, you may qualify for PM-KISAN because your household is engaged in farming activities.

---

# System Architecture

```text
User
 │
 ▼
Frontend (Next.js)
 │
 ▼
FastAPI Backend
 │
 ├───────────────┐
 │               │
 ▼               ▼
Profile       Scheme
Extraction    Knowledge Base
 │               │
 └──────┬────────┘
        ▼
Eligibility Engine
        │
        ▼
Explanation Engine
        │
        ▼
Results Dashboard
```

---

# Technical Architecture

## Frontend

### Framework

* Next.js 15
* React
* TypeScript

### UI

* TailwindCSS
* shadcn/ui
* Lucide Icons

---

## Backend

### Framework

* FastAPI

### Validation

* Pydantic

### API Layer

* REST APIs

---

## Database

### MVP

* SQLite

### Production

* PostgreSQL

---

## AI Layer

Provider abstraction:

```python
LLMProvider
 ├─ OpenAI
 ├─ Claude
 └─ Gemini
```

Allows switching models without changing business logic.

---

# Data Models

## UserProfile

```python
class UserProfile:
    age: int
    state: str
    district: str
    occupation: str
    annual_income: float
    category: str
    student_status: bool
    farmer_status: bool
    housing_status: str
    land_ownership: bool
    disability_status: bool
    senior_citizen_status: bool
```

---

## Scheme

```python
class Scheme:
    id: str
    name: str
    category: str
    summary: str
    eligibility_rules: list
    documents_required: list
    official_url: str
```

---

## MatchResult

```python
class MatchResult:
    scheme_id: str
    status: str
    score: float
    confidence: float
    matched_rules: list
    missing_rules: list
    explanation: str
```

---

# API Specification

## POST /api/chat

Purpose:

* Main conversation endpoint.

Input:

```json
{
  "message": "I am a student..."
}
```

Output:

```json
{
  "profile": {},
  "follow_up_question": null,
  "recommendations": []
}
```

---

## POST /api/extract-profile

Returns structured profile.

---

## POST /api/evaluate

Evaluates profile against scheme rules.

---

## GET /api/schemes

Returns all schemes.

---

## GET /api/schemes/{id}

Returns scheme details.

---

# Recommendation Engine

Scoring Factors:

| Factor                   | Weight          |
| ------------------------ | --------------- |
| Eligibility Match        | High            |
| Income Match             | High            |
| Occupation Match         | Medium          |
| State Match              | Medium          |
| Missing Information      | Negative        |
| Disqualifying Conditions | Strong Negative |

---

# Trust & Safety

The system must never:

* Claim approval.
* Guarantee eligibility.
* Provide legal certainty.

Allowed wording:

* May qualify
* Appears eligible
* Potentially eligible

Required disclaimer:

> This recommendation is based on available information and does not guarantee approval. Final decisions are made by the relevant government authority.

---

# User Interface Requirements

## Home Page

Contains:

* Hero section
* Chat interface
* Quick examples

---

## Results Panel

Displays:

* Top schemes
* Eligibility score
* Confidence score
* Short explanation

---

## Scheme Details Page

Displays:

* Overview
* Eligibility rules
* Required documents
* Application link
* Explanation

---

# Future Roadmap

## Phase 2

* Voice interactions
* Regional language support
* OCR document analysis
* State-specific schemes

---

## Phase 3

* NGO dashboard
* Caseworker tools
* Analytics platform
* Application progress tracking

---

# Success Metrics

## Technical

* Profile extraction accuracy > 90%
* API latency < 3 seconds
* Recommendation generation < 5 seconds

## Product

* User receives relevant schemes in one interaction
* User understands why recommendations were made
* User receives actionable next steps

---

# Demo Flow

1. Open Benefitor AI.
2. Enter user situation.
3. AI extracts profile.
4. AI asks missing question if required.
5. Eligibility engine evaluates schemes.
6. Recommendations appear.
7. Open scheme details.
8. Show explanation and required documents.
9. Demonstrate official application links.

---

# Hackathon Value Proposition

Benefitor AI is not a search engine.

It is an explainable welfare intelligence system that:

* Understands users through conversation.
* Interprets eligibility rules.
* Explains recommendations.
* Bridges the gap between citizens and government benefits.

By combining LLMs, deterministic reasoning, and explainable AI, Benefitor AI makes public welfare programs more accessible, transparent, and actionable for millions of citizens.
