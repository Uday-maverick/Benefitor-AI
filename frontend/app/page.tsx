"use client";

import ChatInterface from "@/components/ChatInterface";
import ResultsPanel from "@/components/ResultsPanel";
import LanguagePicker from "@/components/LanguagePicker";
import { useLang } from "@/lib/LanguageContext";
import { useChat } from "@/lib/ChatContext";
import { t } from "@/lib/i18n";
import Link from "next/link";
import { LayoutList, RotateCcw } from "lucide-react";

export default function Home() {
  const { lang } = useLang();
  const tr = t(lang);
  const { recommendations, profile, isLoading, handleResponse, setIsLoading, clearChat, messages } =
    useChat();

  return (
    <div
      className="h-svh flex flex-col"
      style={{ background: "hsl(var(--bg))" }}
    >
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <header
        className="flex-shrink-0 px-5 h-14 flex items-center justify-between"
        style={{
          borderBottom: "1.5px solid hsl(var(--border))",
          background: "hsl(var(--s1))",
          boxShadow: "var(--shadow-sm)",
        }}
      >
        {/* Brand */}
        <div className="flex items-center gap-2.5">
          <div
            className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
            style={{ background: "hsl(var(--blue))" }}
          >
            <svg width="16" height="16" viewBox="0 0 14 14" fill="none">
              <path
                d="M7 1L9 5.5L14 6.18L10.5 9.59L11.38 14L7 11.77L2.62 14L3.5 9.59L0 6.18L5 5.5L7 1Z"
                fill="white"
              />
            </svg>
          </div>
          <div>
            <span
              className="font-bold text-base"
              style={{ color: "hsl(var(--tx))", letterSpacing: "-0.015em" }}
            >
              Benefitor AI
            </span>
            <span
              className="hidden sm:inline text-xs ml-2 px-2 py-0.5 rounded-full"
              style={{
                background: "hsl(var(--blue) / 0.10)",
                color: "hsl(var(--blue))",
                fontWeight: 500,
              }}
            >
              {tr.tagline}
            </span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="nav-link flex items-center gap-1.5"
              title="Start a new conversation"
            >
              <RotateCcw size={15} />
              <span className="hidden sm:inline">{tr.newChat}</span>
            </button>
          )}
          <Link href="/schemes" className="nav-link flex items-center gap-1.5">
            <LayoutList size={15} />
            <span className="hidden sm:inline">{tr.browseSchemes}</span>
          </Link>
          <LanguagePicker />
          <span
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full text-xs font-semibold"
            style={{
              background: "hsl(var(--green) / 0.10)",
              border: "1.5px solid hsl(var(--green) / 0.25)",
              color: "hsl(var(--green))",
            }}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
            {tr.live}
          </span>
        </nav>
      </header>

      {/* ── Main split ─────────────────────────────────────────────────── */}
      <main className="flex-1 flex overflow-hidden min-h-0">
        {/* Chat */}
        <div
          className="flex-1 flex flex-col min-w-0"
          style={{ borderRight: "1.5px solid hsl(var(--border))" }}
        >
          <ChatInterface
            onResponse={handleResponse}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        </div>

        {/* Results sidebar */}
        <div
          className="flex-shrink-0 flex flex-col overflow-hidden"
          style={{ width: "390px" }}
        >
          <ResultsPanel
            recommendations={recommendations}
            profile={profile}
            isLoading={isLoading}
          />
        </div>
      </main>
    </div>
  );
}

