"use client";

import { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import type { Scheme } from "@/lib/types";
import { fetchSchemes } from "@/lib/api";
import { useLang } from "@/lib/LanguageContext";
import { t, tExtra } from "@/lib/i18n";
import {
  Tractor, Home, HeartPulse, UserCircle, GraduationCap, ListChecks,
  ArrowLeft, AlertCircle, Search, FileText, Building2, X, ChevronRight,
} from "lucide-react";

/* ── Category config ───────────────────────────────────────────────────────── */
const CATEGORIES = [
  { key: "all", label: "All Schemes" },
  { key: "farmer", label: "Farmer Support" },
  { key: "housing", label: "Housing" },
  { key: "healthcare", label: "Healthcare" },
  { key: "pension", label: "Pension" },
  { key: "education", label: "Education" },
] as const;

type CategoryKey = (typeof CATEGORIES)[number]["key"];

const CATEGORY_META: Record<
  string,
  { icon: React.ReactNode; colorVar: string; bg: string; border: string; label: string }
> = {
  farmer: {
    icon: <Tractor size={18} />,
    colorVar: "hsl(152 60% 45%)",
    bg: "hsl(152 60% 45% / 0.10)",
    border: "hsl(152 60% 45% / 0.28)",
    label: "Farmer Support",
  },
  housing: {
    icon: <Home size={18} />,
    colorVar: "hsl(220 80% 60%)",
    bg: "hsl(220 80% 60% / 0.10)",
    border: "hsl(220 80% 60% / 0.28)",
    label: "Housing",
  },
  healthcare: {
    icon: <HeartPulse size={18} />,
    colorVar: "hsl(338 70% 58%)",
    bg: "hsl(338 70% 58% / 0.10)",
    border: "hsl(338 70% 58% / 0.28)",
    label: "Healthcare",
  },
  pension: {
    icon: <UserCircle size={18} />,
    colorVar: "hsl(38 80% 55%)",
    bg: "hsl(38 80% 55% / 0.10)",
    border: "hsl(38 80% 55% / 0.28)",
    label: "Pension",
  },
  education: {
    icon: <GraduationCap size={18} />,
    colorVar: "hsl(252 60% 64%)",
    bg: "hsl(252 60% 64% / 0.10)",
    border: "hsl(252 60% 64% / 0.28)",
    label: "Education",
  },
};

/* ── Stats derived from schemes ────────────────────────────────────────────── */
function getStats(schemes: Scheme[]) {
  const totalBeneficiaries: Record<string, string> = {
    "pm-kisan": "11 Cr+",
    pmay: "2.5 Cr+",
    "ayushman-bharat": "50 Cr+",
    nsap: "3 Cr+",
    "nsp-scholarship": "1 Cr+",
  };
  return {
    count: schemes.length,
    categories: new Set(schemes.map((s) => s.category)).size,
    maxBenefit: "₹5 lakh / yr",
  };
}

/* ── Main page ─────────────────────────────────────────────────────────────── */
export default function SchemesPage() {
  const { lang } = useLang();
  const tr = t(lang);
  const trEx = tExtra(lang);

  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState<CategoryKey>("all");
  const [query, setQuery] = useState("");

  const getCategoryLabel = (key: string) => {
    if (key === "all") return tr.allSchemes ?? "All Schemes";
    if (key === "farmer") return trEx.catFarmer;
    if (key === "housing") return trEx.catHousing;
    if (key === "healthcare") return trEx.catHealthcare;
    if (key === "pension") return trEx.catPension;
    if (key === "education") return trEx.catEducation;
    return key;
  };

  useEffect(() => {
    setLoading(true);
    fetchSchemes(lang)
      .then(setSchemes)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [lang]);

  const filtered = useMemo(() => {
    let result = schemes;
    if (category !== "all") result = result.filter((s) => s.category === category);
    if (query.trim()) {
      const q = query.toLowerCase();
      result = result.filter(
        (s) =>
          s.name.toLowerCase().includes(q) ||
          s.summary.toLowerCase().includes(q) ||
          s.ministry?.toLowerCase().includes(q) ||
          s.category.toLowerCase().includes(q)
      );
    }
    return result;
  }, [schemes, category, query]);

  const stats = getStats(schemes);

  return (
    <div className="min-h-svh" style={{ background: "hsl(var(--bg))" }}>
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <header
        className="sticky top-0 z-10 px-6 h-12 flex items-center gap-3"
        style={{
          borderBottom: "1px solid hsl(var(--border))",
          background: "hsl(var(--bg) / 0.92)",
          backdropFilter: "blur(10px)",
        }}
      >
        <Link href="/" className="nav-link flex items-center gap-1.5 -ml-2">
          <ArrowLeft size={13} />
          {trEx.back}
        </Link>
        <span style={{ color: "hsl(var(--border-hi))" }}>/</span>
        <div className="flex items-center gap-2">
          <div
            className="w-5 h-5 rounded flex items-center justify-center"
            style={{ background: "hsl(var(--blue))" }}
          >
            <svg width="10" height="10" viewBox="0 0 14 14" fill="none">
              <path
                d="M7 1L9 5.5L14 6.18L10.5 9.59L11.38 14L7 11.77L2.62 14L3.5 9.59L0 6.18L5 5.5L7 1Z"
                fill="white"
              />
            </svg>
          </div>
          <Link
            href="/"
            className="text-sm font-semibold no-underline"
            style={{ color: "hsl(var(--tx))" }}
          >
            Benefitor AI
          </Link>
        </div>
        <span style={{ color: "hsl(var(--border-hi))" }}>/</span>
        <span className="text-sm" style={{ color: "hsl(var(--tx-2))" }}>
          {tr.allSchemes}
        </span>
      </header>

      {/* ── Hero ───────────────────────────────────────────────────────── */}
      <div
        className="px-6 py-10"
        style={{
          borderBottom: "1px solid hsl(var(--border))",
          background: "hsl(var(--s1))",
        }}
      >
        <div className="max-w-4xl mx-auto">
          <p
            className="text-xs font-medium uppercase tracking-widest mb-3"
            style={{ color: "hsl(var(--blue))" }}
          >
            {trEx.govtOfIndia}
          </p>
          <h1
            className="text-2xl font-semibold mb-2"
            style={{ color: "hsl(var(--tx))", letterSpacing: "-0.03em" }}
          >
            {tr.schemesHeading}
          </h1>
          <p className="text-sm mb-7" style={{ color: "hsl(var(--tx-2))" }}>
            {tr.schemesSubtext}
          </p>

          {/* Stats row */}
          <dl className="flex gap-6 mb-7">
            {[
              { value: stats.count, label: tr.statsSchemes },
              { value: stats.categories, label: tr.categoryCounts },
              { value: stats.maxBenefit, label: tr.highestBenefit },
              { value: tr.freeCost, label: trEx.costToApply },
            ].map((s) => (
              <div key={s.label}>
                <dt
                  className="text-xl font-semibold tabular"
                  style={{ color: "hsl(var(--tx))", letterSpacing: "-0.025em" }}
                >
                  {s.value}
                </dt>
                <dd className="text-xs mt-0.5" style={{ color: "hsl(var(--tx-3))" }}>
                  {s.label}
                </dd>
              </div>
            ))}
          </dl>

          {/* Search */}
          <div
            className="flex items-center gap-2.5 rounded-lg px-3.5 py-2.5 max-w-md"
            style={{
              background: "hsl(var(--bg))",
              border: "1px solid hsl(var(--border-hi))",
            }}
          >
            <Search size={14} style={{ color: "hsl(var(--tx-3))", flexShrink: 0 }} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tr.searchPlaceholder}
              className="flex-1 bg-transparent text-sm outline-none"
              style={{ color: "hsl(var(--tx))" }}
            />
            {query && (
              <button onClick={() => setQuery("")}>
                <X size={13} style={{ color: "hsl(var(--tx-3))" }} />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* ── Body ───────────────────────────────────────────────────────── */}
      <div className="max-w-4xl mx-auto px-6 py-8">

        {/* Category filter tabs */}
        <div className="flex flex-wrap gap-1.5 mb-6">
          {CATEGORIES.map((cat) => {
            const active = category === cat.key;
            const meta = cat.key !== "all" ? CATEGORY_META[cat.key] : null;
            return (
              <button
                key={cat.key}
                onClick={() => setCategory(cat.key)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm"
                style={{
                  ...(active && meta
                    ? {
                        background: meta.bg,
                        border: `1px solid ${meta.border}`,
                        color: meta.colorVar,
                      }
                    : active
                    ? {
                        background: "hsl(var(--blue) / 0.12)",
                        border: "1px solid hsl(var(--blue) / 0.35)",
                        color: "hsl(var(--blue))",
                      }
                    : {
                        background: "hsl(var(--s1))",
                        border: "1px solid hsl(var(--border))",
                        color: "hsl(var(--tx-2))",
                      }),
                  transition: "background-color 120ms ease-out, border-color 120ms ease-out, color 120ms ease-out",
                }}
              >
                {meta && <span style={{ color: active ? meta.colorVar : "hsl(var(--tx-3))" }}>{meta.icon}</span>}
                {getCategoryLabel(cat.key)}
                {cat.key !== "all" && (
                  <span
                    className="text-xs tabular px-1.5 py-0.5 rounded"
                    style={{
                      background: active && meta ? meta.border : "hsl(var(--s2))",
                      color: active && meta ? meta.colorVar : "hsl(var(--tx-3))",
                    }}
                  >
                    {schemes.filter((s) => s.category === cat.key).length}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Results count */}
        {!loading && !error && (
          <p className="text-xs mb-4" style={{ color: "hsl(var(--tx-3))" }}>
            {filtered.length} {filtered.length !== 1 ? tr.statsSchemes.toLowerCase() : tr.statsSchemes.toLowerCase().replace(/s$/, "")}
            {query && ` matching "${query}"`}
            {category !== "all" && ` in ${getCategoryLabel(category)}`}
          </p>
        )}

        {/* Skeleton */}
        {loading && (
          <div className="flex flex-col gap-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="shimmer h-32 rounded-xl" />
            ))}
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            className="flex items-center gap-2.5 p-3.5 rounded-xl text-sm"
            style={{
              background: "hsl(var(--red) / 0.08)",
              border: "1px solid hsl(var(--red) / 0.25)",
              color: "hsl(var(--red))",
            }}
          >
            <AlertCircle size={15} className="flex-shrink-0" />
            <span>Could not load schemes: {error}. Make sure the backend is running on port 8000.</span>
          </div>
        )}

        {/* Scheme list — full-width rows, not a grid */}
        {!loading && !error && (
          <div className="flex flex-col gap-3">
            {filtered.map((scheme, i) => {
              const meta = CATEGORY_META[scheme.category];
              return (
                <Link
                  key={scheme.id}
                  href={`/schemes/${scheme.id}`}
                  className="card block no-underline group animate-in"
                  style={{
                    animationDelay: `${i * 50}ms`,
                    textDecoration: "none",
                    transition:
                      "transform 140ms ease-out, box-shadow 140ms ease-out, border-color 140ms ease-out",
                  }}
                  onMouseEnter={(e) => {
                    const el = e.currentTarget as HTMLAnchorElement;
                    el.style.borderColor = meta ? meta.border : "hsl(var(--border-hi))";
                    el.style.boxShadow = `0 4px 24px ${meta ? meta.bg : "hsl(var(--blue) / 0.06)"}`;
                  }}
                  onMouseLeave={(e) => {
                    const el = e.currentTarget as HTMLAnchorElement;
                    el.style.borderColor = "";
                    el.style.boxShadow = "";
                  }}
                >
                  <div className="flex items-start gap-4 p-4 pb-3">
                    {/* Icon */}
                    <div
                      className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5"
                      style={{ background: meta?.bg ?? "hsl(var(--s2))", color: meta?.colorVar ?? "hsl(var(--tx-2))" }}
                    >
                      {meta?.icon ?? <ListChecks size={18} />}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-3 mb-1">
                        <div>
                          <h2
                            className="text-sm font-semibold leading-snug"
                            style={{ color: "hsl(var(--tx))" }}
                          >
                            {scheme.name}
                          </h2>
                          {scheme.ministry && (
                            <p
                              className="text-xs mt-0.5 flex items-center gap-1"
                              style={{ color: "hsl(var(--tx-3))" }}
                            >
                              <Building2 size={11} />
                              {scheme.ministry}
                            </p>
                          )}
                        </div>
                        <div className="flex items-center gap-2 flex-shrink-0">
                          {scheme.benefit_amount && (
                            <span
                              className="chip text-xs"
                              style={{
                                background: "hsl(var(--blue) / 0.10)",
                                border: "1px solid hsl(var(--blue) / 0.25)",
                                color: "hsl(var(--blue))",
                              }}
                            >
                              {scheme.benefit_amount}
                            </span>
                          )}
                          <ChevronRight
                            size={15}
                            style={{
                              color: "hsl(var(--tx-3))",
                              transition: "transform 140ms ease-out, color 140ms ease-out",
                            }}
                            className="group-hover:translate-x-0.5"
                          />
                        </div>
                      </div>

                      <p
                        className="text-xs leading-relaxed line-clamp-2 mb-3"
                        style={{ color: "hsl(var(--tx-2))" }}
                      >
                        {scheme.summary}
                      </p>

                      {/* Bottom meta row */}
                      <div
                        className="flex items-center gap-4 pt-2.5"
                        style={{ borderTop: "1px solid hsl(var(--border))" }}
                      >
                        {/* Category pill */}
                        <span
                           className="chip flex items-center gap-1"
                           style={{
                             background: meta?.bg ?? "hsl(var(--s2))",
                             border: `1px solid ${meta?.border ?? "hsl(var(--border))"}`,
                             color: meta?.colorVar ?? "hsl(var(--tx-2))",
                             fontSize: "0.7rem",
                           }}
                        >
                          {meta?.icon}
                          {getCategoryLabel(scheme.category)}
                        </span>

                        {/* Documents */}
                        <span
                          className="flex items-center gap-1 text-xs"
                          style={{ color: "hsl(var(--tx-3))" }}
                        >
                          <FileText size={11} />
                          {scheme.documents_required.length} {tr.docsRequired}
                        </span>

                        {/* Eligibility rules */}
                        <span
                          className="flex items-center gap-1 text-xs"
                          style={{ color: "hsl(var(--tx-3))" }}
                        >
                          <ListChecks size={11} />
                          {scheme.eligibility_rules.filter((r) => r.required).length} {tr.requiredCriteria}
                        </span>

                        {/* External url hint */}
                        <span
                          className="ml-auto text-xs"
                          style={{ color: "hsl(var(--tx-3))" }}
                        >
                          {new URL(scheme.official_url).hostname}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              );
            })}

            {filtered.length === 0 && (
              <div className="py-16 text-center">
                <p className="text-sm mb-1" style={{ color: "hsl(var(--tx-2))" }}>
                  {tr.noSchemesFound}
                </p>
                <p className="text-xs" style={{ color: "hsl(var(--tx-3))" }}>
                  Try a different category or search term
                </p>
                <button
                  onClick={() => { setQuery(""); setCategory("all"); }}
                  className="btn btn-ghost mt-4"
                >
                  {tr.clearFilters}
                </button>
              </div>
            )}
          </div>
        )}

        {/* CTA */}
        {!loading && !error && filtered.length > 0 && (
          <div
            className="mt-8 p-5 rounded-xl flex items-center justify-between gap-4"
            style={{
              background: "hsl(var(--blue) / 0.06)",
              border: "1px solid hsl(var(--blue) / 0.18)",
            }}
          >
            <div>
              <p className="text-sm font-medium" style={{ color: "hsl(var(--tx))" }}>
                {tr.ctaHeading}
              </p>
              <p className="text-xs mt-0.5" style={{ color: "hsl(var(--tx-2))" }}>
                {tr.ctaSubtext}
              </p>
            </div>
            <Link href="/" className="btn btn-primary flex-shrink-0">
              {tr.checkEligibility}
              <ChevronRight size={13} />
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
