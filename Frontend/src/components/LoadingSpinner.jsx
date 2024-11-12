import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';


const LoadingSpinner = ({ message = 'Caricamento in corso...', size = 40 }) => {
  return (
    <div className="loading-spinner">
      <CircularProgress size={size} />
      <p className="loading-text">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
