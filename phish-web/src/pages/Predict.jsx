import React from "react";
import ResponsiveAppBar from "../components/Appbar";
import Footer from "../components/Footer"
import { useSearchParams } from 'react-router-dom';

function Predict() {
    const [searchParams] = useSearchParams();
    const data = searchParams.get('data');
    const urlJson = JSON.parse(decodeURIComponent(data));
    const { url } = urlJson;
    return (
        <div>
            <ResponsiveAppBar />
            <h1>Predicted result</h1>
            <p>Entered URL: {url}</p>
            <Footer />
        </div>
    )
}

export default Predict