// MyForm.jsx
import React from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

function Main() {
  const [url, setUrl] = React.useState('');
  const navigate = useNavigate();

  function handleChange(event){
    setUrl(event.target.value);
  }
  function handleClick() {
    const urlJson = { url: url };
    const urlJsonString = encodeURIComponent(JSON.stringify(urlJson));
    navigate(`/predict?data=${urlJsonString}`);
  };

  return (
    <div className='main-div'>
      <TextField
        label="Enter URL"
        variant="filled"
        size="large"
        value={url}
        onChange={handleChange}
        fullWidth
        style={{ marginBottom: '1rem' }}
      />
      <Button 
        variant="contained" 
        className='main-button'
        onClick={handleClick}>
        Predict
      </Button>
    </div>
  );
}

export default Main;
