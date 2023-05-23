import React from "react";


function Phish({ url }) {
    return (
        <div className="phish">
            <h2 className="alert-title">Phishing Alert!</h2>
            <p className="alert-text">The URL is suspected to be a phishing site.</p>
            <p className="alert-text">{url}</p>
            <div className="alarm-animation">
                <span role="img" aria-label="alarm">⚠️</span>
            </div>
        </div>
    );
}

export default Phish;
