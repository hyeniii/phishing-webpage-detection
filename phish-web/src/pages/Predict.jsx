import React from "react";
import { useLocation } from "react-router-dom";
import ResponsiveAppBar from "../components/Appbar";
import Footer from "../components/Footer";

function Predict() {
    const location = useLocation();
    const predictionData = location.state.predictionData;
    const { prediction } = predictionData;

    return (
        <div>
            <ResponsiveAppBar />
            <h1>Predicted result</h1>
            <p>The entered URL is {prediction === 0 ? 'safe' : 'phish'}</p>
            <Footer />
        </div>
    );
}

export default Predict;
