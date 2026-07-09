import { useState } from "react";
import {
  Box,
  Stack,
  TextField,
  Button,
  Alert,
  Snackbar,
  Divider,
} from "@mui/material";
import { NumericFormat } from "react-number-format";
import { clearDB } from "../api";

interface ControlsPanelProps {
  threshold: number;
  onThresholdChange: (value: number) => void;
  onLoadStats: () => void;
}

export const ControlPanel = ({
  threshold,
  onThresholdChange,
}: ControlsPanelProps) => {
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: "success" | "error" | "info";
  }>({
    open: false,
    message: "",
    severity: "info",
  });

  const handleClearDB = async () => {
    try {
      await clearDB();
      setSnackbar({
        open: true,
        message: `База данных очищена`,
        severity: "success",
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: `Ошибка очистки БД: ${error instanceof Error ? error.message : "Неизвестная ошибка"}`,
        severity: "error",
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }));
  };

  return (
    <Box sx={{ border: 2, borderRadius: 4, padding: 4 }}>
      <Stack spacing={4}>
        <NumericFormat
          customInput={TextField}
          label="Пороговое значение, %"
          value={threshold}
          onValueChange={(value) => {
            onThresholdChange(value.floatValue);
          }}
          isAllowed={(value) => {
            const { floatValue } = value;
            return (
              floatValue === undefined || (floatValue > 0 && floatValue < 100)
            );
          }}
        />

        <Divider />

        <Button variant="outlined" color="error" onClick={handleClearDB}>
          Очистить БД
        </Button>
      </Stack>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};
