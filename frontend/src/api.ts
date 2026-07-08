import type { DataPoint, CPULoadParameter } from "./types";

const API_BASE = "http://localhost:8000/api";

export const fetchCPULoad = async (
  endpoint: CPULoadParameter,
): Promise<DataPoint[]> => {
  const response = await fetch(`${API_BASE}/cpu/load?type=${endpoint}`);
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
};
