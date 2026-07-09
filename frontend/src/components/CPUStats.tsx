import { Box, Skeleton, Stack, Typography } from "@mui/material";
import { ErrorMessage } from "./ErrorMessage";
import { useCPUStats } from "../hooks/useCPUStats";

interface CPUStatsProps {
  threshold?: number;
}

export const CPUStats = ({ threshold = 80 }: CPUStatsProps) => {
  const { data, isLoading, isError, error } = useCPUStats(threshold);

  if (isLoading) {
    return <Skeleton variant="rounded" height={200} />;
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

  if (!data) {
    return <ErrorMessage message="Нет данных" />;
  }

  console.log(data);

  return (
    <Box sx={{ border: 2, borderRadius: 4, p: 4 }}>
      <Typography variant="h6">
        Статистика нагрузки процессора за последний час
      </Typography>
      <Typography>Минимальное значение: {data.min_load}%</Typography>
      <Typography>Максимальное значение: {data.max_load}%</Typography>
      <Typography>Среднее значение: {data.avg_load}%</Typography>
      <Typography>Медианное значение: {data.median_load}%</Typography>
      <Typography>
        Время выше порогового значения: {data.seconds_above_threshold} секунд
      </Typography>
    </Box>
  );
};
