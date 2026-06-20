"use client";

import type { MatchResult } from "@/lib/types";
import { useRouter } from "next/navigation";
import { useLang } from "@/lib/LanguageContext";
import { t, tExtra } from "@/lib/i18n";
import {
  Tractor, Home, HeartPulse, UserCircle, GraduationCap, ListChecks,
  CheckCircle2, HelpCircle, XCircle, ArrowRight,
} from "lucide-react";

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  farmer:     <Tractor size={16} />,
  housing:    <Home size={16} />,
  healthcare: <HeartPulse size={16} />,
  pension:    <UserCircle size={16} />,
  education:  <GraduationCap size={16} />,
};

const CATEGORY_LABELS: Record<string, string> = {
  farmer:     "Farmer Support",
  housing:    "Housing",
  healthcare: "Healthcare",
  pension:    "Pension",
  education:  "Education",
};

const STATUS_CONFIG = {
  "Likely Eligible": {
    badge: "badge-eligible",
    icon: <CheckCircle2 size={13} />,
  },
  "Possibly Eligible": {
    badge: "badge-possibly",
    icon: <HelpCircle size={13} />,
  },
  "Likely Not Eligible": {
    badge: "badge-not-eligible",
    icon: <XCircle size={13} />,
  },
} as const;

interface SchemeCardProps {
  result: MatchResult;
  index?: number;
}

export default function SchemeCard({ result, index = 0 }: SchemeCardProps) {
  const router = useRouter();
  const { lang } = useLang();
  const tr = t(lang);
  const trEx = tExtra(lang);

  const icon = CATEGORY_ICONS[result.scheme_category] ?? <ListChecks size={16} />;
  
  const getCategoryLabel = (key: string) => {
    if (key === "farmer") return trEx.catFarmer;
    if (key === "housing") return trEx.catHousing;
    if (key === "healthcare") return trEx.catHealthcare;
    if (key === "pension") return trEx.catPension;
    if (key === "education") return trEx.catEducation;
    return key;
  };

  const getStatusLabel = (status: string) => {
    if (status === "Likely Eligible") return tr.eligible;
    if (status === "Possibly Eligible") return tr.possiblyEligible;
    if (status === "Likely Not Eligible") return tr.notEligible;
    return status;
  };

  const categoryLabel = getCategoryLabel(result.scheme_category);
  const cfg = STATUS_CONFIG[result.status as keyof typeof STATUS_CONFIG];

  return (
    <div
      className="card p-4 cursor-pointer animate-in"
      style={{
        animationDelay: `${index * 80}ms`,
        transition: "transform 150ms ease-out, box-shadow 150ms ease-out, border-color 150ms ease-out",
      }}
      onClick={() =>
        router.push(
          `/schemes/${result.scheme_id}?result=${encodeURIComponent(JSON.stringify(result))}`
        )
      }
      onMouseEnter={(e) => {
        const el = e.currentTarget as HTMLDivElement;
        el.style.transform = "translateY(-1px)";
        el.style.boxShadow = "0 6px 20px hsl(var(--blue) / 0.10)";
        el.style.borderColor = "hsl(var(--border-hi))";
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget as HTMLDivElement;
        el.style.transform = "";
        el.style.boxShadow = "";
        el.style.borderColor = "";
      }}
      role="button"
      tabIndex={0}
      aria-label={`View ${result.scheme_name} details`}
      onKeyDown={(e) => {
        if (e.key === "Enter") router.push(`/schemes/${result.scheme_id}`);
      }}
    >
      {/* Header row */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-start gap-3">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
            style={{
              background: "hsl(var(--s2))",
              color: "hsl(var(--tx-2))",
              /* inner radius (8px) = card radius (12px) - padding diff (4px) */
            }}
          >
            {icon}
          </div>
          <div>
            <h3 className="text-sm font-medium" style={{ color: "hsl(var(--tx))" }}>
              {result.scheme_name}
            </h3>
            <span className="text-xs" style={{ color: "hsl(var(--tx-3))" }}>
              {categoryLabel}
            </span>
          </div>
        </div>

        {cfg && (
          <span
            className={`${cfg.badge} chip flex items-center gap-1 flex-shrink-0`}
          >
            {cfg.icon}
            {getStatusLabel(result.status)}
          </span>
        )}
      </div>

      {/* Score bar */}
      <div className="mb-3">
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs" style={{ color: "hsl(var(--tx-3))" }}>
            {tr.eligibilityScore}
          </span>
          <span className="text-xs font-medium tabular" style={{ color: "hsl(var(--tx-2))" }}>
            {Math.round(result.score * 100)}%
          </span>
        </div>
        <div className="score-bar">
          <div className="score-fill" style={{ width: `${result.score * 100}%` }} />
        </div>
      </div>

      {/* Explanation */}
      <p
        className="text-xs leading-relaxed mb-3 line-clamp-2"
        style={{ color: "hsl(var(--tx-2))" }}
      >
        {result.explanation}
      </p>

      {/* Matched rules */}
      {result.matched_rules.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {result.matched_rules.slice(0, 2).map((rule, i) => (
            <span
              key={i}
              className="chip flex items-center gap-1"
              style={{
                background: "hsl(var(--green) / 0.08)",
                border: "1px solid hsl(var(--green) / 0.22)",
                color: "hsl(var(--green))",
              }}
            >
              <CheckCircle2 size={10} className="flex-shrink-0" />
              <span className="truncate max-w-32">{rule}</span>
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between">
        <span className="text-xs" style={{ color: "hsl(var(--tx-3))" }}>
          {result.documents_required.length} {tr.docsRequired}
        </span>
        <span
          className="text-xs font-medium flex items-center gap-1"
          style={{ color: "hsl(var(--blue))" }}
        >
          {tr.viewDetails}
          <ArrowRight size={12} />
        </span>
      </div>
    </div>
  );
}
