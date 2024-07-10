import { Button, Box, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Welcome = () => {
  const navigate = useNavigate();

  const handleGoToProducts = () => {
    navigate('/products');
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
      textAlign="center"
    >
      <Typography variant="h3" gutterBottom>
        Welcome to the Shopping App
      </Typography>
      <Button variant="contained" onClick={handleGoToProducts}>
        Manage Products
      </Button>
    </Box>
  );
};

export default Welcome;
