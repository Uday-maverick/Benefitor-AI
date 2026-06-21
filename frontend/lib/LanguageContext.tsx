"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import type { LangCode } from "./i18n";

interface LanguageContextType {
  lang: LangCode;
  setLang: (l: LangCode) => void;
}

const LanguageContext = createContext<LanguageContextType>({
  lang: "en",
  setLang: () => {},
});

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = useState<LangCode>("en");

  // Persist language choice in localStorage
  useEffect(() => {
    const saved = localStorage.getItem("midas_ledger_lang") as LangCode | null;
    if (saved) setLangState(saved);
  }, []);

  const setLang = (l: LangCode) => {
    setLangState(l);
    localStorage.setItem("midas_ledger_lang", l);
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLang() {
  return useContext(LanguageContext);
}
