"use client";

import React from "react";
import { QueryResponse } from "@/types";

interface ResultsViewProps {
  response: QueryResponse;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ response }) => {
  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between pb-3 border-b border-gray-100">
          <h2 className="text-base font-semibold text-gray-900">Answer</h2>
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span>Model: <strong className="text-gray-700">{response.model}</strong></span>
            <span>Latency: <strong className="text-gray-700">{response.latency_ms}ms</strong></span>
            <span>Tokens: <strong className="text-gray-700">{response.tokens}</strong></span>
          </div>
        </div>
        <p className="mt-4 text-gray-800 leading-relaxed whitespace-pre-wrap font-sans text-sm">
          {response.answer}
        </p>
      </div>
    </div>
  );
};
