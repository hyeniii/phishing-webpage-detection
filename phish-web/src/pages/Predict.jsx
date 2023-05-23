import React from "react";
import { useLocation } from "react-router-dom";
import ResponsiveAppBar from "../components/Appbar";
import Footer from "../components/Footer";
import Safe from "../components/Safe";
import Phish from "../components/Phish";

function Predict() {
    const location = useLocation();
  const { predictionData, url } = location.state;
  const { prediction } = predictionData;

    return (
        <div>
            <ResponsiveAppBar />
            <h1>Predicted result</h1>
            {prediction === 0 ? <Safe url={url} /> : <Phish url={url} />}
            <Footer />
        </div>
    );
}

export default Predict;
