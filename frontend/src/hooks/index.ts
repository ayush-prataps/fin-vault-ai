"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { queryFinancialData, getCorpus } from "@/lib/api";
import { QueryRequest, CorpusMetadata } from "@/types";

export const useQueryFinancialData = () => {
  return useMutation({
    mutationFn: (request: QueryRequest) => queryFinancialData(request),
  });
};

export const useCorpusMetadata = () => {
  return useQuery<CorpusMetadata>({
    queryKey: ["corpus"],
    queryFn: getCorpus,
    staleTime: 1000 * 60 * 30,
  });
};
