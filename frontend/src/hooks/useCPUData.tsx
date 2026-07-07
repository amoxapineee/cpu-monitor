import { useState, useEffect, useCallback } from "react";
import type { DataPoint, Endpoint } from "../types";
import { fetchCPUData } from "../api";

interface UseCPUDataResult {
  data: DataPoint[];
  loading: boolean;
  error: Error | null;
}

export const useCPUData = (
  endpoint: Endpoint,
  updateInterval: number = 5000,
): UseCPUDataResult => {
  const [data, setData] = useState<DataPoint[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const result = await fetchCPUData(endpoint);
      setData(result);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, updateInterval);
    return () => clearInterval(interval);
  }, [fetchData, updateInterval]);

  return { data, loading, error };
};
