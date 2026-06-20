import type { Metadata } from "next";
import "./globals.css";
import { LanguageProvider } from "@/lib/LanguageContext";
import { ChatProvider } from "@/lib/ChatContext";

export const metadata: Metadata = {
  title: "Benefitor AI — Welfare Benefits Navigator",
  description:
    "AI-powered welfare benefits navigator for Indian citizens. Discover government schemes you qualify for through natural conversation — in your language.",
  keywords:
    "welfare schemes, government benefits, India, PM-KISAN, PMAY, Ayushman Bharat, scholarships, pension, hindi, telugu, tamil, bengali",
  openGraph: {
    title: "Benefitor AI",
    description:
      "Discover government welfare schemes you qualify for — powered by AI, in your language.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        {/*
          Noto Sans covers:
          - Latin (English)
          - Devanagari (Hindi, Marathi)
          - Bengali
          - Tamil
          - Telugu
          - Gujarati
          - Gurmukhi (Punjabi)
        */}
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;500;600;700&family=Noto+Sans+Tamil:wght@400;500;600;700&family=Noto+Sans+Telugu:wght@400;500;600;700&family=Noto+Sans+Gujarati:wght@400;500;600;700&family=Noto+Sans+Gurmukhi:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased" suppressHydrationWarning>
        <LanguageProvider><ChatProvider>{children}</ChatProvider></LanguageProvider>
      </body>
    </html>
  );
}
