/**
 * Results View Component
 * Displays structured query results with multiple panels
 */

"use client";

import React from "react";
import { QueryResponse } from "@/types";
import { AlertCircle, CheckCircle2 } from "lucide-react";

interface ResultsViewProps {
  response: QueryResponse;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ response }) => {
  return (
    <div className="space-y-4">
      {/* Summary Panel */}
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Summary</h2>
        <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
          {response.analysis}
        </p>
        {response.contradictions_detected && (
          <div className="mt-4 flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-md">
            <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-medium text-amber-900">Contradictions Detected</h3>
              <p className="text-sm text-amber-800 mt-1">{response.contradictions_detected}</p>
            </div>
          </div>
        )}
      </div>

      {/* Metrics Panel (if numeric data exists) */}
      {response.numeric_data_count > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Metrics</h2>
          <p className="text-sm text-gray-600 mb-4">
            Live results from retrieval and narrative evidence
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="p-3 rounded-md bg-gray-50 border border-gray-200">
              <p className="text-xs font-medium text-gray-600">Structured data points</p>
              <p className="text-sm font-semibold text-gray-900 mt-1">
                {response.numeric_data_count}
              </p>
            </div>
            <div className="p-3 rounded-md bg-gray-50 border border-gray-200">
              <p className="text-xs font-medium text-gray-600">Narrative chunks</p>
              <p className="text-sm font-semibold text-gray-900 mt-1">
                {response.narrative_chunks_count}
              </p>
            </div>
            <div className="p-3 rounded-md bg-gray-50 border border-gray-200">
              <p className="text-xs font-medium text-gray-600">Latency</p>
              <p className="text-sm font-semibold text-gray-900 mt-1">
                {response.latency_ms} ms
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Evidence Panel (if narratives exist) */}
      {response.narrative_chunks_count > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Evidence</h2>
          <p className="text-sm text-gray-600 mb-4">
            {response.narrative_chunks_count} supporting narrative chunks
          </p>
          <div className="space-y-3">
            {response.sources.slice(0, 3).map((source, i) => (
              <div
                key={i}
                className="p-3 rounded-md bg-blue-50 border border-blue-200"
              >
                <p className="text-sm text-blue-900">
                  {source.section || "Earnings transcript excerpt"}
                </p>
                <p className="text-xs text-blue-700 mt-2">
                  {source.ticker} {source.doc_type} FY{source.year}
                  {source.similarity_score && ` · Relevance: ${(source.similarity_score * 100).toFixed(0)}%`}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Confidence Panel */}
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Confidence & Metadata</h2>
        <div className="space-y-3">
          <div>
            <label className="text-sm font-medium text-gray-600">Retrieval Mode</label>
            <p className="text-gray-900 font-semibold capitalize mt-1">
              {response.retrieval_mode}
            </p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-600">Model Used</label>
            <p className="text-gray-900 font-semibold mt-1">{response.model_used}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-600">Query Processed</label>
            <p className="text-gray-900 mt-1 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-green-600" />
              Successfully
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
