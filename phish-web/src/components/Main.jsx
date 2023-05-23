import React from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import { useNavigate } from 'react-router-dom';

function Main() {
  const [url, setUrl] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const navigate = useNavigate();

  const handleChange = (event) => {
    setUrl(event.target.value);
  };

  const handleClick = async () => {
    const urlJson = { url: url };
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(urlJson),
      });
      if (response.ok) {
        const predictionData = await response.json();
        console.log(predictionData)
        navigate('/predict', { state: { predictionData } });
      } else if (response.status === 405) {
        console.error("Method Not Allowed:", response.status);
        // Handle the Method Not Allowed error appropriately
      } else {
        console.error("Error while fetching prediction:", response.status);
        navigate('/');
      }
    } catch (error) {
      console.error("Error while fetching prediction:", error);
      navigate('/');
    } finally {
      setLoading(false);
    }
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
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} color="inherit" /> : 'Predict'}
      </Button>
    </div>
  );
}

export default Main;
