"use client";

import { useState, useEffect } from "react";
import { useParams, useSearchParams } from "next/navigation";
import Link from "next/link";
import type { Scheme, MatchResult } from "@/lib/types";
import { fetchScheme } from "@/lib/api";
import { useLang } from "@/lib/LanguageContext";
import { t, tExtra } from "@/lib/i18n";
import {
  Tractor, Home, HeartPulse, UserCircle, GraduationCap, ListChecks,
  CheckCircle2, HelpCircle, XCircle, ExternalLink, ArrowLeft,
  FileText, ShieldCheck, AlertTriangle, Loader2,
} from "lucide-react";

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  farmer:     <Tractor size={24} />,
  housing:    <Home size={24} />,
  healthcare: <HeartPulse size={24} />,
  pension:    <UserCircle size={24} />,
  education:  <GraduationCap size={24} />,
};

const CATEGORY_CLASS: Record<string, string> = {
  farmer:     "cat-farmer",
  housing:    "cat-housing",
  healthcare: "cat-healthcare",
  pension:    "cat-pension",
  education:  "cat-education",
};

const STATUS_CONFIG = {
  "Likely Eligible": {
    badge: "badge-eligible",
    icon: <CheckCircle2 size={14} />,
  },
  "Possibly Eligible": {
    badge: "badge-possibly",
    icon: <HelpCircle size={14} />,
  },
  "Likely Not Eligible": {
    badge: "badge-not-eligible",
    icon: <XCircle size={14} />,
  },
} as const;

export default function SchemeDetailPage() {
  const { lang } = useLang();
  const tr = t(lang);
  const trEx = tExtra(lang);
  const params = useParams();
  const searchParams = useSearchParams();
  const schemeId = params.id as string;

  const [scheme, setScheme] = useState<Scheme | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const resultParam = searchParams.get("result");
  const matchResult: MatchResult | null = resultParam
    ? (() => {
        try { return JSON.parse(decodeURIComponent(resultParam)) as MatchResult; }
        catch { return null; }
      })()
    : null;

  useEffect(() => {
    setLoading(true);
    fetchScheme(schemeId, lang)
      .then(setScheme)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [schemeId, lang]);

  const statusCfg = matchResult
    ? STATUS_CONFIG[matchResult.status as keyof typeof STATUS_CONFIG]
    : null;

  const getStatusLabel = (status: string) => {
    if (status === "Likely Eligible") return tr.eligible;
    if (status === "Possibly Eligible") return tr.possiblyEligible;
    if (status === "Likely Not Eligible") return tr.notEligible;
    return status;
  };

  /* ── Loading ──────────────────────────────────────────────────────── */
  if (loading) {
    return (
      <div className="min-h-svh flex items-center justify-center" style={{ background: "hsl(var(--bg))" }}>
        <Loader2 size={22} className="animate-spin" style={{ color: "hsl(var(--blue))" }} />
      </div>
    );
  }

  /* ── Error ────────────────────────────────────────────────────────── */
  if (error || !scheme) {
    return (
      <div className="min-h-svh flex flex-col items-center justify-center gap-3" style={{ background: "hsl(var(--bg))" }}>
        <p className="text-sm" style={{ color: "hsl(var(--red))" }}>{error ?? "Scheme not found"}</p>
        <Link href="/" className="btn btn-ghost">
          <ArrowLeft size={13} /> {trEx.back}
        </Link>
      </div>
    );
  }

  /* ── Page ─────────────────────────────────────────────────────────── */
  return (
    <div className="min-h-svh" style={{ background: "hsl(var(--bg))" }}>
      {/* Header */}
      <header
        className="px-5 h-12 flex items-center gap-3"
        style={{ borderBottom: "1px solid hsl(var(--border))" }}
      >
        <Link href="/" className="nav-link flex items-center gap-1.5 -ml-2">
          <ArrowLeft size={13} />
          {trEx.back}
        </Link>
        <span style={{ color: "hsl(var(--border-hi))" }}>/</span>
        <Link href="/schemes" className="nav-link" style={{ padding: "4px 8px" }}>
          {tr.statsSchemes}
        </Link>
        <span style={{ color: "hsl(var(--border-hi))" }}>/</span>
        <span
          className="text-sm truncate max-w-48"
          style={{ color: "hsl(var(--tx-2))" }}
        >
          {scheme.name}
        </span>
      </header>

      <div className="max-w-3xl mx-auto px-5 py-10">
        {/* Hero card */}
        <div
          className="card p-5 mb-6 animate-in"
          style={{
            ...(matchResult?.status === "Likely Eligible" && {
              borderColor: "hsl(var(--green) / 0.35)",
            }),
          }}
        >
          <div className="flex items-start gap-4">
            <div
              className={`w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0 ${CATEGORY_CLASS[scheme.category] ?? ""}`}
              style={{ background: "hsl(var(--s2))" }}
            >
              {CATEGORY_ICONS[scheme.category] ?? <ListChecks size={24} />}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h1
                    className="text-xl font-semibold mb-0.5"
                    style={{ color: "hsl(var(--tx))", letterSpacing: "-0.025em" }}
                  >
                    {scheme.name}
                  </h1>
                  <p className="text-sm" style={{ color: "hsl(var(--tx-2))" }}>
                    {scheme.ministry}
                  </p>
                </div>
                {matchResult && statusCfg && (
                  <span
                    className={`${statusCfg.badge} chip flex items-center gap-1.5 flex-shrink-0`}
                  >
                    {statusCfg.icon}
                    {getStatusLabel(matchResult.status)}
                  </span>
                )}
              </div>
              {scheme.benefit_amount && (
                <span
                  className="chip mt-3 inline-flex"
                  style={{
                    background: "hsl(var(--blue) / 0.10)",
                    border: "1px solid hsl(var(--blue) / 0.25)",
                    color: "hsl(var(--blue))",
                  }}
                >
                  {scheme.benefit_amount}
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Left column */}
          <div className="space-y-4">
            {/* Overview */}
            <section className="card p-4 animate-in" style={{ animationDelay: "80ms" }}>
              <h2
                className="text-xs font-semibold uppercase tracking-wider mb-2.5"
                style={{ color: "hsl(var(--tx-3))" }}
              >
                {trEx.overview}
              </h2>
              <p className="text-sm leading-relaxed" style={{ color: "hsl(var(--tx-2))" }}>
                {scheme.summary}
              </p>
            </section>

            {/* AI Explanation */}
            {matchResult && (
              <section
                className="card p-4 animate-in"
                style={{
                  animationDelay: "140ms",
                  borderColor: "hsl(var(--blue) / 0.22)",
                  background: "hsl(var(--blue) / 0.04)",
                }}
              >
                <h2
                  className="text-xs font-semibold uppercase tracking-wider mb-2.5"
                  style={{ color: "hsl(var(--tx-3))" }}
                >
                  {trEx.aiAnalysis}
                </h2>
                <p className="text-sm leading-relaxed mb-3" style={{ color: "hsl(var(--tx-2))" }}>
                  {matchResult.explanation}
                </p>

                {matchResult.matched_rules.length > 0 && (
                  <div className="mb-2.5">
                    <p className="text-xs font-medium mb-1.5 flex items-center gap-1.5" style={{ color: "hsl(var(--green))" }}>
                      <CheckCircle2 size={12} /> {trEx.criteriaYouMeet}
                    </p>
                    <div className="flex flex-col gap-1">
                      {matchResult.matched_rules.map((rule, i) => (
                        <div
                          key={i}
                          className="text-xs px-2.5 py-1.5 rounded-lg"
                          style={{
                            background: "hsl(var(--green) / 0.08)",
                            border: "1px solid hsl(var(--green) / 0.18)",
                            color: "hsl(var(--green))",
                          }}
                        >
                          {rule}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {matchResult.missing_rules.length > 0 && (
                  <div className="mb-3">
                    <p className="text-xs font-medium mb-1.5 flex items-center gap-1.5" style={{ color: "hsl(var(--amber))" }}>
                      <HelpCircle size={12} /> {trEx.infoNeeded}
                    </p>
                    <div className="flex flex-col gap-1">
                      {matchResult.missing_rules.map((rule, i) => (
                        <div
                          key={i}
                          className="text-xs px-2.5 py-1.5 rounded-lg"
                          style={{
                            background: "hsl(var(--amber) / 0.07)",
                            border: "1px solid hsl(var(--amber) / 0.18)",
                            color: "hsl(var(--amber))",
                          }}
                        >
                          {rule}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Score */}
                <div>
                  <div className="flex justify-between mb-1.5 text-xs">
                    <span style={{ color: "hsl(var(--tx-3))" }}>{tr.eligibilityScore}</span>
                    <span className="font-medium tabular" style={{ color: "hsl(var(--tx-2))" }}>
                      {Math.round(matchResult.score * 100)}%
                    </span>
                  </div>
                  <div className="score-bar">
                    <div className="score-fill" style={{ width: `${matchResult.score * 100}%` }} />
                  </div>
                </div>
              </section>
            )}

            {/* Eligibility criteria */}
            <section className="card p-4 animate-in" style={{ animationDelay: "200ms" }}>
              <h2
                className="text-xs font-semibold uppercase tracking-wider mb-2.5 flex items-center gap-1.5"
                style={{ color: "hsl(var(--tx-3))" }}
              >
                <ShieldCheck size={12} />
                {tr.requiredCriteria}
              </h2>
              <div className="flex flex-col gap-2">
                {scheme.eligibility_rules.map((rule, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm">
                    <span
                      className="chip flex-shrink-0 mt-0.5"
                      style={{
                        background: rule.required ? "hsl(var(--red) / 0.08)" : "hsl(var(--amber) / 0.08)",
                        color: rule.required ? "hsl(var(--red))" : "hsl(var(--amber))",
                        border: `1px solid ${rule.required ? "hsl(var(--red) / 0.22)" : "hsl(var(--amber) / 0.22)"}`,
                      }}
                    >
                      {rule.required ? trEx.required : trEx.bonus}
                    </span>
                    <span style={{ color: "hsl(var(--tx-2))" }}>{rule.label}</span>
                  </div>
                ))}
              </div>
            </section>
          </div>

          {/* Right column */}
          <div className="space-y-4">
            {/* Documents required */}
            <section className="card p-4 animate-in" style={{ animationDelay: "120ms" }}>
              <h2
                className="text-xs font-semibold uppercase tracking-wider mb-2.5 flex items-center gap-1.5"
                style={{ color: "hsl(var(--tx-3))" }}
              >
                <FileText size={12} />
                {trEx.documentsRequired}
              </h2>
              <div className="flex flex-col gap-1.5">
                {scheme.documents_required.map((doc, i) => (
                  <div
                    key={i}
                    className="flex items-center gap-2 text-sm px-2.5 py-2 rounded-lg"
                    style={{ background: "hsl(var(--s2))" }}
                  >
                    <span
                      className="w-1 h-1 rounded-full flex-shrink-0"
                      style={{ background: "hsl(var(--tx-3))" }}
                    />
                    <span style={{ color: "hsl(var(--tx-2))" }}>{doc}</span>
                  </div>
                ))}
              </div>
            </section>

            {/* Apply */}
            <section
              className="card p-4 animate-in"
              style={{
                animationDelay: "180ms",
                background: "hsl(var(--blue) / 0.04)",
                borderColor: "hsl(var(--blue) / 0.22)",
              }}
            >
              <h2
                className="text-xs font-semibold uppercase tracking-wider mb-2"
                style={{ color: "hsl(var(--tx-3))" }}
              >
                {trEx.apply}
              </h2>
              <p className="text-xs mb-3.5" style={{ color: "hsl(var(--tx-2))" }}>
                Visit the official government portal to begin your application.
                Keep your documents ready before applying.
              </p>
              <a
                href={scheme.official_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary w-full justify-center"
              >
                {trEx.visitOfficialPortal}
                <ExternalLink size={13} />
              </a>
              <p
                className="text-xs text-center mt-2 truncate"
                style={{ color: "hsl(var(--tx-3))" }}
              >
                {scheme.official_url}
              </p>
            </section>

            {/* Disclaimer */}
            <div
              className="flex items-start gap-2 rounded-lg px-3 py-2.5 text-xs"
              style={{
                background: "hsl(var(--amber) / 0.06)",
                border: "1px solid hsl(var(--amber) / 0.18)",
                color: "hsl(var(--tx-2))",
              }}
            >
              <AlertTriangle size={13} className="flex-shrink-0 mt-0.5" style={{ color: "hsl(var(--amber))" }} />
              <span>
                {tr.disclaimer}
              </span>
            </div>

            {/* Back */}
            <Link href="/" className="btn btn-ghost w-full justify-center">
              <ArrowLeft size={13} />
              {trEx.back}
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
