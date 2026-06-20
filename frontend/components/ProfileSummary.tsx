"use client";

import type { UserProfile } from "@/lib/types";
import {
  Calendar, MapPin, Map, Briefcase, Banknote, Tag,
  GraduationCap, Tractor, Home, Leaf, Accessibility,
  UserCircle, User, FileText,
} from "lucide-react";
import { useLang } from "@/lib/LanguageContext";
import { tExtra } from "@/lib/i18n";

const FIELD_LABELS: Record<string, string> = {
  age:                   "Age",
  state:                 "State",
  district:              "District",
  occupation:            "Occupation",
  annual_income:         "Annual Income",
  category:              "Category",
  student_status:        "Student",
  farmer_status:         "Farmer",
  housing_status:        "Housing",
  land_ownership:        "Owns Land",
  disability_status:     "Disability",
  senior_citizen_status: "Senior Citizen",
  gender:                "Gender",
  bpl_card:              "BPL Card",
};

const FIELD_ICONS: Record<string, React.ReactNode> = {
  age:                   <Calendar size={13} />,
  state:                 <MapPin size={13} />,
  district:              <Map size={13} />,
  occupation:            <Briefcase size={13} />,
  annual_income:         <Banknote size={13} />,
  category:              <Tag size={13} />,
  student_status:        <GraduationCap size={13} />,
  farmer_status:         <Tractor size={13} />,
  housing_status:        <Home size={13} />,
  land_ownership:        <Leaf size={13} />,
  disability_status:     <Accessibility size={13} />,
  senior_citizen_status: <UserCircle size={13} />,
  gender:                <User size={13} />,
  bpl_card:              <FileText size={13} />,
};

function formatValue(key: string, value: unknown, trEx: any, country: string | null | undefined): string {
  if (value === null || value === undefined) return "";
  if (key === "annual_income") {
    const isUs = (country || "").toLowerCase().trim() === "us";
    const symbol = isUs ? "$" : "₹";
    const locale = isUs ? "en-US" : "en-IN";
    return `${symbol}${(value as number).toLocaleString(locale)}`;
  }
  if (typeof value === "boolean") return value ? trEx.yes : trEx.no;
  if (typeof value === "string")
    return value.charAt(0).toUpperCase() + value.slice(1).replace(/_/g, " ");
  return String(value);
}

interface ProfileSummaryProps {
  profile: UserProfile;
}

export default function ProfileSummary({ profile }: ProfileSummaryProps) {
  const { lang } = useLang();
  const trEx = tExtra(lang);

  const entries = Object.entries(profile).filter(
    ([, v]) => v !== null && v !== undefined && v !== false
  );

  if (entries.length === 0) return null;

  return (
    <div
      className="rounded-xl p-3.5"
      style={{
        background: "hsl(var(--s1))",
        border: "1px solid hsl(var(--border))",
      }}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider" style={{ color: "hsl(var(--tx-3))" }}>
          {trEx.extractedProfile}
        </h3>
        <span
          className="chip tabular"
          style={{
            background: "hsl(var(--blue) / 0.1)",
            border: "1px solid hsl(var(--blue) / 0.22)",
            color: "hsl(var(--blue))",
          }}
        >
          {entries.length} {trEx.fields}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-1.5">
        {entries.map(([key, value]) => (
          <div
            key={key}
            className="flex items-center gap-2 px-2.5 py-2 rounded-lg"
            style={{
              background: "hsl(var(--s2))",
            }}
          >
            <span className="flex-shrink-0" style={{ color: "hsl(var(--tx-3))" }}>
              {FIELD_ICONS[key] ?? <User size={13} />}
            </span>
            <div className="min-w-0">
              <p className="text-xs truncate" style={{ color: "hsl(var(--tx-3))" }}>
                {trEx[key as keyof typeof trEx] ?? key}
              </p>
              <p className="text-xs font-medium truncate" style={{ color: "hsl(var(--tx))" }}>
                {formatValue(key, value, trEx, profile.country)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
