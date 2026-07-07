import { Box, Container } from "@mui/material";
import { Header } from "./components/Header";
import { CPUChart } from "./components/CPUChart";

export const App = () => {
  return (
    <Container>
      <Header
        title="CPU Monitor"
        description="Веб-сервис для мониторинга нагрузки процессора в реальном времени"
      />

      <Box>
        <CPUChart
          title="Мгновенная нагрузка"
          endpoint="cpu/instant"
          updateInterval={5000}
        />
        <CPUChart
          title="Усредненная нагрузка"
          endpoint="cpu/average"
          updateInterval={60000}
        />
      </Box>
    </Container>
  );
};
