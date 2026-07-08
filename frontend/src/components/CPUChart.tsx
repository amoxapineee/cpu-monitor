import { Box, Skeleton, Typography } from "@mui/material";
import { useCPUData } from "../hooks/useCPUData";
import type { CPULoadParameter } from "../types";
import { ErrorMessage } from "./ErrorMessage";
import { LineChart } from "@mui/x-charts";

interface CPUChartProps {
  title: string;
  endpoint: CPULoadParameter;
  updateInterval?: number;
}

export const CPUChart = ({
  title,
  endpoint,
  updateInterval,
}: CPUChartProps) => {
  const { data, loading, error } = useCPUData(endpoint, updateInterval);

  if (loading) {
    return <Skeleton />;
  }
  if (error) {
    return <ErrorMessage message="Ошибка загрузки данных" />;
  }

  const timestamps = data.map((d) => new Date(d.timestamp));
  const values = data.map((d) => d.value);

  return (
    <Box sx={{ border: 2, borderRadius: 4, my: 1, py: 1 }}>
      <Typography sx={{ pl: 14 }}>{title}</Typography>
      <LineChart
        xAxis={[{ data: timestamps, scaleType: "time" }]}
        series={[{ data: values, color: "#444444" }]}
        height={400}
        grid={{ vertical: true, horizontal: true }}
      />
    </Box>
  );
};
