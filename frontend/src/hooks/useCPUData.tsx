import type { CPULoadParameter } from "../types";
import { fetchCPULoad } from "../api";
import { useQuery } from "@tanstack/react-query";

export const useCPUData = (
  type: CPULoadParameter,
  updateInterval: number = 5000,
) => {
  return useQuery({
    queryKey: ["load", type, updateInterval],
    queryFn: () => fetchCPULoad(type),
    refetchInterval: 5000,
  });
};
