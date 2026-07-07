import { Alert, Box } from "@mui/material";

interface ErrorMessageProps {
  message: string;
}

export const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <Box sx={{ my: 4 }}>
      <Alert severity="error">{message}</Alert>
    </Box>
  );
};
