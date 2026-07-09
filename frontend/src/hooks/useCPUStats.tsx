import { useQuery } from "@tanstack/react-query";
import { fetchCPUStats } from "../api";
import type { CPUStatistic } from "../types";

export const useCPUStats = (threshold: number) => {
  return useQuery<CPUStatistic>({
    queryKey: ["stats", threshold],
    queryFn: () => fetchCPUStats(threshold),
    refetchInterval: 5000,
  });
};
