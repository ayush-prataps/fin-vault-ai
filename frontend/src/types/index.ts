/**
 * API Types for FinVault AI Backend Integration
 */

export interface QueryRequest {
  query: string;
  mode: "quick" | "deep";
  tickers?: string[];
  retrieval_mode?: "numeric" | "narrative" | "hybrid";
}

export interface SourceReference {
  doc_type: string;
  ticker: string;
  year: number;
  section?: string;
  similarity_score?: number;
}

export interface QueryResponse {
  query: string;
  analysis: string;
  retrieval_mode: string;
  model_used: string;
  numeric_data_count: number;
  narrative_chunks_count: number;
  sources: SourceReference[];
  latency_ms: number;
  tokens_used?: number;
  retrieval_latency_ms?: number;
  llm_latency_ms?: number;
  contradictions_detected?: string;
}
export interface QueryHistoryItem {
  id: number;
  query: string;
  mode: string;
  retrieval_mode: string;
  analysis?: string;
  model_used?: string;
  latency_ms?: number;
  tokens_used?: number;
  retrieval_latency_ms?: number;
  llm_latency_ms?: number;
  created_at: string;
}
