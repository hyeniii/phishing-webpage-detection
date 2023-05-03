import React from "react";
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from "./pages/Dashboard";
import Predict from "./pages/Predict";

function App() {
  
  return (
    <>
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/predict" element={<Predict />} />
       </Routes>
    </>
  );
}

export default App;