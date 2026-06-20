"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import type { ChatMessage, ChatResponse, MatchResult, UserProfile } from "./types";

interface ChatState {
  messages: ChatMessage[];
  recommendations: MatchResult[];
  profile: UserProfile | null;
  isLoading: boolean;
}

interface ChatContextValue extends ChatState {
  addUserMessage: (text: string) => void;
  addAssistantMessage: (text: string) => void;
  setMessages: (msgs: ChatMessage[]) => void;
  handleResponse: (response: ChatResponse) => void;
  setIsLoading: (v: boolean) => void;
  clearChat: () => void;
}

const STORAGE_KEY = "benefitor-chat-state";

const ChatContext = createContext<ChatContextValue | null>(null);

function saveToSession(state: Omit<ChatState, "isLoading">) {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // Storage full or unavailable — silently ignore
  }
}

function loadFromSession(): Omit<ChatState, "isLoading"> | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessagesRaw] = useState<ChatMessage[]>([]);
  const [recommendations, setRecommendations] = useState<MatchResult[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  // Restore state from sessionStorage on mount
  useEffect(() => {
    const saved = loadFromSession();
    if (saved) {
      setMessagesRaw(saved.messages || []);
      setRecommendations(saved.recommendations || []);
      setProfile(saved.profile || null);
    }
    setHydrated(true);
  }, []);

  // Persist to sessionStorage whenever state changes (after hydration)
  useEffect(() => {
    if (!hydrated) return;
    saveToSession({ messages, recommendations, profile });
  }, [messages, recommendations, profile, hydrated]);

  const setMessages = useCallback((msgs: ChatMessage[]) => {
    setMessagesRaw(msgs);
  }, []);

  const addUserMessage = useCallback((text: string) => {
    setMessagesRaw((prev) => [...prev, { role: "user", content: text }]);
  }, []);

  const addAssistantMessage = useCallback((text: string) => {
    setMessagesRaw((prev) => [...prev, { role: "assistant", content: text }]);
  }, []);

  const handleResponse = useCallback((response: ChatResponse) => {
    if (response.recommendations.length > 0) {
      setRecommendations(response.recommendations);
    }
    if (response.profile) {
      setProfile(response.profile);
    }
  }, []);

  const clearChat = useCallback(() => {
    setMessagesRaw([]);
    setRecommendations([]);
    setProfile(null);
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch {}
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        recommendations,
        profile,
        isLoading,
        addUserMessage,
        addAssistantMessage,
        setMessages,
        handleResponse,
        setIsLoading,
        clearChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error("useChat must be used within a ChatProvider");
  return ctx;
}
