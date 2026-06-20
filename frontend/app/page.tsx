"use client";

import { useState } from "react";
import ChatInterface from "@/components/ChatInterface";
import ResultsPanel from "@/components/ResultsPanel";
import LanguagePicker from "@/components/LanguagePicker";
import { useLang } from "@/lib/LanguageContext";
import { useChat } from "@/lib/ChatContext";
import { t } from "@/lib/i18n";
import Link from "next/link";
import { LayoutList, RotateCcw } from "lucide-react";

const TAB_TRANSLATIONS: Record<string, { chat: string; results: string }> = {
  en: { chat: "Chat", results: "Results" },
  hi: { chat: "बातचीत", results: "परिणाम" },
  bn: { chat: "চ্যাট", results: "ফলাফল" },
  ta: { chat: "உரையாடல்", results: "முடிவுகள்" },
  te: { chat: "చాట్", results: "ఫలితాలు" },
  mr: { chat: "संभाषण", results: "निकाल" },
  gu: { chat: "વાતચીत", results: "પરિણામો" },
  pa: { chat: "ਗੱਲਬਾਤ", results: "ਨਤੀਜੇ" },
};

export default function Home() {
  const { lang } = useLang();
  const tr = t(lang);
  const { recommendations, profile, isLoading, handleResponse, setIsLoading, clearChat, messages } =
    useChat();
  const [activeTab, setActiveTab] = useState<"chat" | "results">("chat");

  const tabs = TAB_TRANSLATIONS[lang] || TAB_TRANSLATIONS.en;

  const handleResponseWithTabSwitch = (response: any) => {
    handleResponse(response);
    // Switch to results tab on mobile screen when schemes are matched
    if (response.recommendations && response.recommendations.length > 0) {
      setActiveTab("results");
    }
  };

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
              onClick={() => {
                clearChat();
                setActiveTab("chat");
              }}
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

      {/* Mobile Tab Toggle Bar */}
      <div
        className="flex-shrink-0 flex md:hidden"
        style={{
          borderBottom: "1.5px solid hsl(var(--border))",
          background: "hsl(var(--s1))",
        }}
      >
        <button
          onClick={() => setActiveTab("chat")}
          className="flex-1 py-3 text-center text-sm font-semibold transition-all border-b-2"
          style={{
            borderColor: activeTab === "chat" ? "hsl(var(--blue))" : "transparent",
            color: activeTab === "chat" ? "hsl(var(--blue))" : "hsl(var(--tx-2))",
          }}
        >
          {tabs.chat}
        </button>
        <button
          onClick={() => setActiveTab("results")}
          className="flex-1 py-3 text-center text-sm font-semibold transition-all border-b-2 relative"
          style={{
            borderColor: activeTab === "results" ? "hsl(var(--blue))" : "transparent",
            color: activeTab === "results" ? "hsl(var(--blue))" : "hsl(var(--tx-2))",
          }}
        >
          {tabs.results}
          {recommendations.length > 0 && (
            <span
              className="absolute top-2.5 right-6 w-4.5 h-4.5 rounded-full flex items-center justify-center text-[10px] font-bold text-white bg-current"
              style={{
                background: "hsl(var(--blue))",
                color: "white",
              }}
            >
              {recommendations.length}
            </span>
          )}
        </button>
      </div>

      {/* ── Main split ─────────────────────────────────────────────────── */}
      <main className="flex-1 flex overflow-hidden min-h-0">
        {/* Chat */}
        <div
          className={`flex-1 flex-col min-w-0 ${
            activeTab === "chat" ? "flex" : "hidden md:flex"
          }`}
          style={{
            borderRight: "1.5px solid hsl(var(--border))",
          }}
        >
          <ChatInterface
            onResponse={handleResponseWithTabSwitch}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        </div>

        {/* Results sidebar */}
        <div
          className={`flex-shrink-0 flex-col overflow-hidden ${
            activeTab === "results" ? "flex w-full" : "hidden md:flex md:w-[390px]"
          }`}
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

