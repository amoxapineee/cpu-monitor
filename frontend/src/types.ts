export interface DataPoint {
  timestamp: string;
  value: number | null;
}

export type CPULoadParameter = "instant" | "average";

export interface CPUStatistic {
  min_load: number;
  max_load: number;
  avg_load: number;
  median_load: number;
  seconds_above_threshold: number;
}
