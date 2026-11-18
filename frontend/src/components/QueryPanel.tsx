"use client";

import React, { useState } from "react";
import { QueryRequest } from "@/types";
import { Search, Loader2 } from "lucide-react";

interface QueryPanelProps {
  onSubmit: (request: QueryRequest) => void;
  isLoading: boolean;
}

export const QueryPanel: React.FC<QueryPanelProps> = ({
  onSubmit,
  isLoading,
}) => {
  const [question, setQuestion] = useState("");
  const [tickers, setTickers] = useState("");
  const [year, setYear] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const parsedYear = year.trim() ? parseInt(year.trim(), 10) : undefined;
    const parsedTickers = tickers
      .split(",")
      .map((t) => t.trim().toUpperCase())
      .filter((t) => t);

    onSubmit({
      question: question.trim(),
      tickers: parsedTickers.length > 0 ? parsedTickers : undefined,
      year: isNaN(parsedYear as number) ? undefined : parsedYear,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <div>
        <label className="block text-sm font-medium text-gray-900 mb-2">
          Question
        </label>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about the SEC filings..."
          disabled={isLoading}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50 resize-none text-gray-900"
          rows={3}
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-900 mb-1">
            Company / Ticker (Optional)
          </label>
          <input
            type="text"
            value={tickers}
            onChange={(e) => setTickers(e.target.value)}
            placeholder="e.g. AAPL, MSFT"
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 text-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900 mb-1">
            Fiscal Year (Optional)
          </label>
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            placeholder="e.g. 2023"
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 text-sm"
          />
        </div>
      </div>

      <div className="flex justify-end pt-2">
        <button
          type="submit"
          disabled={isLoading || !question.trim()}
          className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors text-sm"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Retrieving & Generating...
            </>
          ) : (
            <>
              <Search className="w-4 h-4" />
              Ask
            </>
          )}
        </button>
      </div>
    </form>
  );
};
