"use client";

import React, { useState, useMemo } from "react";
import { QueryRequest } from "@/types";
import { Search, Loader2 } from "lucide-react";
import { useCorpusMetadata } from "@/hooks";

interface QueryPanelProps {
  onSubmit: (request: QueryRequest) => void;
  isLoading: boolean;
}

export const QueryPanel: React.FC<QueryPanelProps> = ({
  onSubmit,
  isLoading,
}) => {
  const [question, setQuestion] = useState("");
  const [selectedCompany, setSelectedCompany] = useState("");
  const [selectedYear, setSelectedYear] = useState("");

  const { data: corpus, isLoading: isCorpusLoading } = useCorpusMetadata();

  const companies = useMemo(
    () => (corpus ? Object.keys(corpus).sort() : []),
    [corpus]
  );

  const availableYears: number[] = useMemo(() => {
    if (!corpus) return [];
    if (selectedCompany && corpus[selectedCompany]) {
      return [...corpus[selectedCompany]].sort((a, b) => b - a);
    }
    const allYears = new Set<number>();
    Object.values(corpus).forEach((years) =>
      years.forEach((y) => allYears.add(y))
    );
    return Array.from(allYears).sort((a, b) => b - a);
  }, [corpus, selectedCompany]);

  const handleCompanyChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newCompany = e.target.value;
    setSelectedCompany(newCompany);
    if (newCompany && corpus && corpus[newCompany]) {
      const yearNum = parseInt(selectedYear, 10);
      if (!corpus[newCompany].includes(yearNum)) {
        setSelectedYear("");
      }
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const parsedYear = selectedYear ? parseInt(selectedYear, 10) : undefined;

    onSubmit({
      question: question.trim(),
      tickers: selectedCompany ? [selectedCompany] : undefined,
      year: parsedYear,
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
            Company (Optional)
          </label>
          <select
            value={selectedCompany}
            onChange={handleCompanyChange}
            disabled={isLoading || isCorpusLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 text-sm bg-white"
          >
            <option value="">All Companies</option>
            {companies.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900 mb-1">
            Fiscal Year (Optional)
          </label>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            disabled={isLoading || isCorpusLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 text-sm bg-white"
          >
            <option value="">All Years</option>
            {availableYears.map((y) => (
              <option key={y} value={y.toString()}>
                {y}
              </option>
            ))}
          </select>
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
