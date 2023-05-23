import React from "react";


function Safe({ url }) {
    const httpUrl = url.startsWith('http://') || url.startsWith('https://') ? url : `http://${url}`;
    return (
        <div className="safe">
            <h2 className="safe-title">Safe URL</h2>
            <a className ='safe-text' href={httpUrl} target="_blank" rel="noopener noreferrer">{url}</a> 
            <p className="safe-text">
                The URL is safe to browse.    
            </p>
            <div className="safe-icon">
                <span role="img" aria-label="safe">🔒</span>
            </div>
        </div>
    );
}

export default Safe;
