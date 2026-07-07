export interface DataPoint {
  timestamp: string;
  value: number | null;
}

export type Endpoint = "cpu/instant" | "cpu/average";
