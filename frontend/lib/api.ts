// API client for Benefitor AI backend

import type { ChatMessage, ChatResponse, Scheme, UserProfile, MatchResult } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// ─── Chat ─────────────────────────────────────────────────────────────────────

export async function sendChatMessage(
  message: string,
  history: ChatMessage[],
  lang: string = "en"
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_history: history, lang }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Chat API error ${res.status}: ${err}`);
  }

  return res.json() as Promise<ChatResponse>;
}

// ─── Schemes ──────────────────────────────────────────────────────────────────

export async function fetchSchemes(lang: string = "en"): Promise<Scheme[]> {
  const res = await fetch(`${API_BASE}/api/schemes?lang=${lang}`);
  if (!res.ok) throw new Error(`Schemes API error ${res.status}`);
  return res.json() as Promise<Scheme[]>;
}

export async function fetchScheme(id: string, lang: string = "en"): Promise<Scheme> {
  const res = await fetch(`${API_BASE}/api/schemes/${id}?lang=${lang}`);
  if (!res.ok) throw new Error(`Scheme ${id} not found`);
  return res.json() as Promise<Scheme>;
}

// ─── Evaluation ───────────────────────────────────────────────────────────────

export async function evaluateProfile(profile: UserProfile, lang: string = "en"): Promise<MatchResult[]> {
  const res = await fetch(`${API_BASE}/api/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ profile, lang }),
  });
  if (!res.ok) throw new Error(`Evaluate API error ${res.status}`);
  return res.json() as Promise<MatchResult[]>;
}

