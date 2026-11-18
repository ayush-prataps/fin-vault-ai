"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { queryFinancialData, healthCheck } from "@/lib/api";
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
