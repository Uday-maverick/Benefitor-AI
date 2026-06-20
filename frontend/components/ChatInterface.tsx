"use client";

import { useState, useRef, useEffect } from "react";
import type { ChatMessage, ChatResponse } from "@/lib/types";
import { useLang } from "@/lib/LanguageContext";
import { useChat } from "@/lib/ChatContext";
import { t } from "@/lib/i18n";
import { Mic, MicOff } from "lucide-react";

interface ChatInterfaceProps {
  onResponse: (response: ChatResponse) => void;
  isLoading: boolean;
  setIsLoading: (v: boolean) => void;
}

export default function ChatInterface({
  onResponse,
  isLoading,
  setIsLoading,
}: ChatInterfaceProps) {
  const { lang } = useLang();
  const tr = t(lang);
  const { messages, setMessages } = useChat();

  const [input, setInput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const rec = new SpeechRecognition();
        rec.continuous = false;
        rec.interimResults = false;

        rec.onstart = () => {
          setIsListening(true);
        };

        rec.onresult = (e: any) => {
          const transcript = e.results[0][0].transcript;
          if (transcript) {
            setInput((prev) => (prev ? prev + " " + transcript : transcript));
            setTimeout(() => {
              if (textareaRef.current) {
                textareaRef.current.style.height = "auto";
                textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 140) + "px";
              }
            }, 10);
          }
        };

        rec.onerror = (e: any) => {
          console.error("Speech recognition error", e);
          setIsListening(false);
        };

        rec.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = rec;
      }
    }
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert("Voice input is not supported in this browser. Please use Chrome, Edge or Safari.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      const locales: Record<string, string> = {
        en: "en-IN",
        hi: "hi-IN",
        bn: "bn-IN",
        ta: "ta-IN",
        te: "te-IN",
        mr: "mr-IN",
        gu: "gu-IN",
        pa: "pa-IN",
      };
      recognitionRef.current.lang = locales[lang] || "en-IN";
      try {
        recognitionRef.current.start();
      } catch (err) {
        console.error(err);
      }
    }
  };

  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;
    setError(null);

    const userMsg: ChatMessage = { role: "user", content: text };
    const newHistory = [...messages, userMsg];
    setMessages(newHistory);
    setInput("");
    setIsListening(false);
    if (isListening && recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch(e){}
    }
    setIsLoading(true);

    if (textareaRef.current) textareaRef.current.style.height = "auto";

    try {
      const { sendChatMessage } = await import("@/lib/api");
      const response = await sendChatMessage(text, messages, lang);
      const nextMessages: ChatMessage[] = [...newHistory, { role: "assistant", content: response.reply }];
      if (response.profile) {
        nextMessages.push({ role: "system", content: JSON.stringify(response.profile) });
      }
      setMessages(nextMessages);
      onResponse(response);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong";
      setError(msg);
      setMessages([
        ...newHistory,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the server. Please make sure the backend is running on http://localhost:8000.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 140) + "px";
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="flex flex-col h-full" style={{ background: "hsl(var(--bg))" }}>
      {/* ── Messages ────────────────────────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-5 py-6 space-y-4">
        {isEmpty ? (
          <div className="animate-in flex flex-col justify-center h-full max-w-lg mx-auto py-4">
            {/* Welcome */}
            <div className="mb-7">
              <p
                className="text-xs font-semibold uppercase tracking-widest mb-3"
                style={{ color: "hsl(var(--blue))" }}
              >
                {tr.welcomeCaption}
              </p>
              <h2
                className="text-2xl font-bold mb-2"
                style={{ color: "hsl(var(--tx))", letterSpacing: "-0.025em" }}
              >
                {tr.welcomeHeading}
              </h2>
              <p className="text-base" style={{ color: "hsl(var(--tx-2))" }}>
                {tr.welcomeSubtext}
              </p>
            </div>

            {/* Examples — large touch targets */}
            <div>
              <p
                className="text-sm font-semibold uppercase tracking-wider mb-3"
                style={{ color: "hsl(var(--tx-3))" }}
              >
                {tr.tryExample}
              </p>
              <div className="flex flex-col gap-2">
                {tr.examples.map((example, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(example)}
                    className="example-btn"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.filter(msg => msg.role !== "system").map((msg, i) => (
              <MessageBubble key={i} message={msg} index={i} />
            ))}
            {isLoading && <TypingIndicator />}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* ── Error ───────────────────────────────────────────────────────── */}
      {error && (
        <div
          className="mx-5 mb-2 px-4 py-3 rounded-xl text-sm"
          style={{
            background: "hsl(var(--red) / 0.08)",
            border: "1.5px solid hsl(var(--red) / 0.25)",
            color: "hsl(var(--red))",
          }}
        >
          {error}
        </div>
      )}

      {/* ── Input ───────────────────────────────────────────────────────── */}
      <div
        className="px-5 pb-4 pt-3"
        style={{ borderTop: "1.5px solid hsl(var(--border))", background: "hsl(var(--s1))" }}
      >
        <div className="input-wrap flex items-end gap-3 px-4 py-3">
          <textarea
            ref={textareaRef}
            id="chat-input"
            value={input}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder={tr.inputPlaceholder}
            rows={1}
            disabled={isLoading}
            className="flex-1 resize-none bg-transparent outline-none"
            style={{
              color: "hsl(var(--tx))",
              fontSize: "1rem",
              lineHeight: "1.6",
              maxHeight: "140px",
            }}
          />
          <button
            type="button"
            onClick={toggleListening}
            disabled={isLoading}
            className="flex-shrink-0 w-11 h-11 rounded-xl flex items-center justify-center transition-all duration-150"
            style={{
              background: isListening ? "hsl(var(--red) / 0.15)" : "hsl(var(--s2))",
              color: isListening ? "hsl(var(--red))" : "hsl(var(--tx-2))",
              border: isListening ? "1.5px solid hsl(var(--red) / 0.4)" : "1.5px solid hsl(var(--border))",
              cursor: "pointer",
            }}
            aria-label={isListening ? "Stop voice input" : "Start voice input"}
            title="Voice Input (Speak)"
          >
            {isListening ? (
              <MicOff size={18} className="animate-pulse" />
            ) : (
              <Mic size={18} />
            )}
          </button>
          <button
            id="send-button"
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || isLoading}
            className="flex-shrink-0 w-11 h-11 rounded-xl flex items-center justify-center"
            style={{
              background: input.trim() && !isLoading ? "hsl(var(--blue))" : "hsl(var(--s3))",
              cursor: input.trim() && !isLoading ? "pointer" : "default",
              transition: "background-color 150ms ease-out",
              boxShadow: input.trim() && !isLoading ? "0 2px 8px hsl(var(--blue) / 0.30)" : "none",
            }}
            aria-label="Send message"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                d="M14 8L2 2L5 8L2 14L14 8Z"
                fill={input.trim() && !isLoading ? "white" : "hsl(var(--tx-3))"}
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
        <p className="text-xs mt-2 px-1" style={{ color: "hsl(var(--tx-3))" }}>
          {tr.inputHint}
        </p>
      </div>
    </div>
  );
}

function MessageBubble({ message, index }: { message: ChatMessage; index: number }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} animate-in`}
      style={{ animationDelay: `${index * 40}ms` }}
    >
      {!isUser && (
        <div
          className="w-9 h-9 rounded-xl flex items-center justify-center mr-2.5 flex-shrink-0 mt-0.5"
          style={{ background: "hsl(var(--blue))" }}
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path
              d="M7 1L9 5.5L14 6.18L10.5 9.59L11.38 14L7 11.77L2.62 14L3.5 9.59L0 6.18L5 5.5L7 1Z"
              fill="white"
            />
          </svg>
        </div>
      )}
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-base leading-relaxed ${
          isUser ? "bubble-user" : "bubble-ai"
        }`}
        style={{ fontSize: "1rem" }}
      >
        {message.content}
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex items-center gap-2.5 animate-in">
      <div
        className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
        style={{ background: "hsl(var(--blue))" }}
      >
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path
            d="M7 1L9 5.5L14 6.18L10.5 9.59L11.38 14L7 11.77L2.62 14L3.5 9.59L0 6.18L5 5.5L7 1Z"
            fill="white"
          />
        </svg>
      </div>
      <div
        className="flex items-center gap-1.5 px-4 py-3 rounded-2xl bubble-ai"
        style={{ borderBottomLeftRadius: "4px" }}
      >
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </div>
  );
}
