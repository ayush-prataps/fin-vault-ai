"use client";

import { useMutation } from "@tanstack/react-query";
import { queryFinancialData } from "@/lib/api";
import { QueryRequest } from "@/types";

export const useQueryFinancialData = () => {
  return useMutation({
    mutationFn: (request: QueryRequest) => queryFinancialData(request),
  });
};
