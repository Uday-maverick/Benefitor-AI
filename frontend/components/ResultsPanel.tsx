"use client";

import { useState } from "react";
import type { MatchResult, UserProfile } from "@/lib/types";
import SchemeCard from "./SchemeCard";
import ProfileSummary from "./ProfileSummary";
import { CheckCircle2, HelpCircle, XCircle, LayoutList, AlertTriangle } from "lucide-react";
import { useLang } from "@/lib/LanguageContext";
import { t, tExtra } from "@/lib/i18n";

interface ResultsPanelProps {
  recommendations: MatchResult[];
  profile: UserProfile | null;
  isLoading: boolean;
}

type FilterType = "all" | "eligible" | "possibly" | "not-eligible";

const FILTER_TABS: { key: FilterType; label: string; icon: React.ReactNode }[] = [
  { key: "all", label: "All", icon: null },
  { key: "eligible", label: "Eligible", icon: <CheckCircle2 size={11} /> },
  { key: "possibly", label: "Possible", icon: <HelpCircle size={11} /> },
  { key: "not-eligible", label: "Not eligible", icon: <XCircle size={11} /> },
];

export default function ResultsPanel({ recommendations, profile, isLoading }: ResultsPanelProps) {
  const { lang } = useLang();
  const tr = t(lang);
  const trEx = tExtra(lang);
  const [filter, setFilter] = useState<FilterType>("all");
  const [showProfile, setShowProfile] = useState(true);

  const filtered = recommendations.filter((r) => {
    if (filter === "eligible") return r.status === "Likely Eligible";
    if (filter === "possibly") return r.status === "Possibly Eligible";
    if (filter === "not-eligible") return r.status === "Likely Not Eligible";
    return true;
  });

  const eligibleCount = recommendations.filter((r) => r.status === "Likely Eligible").length;
  const possiblyCount = recommendations.filter((r) => r.status === "Possibly Eligible").length;

  const FILTER_TABS: { key: FilterType; label: string; icon: React.ReactNode }[] = [
    { key: "all", label: tr.allSchemes ?? "All", icon: null },
    { key: "eligible", label: tr.eligible, icon: <CheckCircle2 size={11} /> },
    { key: "possibly", label: tr.possiblyEligible, icon: <HelpCircle size={11} /> },
    { key: "not-eligible", label: tr.notEligible, icon: <XCircle size={11} /> },
  ];

  if (isLoading) {
    return (
      <div className="h-full flex flex-col p-4 gap-3">
        <div className="shimmer h-5 w-40 rounded-lg" />
        <div className="shimmer h-3.5 w-28 rounded-lg" />
        {[1, 2, 3].map((i) => (
          <div key={i} className="shimmer h-36 rounded-xl" />
        ))}
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center" style={{ background: "hsl(var(--bg))" }}>
        <div
          className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
          style={{ background: "hsl(var(--s2))" }}
        >
          <LayoutList size={26} style={{ color: "hsl(var(--tx-3))" }} />
        </div>
        <p className="text-base font-semibold mb-1" style={{ color: "hsl(var(--tx))" }}>
          {tr.resultsEmpty}
        </p>
        <p className="text-sm max-w-52 leading-relaxed" style={{ color: "hsl(var(--tx-3))" }}>
          {tr.resultsEmptySubtext}
        </p>
        <dl className="grid grid-cols-3 gap-2 mt-8 w-full max-w-xs text-center">
          {[
            { label: tr.statsSchemes, value: "5+" },
            { label: tr.statsResultsIn, value: "<5s" },
            { label: tr.statsExplain, value: "100%" },
          ].map((s) => (
            <div key={s.label} className="card p-3">
              <dt className="text-lg font-bold tabular" style={{ color: "hsl(var(--tx))", letterSpacing: "-0.02em" }}>
                {s.value}
              </dt>
              <dd className="text-xs mt-0.5" style={{ color: "hsl(var(--tx-3))" }}>
                {s.label}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col overflow-hidden" style={{ background: "hsl(var(--bg))" }}>
      {/* Header */}
      <div className="px-4 pt-4 pb-3" style={{ borderBottom: "1.5px solid hsl(var(--border))", background: "hsl(var(--s1))" }}>
        <div className="flex items-baseline justify-between mb-3">
          <div>
            <h2 className="text-sm font-bold" style={{ color: "hsl(var(--tx))" }}>
              {tr.resultsTitle}
            </h2>
            <p className="text-xs mt-0.5" style={{ color: "hsl(var(--tx-3))" }}>
              {eligibleCount} {tr.eligible.toLowerCase()} · {possiblyCount} {tr.possiblyEligible.toLowerCase()}
            </p>
          </div>
          <span
            className="chip tabular"
            style={{ background: "hsl(var(--s2))", color: "hsl(var(--tx-2))", border: "1px solid hsl(var(--border))" }}
          >
            {recommendations.length}
          </span>
        </div>

        {/* Filter tabs */}
        <div className="flex gap-1">
          {FILTER_TABS.map((tab) => {
            const active = filter === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key)}
                className="btn flex items-center gap-1"
                style={{
                  padding: "4px 10px",
                  borderRadius: "6px",
                  fontSize: "0.75rem",
                  ...(active
                    ? {
                        background: "hsl(var(--blue) / 0.12)",
                        border: "1px solid hsl(var(--blue) / 0.35)",
                        color: "hsl(var(--blue))",
                      }
                    : {
                        background: "transparent",
                        border: "1px solid transparent",
                        color: "hsl(var(--tx-3))",
                      }),
                }}
              >
                {tab.icon}
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Scrollable results */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
        {/* Profile summary */}
        {profile && showProfile && (
          <div className="animate-in">
            <ProfileSummary profile={profile} />
            <button
              onClick={() => setShowProfile(false)}
              className="text-xs mt-1.5 px-1"
              style={{ color: "hsl(var(--tx-3))" }}
            >
              {trEx.hideProfile}
            </button>
          </div>
        )}
        {!showProfile && profile && (
          <button
            onClick={() => setShowProfile(true)}
            className="btn btn-ghost w-full justify-center text-xs"
          >
            {trEx.showExtractedProfile}
          </button>
        )}

        {/* Cards */}
        {filtered.map((result, i) => (
          <SchemeCard key={result.scheme_id} result={result} index={i} />
        ))}

        {filtered.length === 0 && (
          <div className="py-8 text-center text-sm" style={{ color: "hsl(var(--tx-3))" }}>
            {trEx.noSchemesMatchFilter}
          </div>
        )}

        {/* Disclaimer */}
        <div
          className="flex items-start gap-2 rounded-xl px-3.5 py-3 text-sm mt-1"
          style={{
            background: "hsl(var(--amber) / 0.08)",
            border: "1.5px solid hsl(var(--amber) / 0.22)",
            color: "hsl(var(--tx-2))",
          }}
        >
          <AlertTriangle size={15} className="flex-shrink-0 mt-0.5" style={{ color: "hsl(var(--amber))" }} />
          <span>{tr.disclaimer}</span>
        </div>
      </div>
    </div>
  );
}
