export interface DataPoint {
  timestamp: string;
  value: number | null;
}

export type CPULoadParameter = "instant" | "average";
