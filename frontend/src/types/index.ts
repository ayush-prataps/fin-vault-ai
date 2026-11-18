export interface Citation {
  n: number;
  company: string;
  doc: string;
  year: number;
  page: number;
  text: string;
}

export interface QueryRequest {
  question: string;
  tickers?: string[];
  year?: number;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  model: string;
  latency_ms: number;
  tokens: number;
}
