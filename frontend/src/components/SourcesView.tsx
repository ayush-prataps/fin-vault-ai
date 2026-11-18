"use client";

import React, { useState } from "react";
import { Citation } from "@/types";
import { ChevronDown, ChevronUp, FileText } from "lucide-react";

interface SourcesViewProps {
  citations: Citation[];
}

export const SourcesView: React.FC<SourcesViewProps> = ({ citations }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="text-base font-semibold text-gray-900 mb-4">
        Citations ({citations.length})
      </h2>

      <div className="space-y-3">
        {citations.map((c) => {
          const isExpanded = expandedIndex === c.n;
          return (
            <div
              key={c.n}
              className="border border-gray-200 rounded-lg overflow-hidden bg-white"
            >
              <button
                onClick={() => setExpandedIndex(isExpanded ? null : c.n)}
                className="w-full px-4 py-3 text-left flex items-center justify-between gap-3 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 text-blue-800 text-xs font-semibold">
                    [{c.n}]
                  </span>
                  <FileText className="w-4 h-4 text-gray-500" />
                  <span className="font-medium text-sm text-gray-900">
                    {c.company} — {c.doc} (FY{c.year})
                  </span>
                  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded">
                    Page {c.page}
                  </span>
                </div>
                {isExpanded ? (
                  <ChevronUp className="w-4 h-4 text-gray-400" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-gray-400" />
                )}
              </button>

              {isExpanded && (
                <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
                  <pre className="text-xs text-gray-800 whitespace-pre-wrap font-mono leading-relaxed">
                    {c.text}
                  </pre>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
