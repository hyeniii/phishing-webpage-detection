import React from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

function Main() {
  // url used for phishing
  const [url, setUrl] = React.useState('');
  const navigate = useNavigate();

  function handleChange(event){
    // textfield value
    setUrl(event.target.value);
  }
  async function handleClick() {
    // url passed as data when button is clicked
    const urlJson = { url: url };
    const urlJsonString = encodeURIComponent(JSON.stringify(urlJson));

    try {
      const response = await fetch("https://d4a7leuot6.execute-api.us-east-2.amazonaws.com/default/phish-inference", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
      body: JSON.stringify(urlJson),
      });
      if (response.ok) {
        const data = await response.json();
        navigate(`/predict?data=${urlJsonString}`, {state: {predictionData: data}});
      } else {
        console.error("Error while fetching predition:", response.status)
      }
    } catch (error) {
      console.error("Error:", error)
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
        onClick={handleClick}>
        Predict
      </Button>
    </div>
  );
}

export default Main;
