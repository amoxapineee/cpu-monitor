import { Box, Skeleton, Typography } from "@mui/material";
import { useCPUData } from "../hooks/useCPUData";
import type { CPULoadParameter } from "../types";
import { ErrorMessage } from "./ErrorMessage";
import { LineChart } from "@mui/x-charts";

interface CPUChartProps {
  title: string;
  endpoint: CPULoadParameter;
  updateInterval?: number;
  threshold?: number;
}

export const CPUChart = ({
  title,
  endpoint,
  updateInterval,
  threshold,
}: CPUChartProps) => {
  const { data, isLoading, isError, error } = useCPUData(
    endpoint,
    updateInterval,
  );

  if (isLoading) {
    return <Skeleton />;
  }
  if (isError) {
    return (
      <ErrorMessage
        message={
          error instanceof Error ? error.message : "Ошибка загрузки данных"
        }
      />
    );
  }

  const timestamps = data.map((d) => new Date(d.timestamp));
  const values = data.map((d) => d.value);

  const filteredValues = values.filter((value) => value !== null);
  if (
    !filteredValues.some((value) => value <= threshold) ||
    !filteredValues.some((value) => value >= threshold)
  ) {
    threshold = null;
  }

  return (
    <Box sx={{ border: 2, borderRadius: 4, py: 1 }}>
      <Typography sx={{ pl: 14 }}>{title}</Typography>
      <LineChart
        xAxis={[{ data: timestamps, scaleType: "time" }]}
        series={[
          { label: "Нагрузка, %", data: values, color: "#444444" },
          {
            label: "Порог",
            data: timestamps.map(() => threshold),
            color: "#FF0000",
          },
        ]}
        height={400}
        grid={{ vertical: true, horizontal: true }}
      />
    </Box>
  );
};
