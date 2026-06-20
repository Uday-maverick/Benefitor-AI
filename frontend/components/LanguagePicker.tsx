"use client";

import { useState, useRef, useEffect } from "react";
import { useLang } from "@/lib/LanguageContext";
import { LANGUAGES } from "@/lib/i18n";
import { Globe, Check } from "lucide-react";

export default function LanguagePicker() {
  const { lang, setLang } = useLang();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handle(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handle);
    return () => document.removeEventListener("mousedown", handle);
  }, []);

  const current = LANGUAGES.find((l) => l.code === lang)!;

  return (
    <div ref={ref} className="relative">
      <button
        className="lang-btn"
        onClick={() => setOpen((o) => !o)}
        aria-label="Select language"
        aria-expanded={open}
        aria-haspopup="listbox"
      >
        <Globe size={15} style={{ color: "hsl(var(--tx-3))" }} />
        <span>{current.nativeName}</span>
        <svg
          width="10"
          height="10"
          viewBox="0 0 10 10"
          fill="none"
          style={{
            transform: open ? "rotate(180deg)" : "rotate(0)",
            transition: "transform 150ms ease-out",
            color: "hsl(var(--tx-3))",
          }}
        >
          <path d="M2 3.5L5 6.5L8 3.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
        </svg>
      </button>

      {open && (
        <div
          className="absolute right-0 mt-1 z-50 py-1 rounded-xl overflow-hidden animate-in"
          style={{
            background: "hsl(var(--s1))",
            border: "1.5px solid hsl(var(--border))",
            boxShadow: "var(--shadow-md)",
            minWidth: "160px",
            animationDuration: "180ms",
          }}
          role="listbox"
          aria-label="Language options"
        >
          {LANGUAGES.map((l) => (
            <button
              key={l.code}
              role="option"
              aria-selected={l.code === lang}
              onClick={() => {
                setLang(l.code);
                setOpen(false);
              }}
              className="w-full flex items-center justify-between gap-3 px-3.5 py-2.5 text-sm"
              style={{
                background: l.code === lang ? "hsl(var(--blue) / 0.08)" : "transparent",
                color: l.code === lang ? "hsl(var(--blue))" : "hsl(var(--tx))",
                fontWeight: l.code === lang ? 600 : 400,
                transition: "background-color 100ms ease-out",
                textAlign: "left",
              }}
              onMouseEnter={(e) => {
                if (l.code !== lang)
                  (e.currentTarget as HTMLButtonElement).style.background = "hsl(var(--s2))";
              }}
              onMouseLeave={(e) => {
                if (l.code !== lang)
                  (e.currentTarget as HTMLButtonElement).style.background = "transparent";
              }}
            >
              <span>{l.nativeName}</span>
              {l.code === lang && <Check size={13} />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
