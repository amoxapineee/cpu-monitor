import { Container, Grid, Stack } from "@mui/material";
import { CPUChart } from "./components/CPUChart";
import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { ControlPanel } from "./components/ControlPanel";
import { CPUStats } from "./components/CPUStats";

export const App = () => {
  const queryClient = useQueryClient();
  const [threshold, setThreshold] = useState<number>(() => {
    const saved = localStorage.getItem("threshold");
    return saved ? parseFloat(saved) : 80;
  });

  const handleLoadStats = () => {
    queryClient.invalidateQueries({ queryKey: ["stats", threshold] });
  };

  useEffect(() => localStorage.setItem("threshold", String(threshold)));

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Grid container spacing={4}>
        <Grid size={{ xs: 12, md: 8 }}>
          <Stack spacing={4}>
            <CPUChart
              title="Мгновенная нагрузка"
              endpoint="instant"
              updateInterval={5000}
              threshold={threshold}
            />
            <CPUChart
              title="Усредненная нагрузка"
              endpoint="average"
              updateInterval={60000}
              threshold={threshold}
            />
          </Stack>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Stack spacing={4}>
            <CPUStats threshold={threshold} />
            <ControlPanel
              threshold={threshold}
              onThresholdChange={setThreshold}
              onLoadStats={handleLoadStats}
            />
          </Stack>
        </Grid>
      </Grid>
    </Container>
  );
};
