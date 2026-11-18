"use client";

import React, { useState } from "react";
import { QueryPanel, ResultsView, SourcesView } from "@/components";
import { useQueryFinancialData } from "@/hooks";
import { QueryRequest, QueryResponse } from "@/types";

export default function Home() {
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { mutate: queryData, isPending } = useQueryFinancialData();

  const handleSubmit = (request: QueryRequest) => {
    setError(null);
    setResponse(null);

    queryData(request, {
      onSuccess: (data) => {
        setResponse(data);
      },
      onError: (err: Error) => {
        setError(err.message || "Query failed. Please try again.");
      },
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white border-b border-gray-200">
        <div className="mx-auto max-w-4xl px-4 py-4 sm:px-6">
          <h1 className="text-xl font-bold text-gray-900">FinVault AI</h1>
          <p className="text-xs text-gray-500">
            Factual QA over SEC filings with page-level citations
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 space-y-6">
        <QueryPanel onSubmit={handleSubmit} isLoading={isPending} />

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
            {error}
          </div>
        )}

        {response && (
          <>
            <ResultsView response={response} />
            <SourcesView citations={response.citations} />
          </>
        )}
      </main>
    </div>
  );
}
