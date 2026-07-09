import axios from "axios";
import type { DataPoint, CPULoadParameter, CPUStatistic } from "./types";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const fetchCPULoad = async (
  type: CPULoadParameter,
): Promise<DataPoint[]> => {
  const { data } = await api.get("/cpu/load", { params: { type } });
  return data;
};

export const fetchCPUStats = async (
  threshold: number,
): Promise<CPUStatistic> => {
  const { data } = await api.get("/cpu/stats", { params: { threshold } });
  return data;
};

export const clearDB = async (): Promise<void> => {
  await api.delete("/db/clear");
};
