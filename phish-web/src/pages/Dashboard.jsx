import React from "react";
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css";
import ResponsiveAppBar from "../components/Appbar";
import Footer from "../components/Footer";

function Dashboard() {
    return (
        <div>
            <ResponsiveAppBar />
            <h1>Dashboard</h1>
            <h2>Trained Model Metric</h2>
            <Carousel showArrows={true} emulateTouch={true}>
                <div className="carousel-item">
                    <img className="carousel-image" src="assets/images/confusion_matrix.png" alt="Confusion Matrix"/>
                    <p className="legend">Confusion Matrix</p>
                </div>
                <div className="carousel-item">
                    <img className="carousel-image" src="assets/images/classification_report.png" alt="Classification Report"/>
                    <p className="legend">Classification Report</p>
                </div>
                <div className="carousel-item">
                    <img className="carousel-image" src="assets/images/roc_curve.png" alt="ROC curve"/>
                    <p className="legend">ROC Curve</p>
                </div>
            </Carousel>
            <Footer />
        </div>
    )
}

export default Dashboard;
