// MyForm.jsx
import React from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function Main() {
  return (
    <div className='main-div'>
      <TextField
        label="Enter URL"
        variant="filled"
        size="large"
        fullWidth
        style={{ marginBottom: '1rem' }}
      />
      <Button variant="contained" className='main-button'>
        Predict
      </Button>
    </div>
  );
}

export default Main;
