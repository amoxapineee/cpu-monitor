import type { DataPoint, Endpoint } from "./types";

const API_BASE = "http://localhost:8000/api";

export const fetchCPUData = async (
  endpoint: Endpoint,
): Promise<DataPoint[]> => {
  const response = await fetch(`${API_BASE}/${endpoint}`);
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
};
