import axios, { AxiosError } from "axios";
import { QueryRequest, QueryResponse, CorpusMetadata } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const queryFinancialData = async (
  request: QueryRequest
): Promise<QueryResponse> => {
  try {
    const response = await apiClient.post<QueryResponse>("/query", request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      const detail =
        typeof axiosError.response?.data === "object" && axiosError.response?.data
          ? (axiosError.response.data as { detail?: string }).detail || axiosError.message
          : axiosError.message;
      throw new Error(detail || "Query request failed");
    }
    throw error;
  }
};

export const getCorpus = async (): Promise<CorpusMetadata> => {
  const response = await apiClient.get<CorpusMetadata>("/corpus");
  return response.data;
};

export default apiClient;
