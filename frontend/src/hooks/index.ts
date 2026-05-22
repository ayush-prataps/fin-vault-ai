"use client";

import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  queryFinancialData,
  healthCheck,
  getQueryHistory,
  clearQueryHistory,
} from "@/lib/api";
import { QueryRequest } from "@/types";

export const useQueryFinancialData = () => {
  return useMutation({
    mutationFn: (request: QueryRequest) => queryFinancialData(request),
  });
};

export const useHealthCheck = () => {
  return useQuery({
    queryKey: ["health"],
    queryFn: healthCheck,
    retry: 2,
    staleTime: 30000,
  });
};

/**
 * Hook for fetching backend query history
 */
export const useBackendQueryHistory = (token: string | null) => {
  const queryClient = useQueryClient();

  const { data: history = [], isLoading } = useQuery({
    queryKey: ["queryHistory", token],
    queryFn: () => {
      // Only make request if token is a valid non-empty string
      if (!token || typeof token !== "string" || token.trim().length === 0) {
        return Promise.resolve([]);
      }
      return getQueryHistory(token, 50);
    },
    enabled: !!(token && typeof token === "string" && token.trim().length > 0),
    staleTime: 60000, // 1 minute
  });

  const clearHistoryHandler = React.useCallback(() => {
    if (token && typeof token === "string" && token.trim().length > 0) {
      clearQueryHistory(token)
        .then(() => {
          // Refetch after clear
          queryClient.invalidateQueries({ queryKey: ["queryHistory", token] });
        })
        .catch((err: any) => console.warn("Failed to clear history:", err));
    }
  }, [token, queryClient]);

  return { history, isLoading, clearHistory: clearHistoryHandler };
};

// Memory preferences removed from frontend. No-op placeholder left intentionally.
