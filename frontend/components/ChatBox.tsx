"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { askQuestion } from "../lib/api";
import SourceList from "./SourceList";

type Source = {
  document_name: string;
  page: number;
  chunk_index: number;
  text: string;
};

type ChatBoxProps = {
  isReady: boolean;
};

export default function ChatBox({ isReady }: ChatBoxProps) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [error, setError] = useState("");

  const formatAnswer = (text: string) => {
    if (!text) return text;

    let formatted = text;

    // If model writes "Before:" and "After:" but forgets bullets, convert lines below them into bullets.
    formatted = formatted.replace(/(\*\*Before:\*\*|Before:)\n(?!- )([\s\S]*?)(?=\n(\*\*After:\*\*|After:)|\n\d+\. |\n\*\*Sources:|\nSources:|$)/g, (_match, heading, content) => {
      const bulletLines = content
        .split("\n")
        .map((line: string) => line.trim())
        .filter((line: string) => line.length > 0)
        .map((line: string) => (line.startsWith("- ") ? line : `- ${line}`))
        .join("\n");

      return `${heading}\n${bulletLines}\n`;
    });

    formatted = formatted.replace(/(\*\*After:\*\*|After:)\n(?!- )([\s\S]*?)(?=\n\d+\. |\n\*\*Sources:|\nSources:|$)/g, (_match, heading, content) => {
      const bulletLines = content
        .split("\n")
        .map((line: string) => line.trim())
        .filter((line: string) => line.length > 0)
        .map((line: string) => (line.startsWith("- ") ? line : `- ${line}`))
        .join("\n");

      return `${heading}\n${bulletLines}\n`;
    });

    return formatted;
  };

  const handleAsk = async () => {
    if (!isReady) {
      setError("Please upload a PDF first.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnswer("");
      setSources([]);

      const result = await askQuestion(question);

      setAnswer(result.answer);
      setSources(result.sources || []);
    } catch (error) {
      setError("Failed to get answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-2xl font-semibold text-gray-900">Ask Questions</h2>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something about the uploaded document..."
        rows={4}
        className="w-full rounded-xl border border-gray-300 p-4 text-sm text-gray-900 outline-none placeholder:text-gray-400 focus:ring-2 focus:ring-black"
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        className="mt-4 rounded-xl bg-black px-5 py-3 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {error && <p className="mt-4 text-sm text-red-600">{error}</p>}

      {answer && (
        <div className="mt-6 rounded-2xl border border-gray-200 bg-gray-50 p-6">
          <h3 className="mb-4 text-xl font-semibold text-gray-900">Answer</h3>

          <div
            className="prose prose-gray max-w-none text-gray-800
                       prose-p:leading-7
                       prose-li:leading-7
                       prose-strong:text-gray-900
                       prose-ul:my-3
                       prose-ol:my-3
                       prose-li:my-1
                       prose-headings:mb-2"
          >
            <ReactMarkdown>{formatAnswer(answer)}</ReactMarkdown>
          </div>
        </div>
      )}

      <SourceList sources={sources} />
    </div>
  );
}