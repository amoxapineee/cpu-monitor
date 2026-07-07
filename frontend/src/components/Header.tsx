import { Box, Typography } from "@mui/material";

interface HeaderProps {
  title: string;
  description?: string;
}

export const Header = ({ title, description }: HeaderProps) => {
  return (
    <Box sx={{ border: 4, borderRadius: 4, px: 4, py: 2, mb: 3 }}>
      <Typography>{title}</Typography>
      {description && <Typography>{description}</Typography>}
    </Box>
  );
};
