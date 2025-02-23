import React from 'react';
import './Landing.css';
import 'bootstrap/dist/css/bootstrap.css';
import LoginButton from './LoginButton';

function Landing() {
    
    return (
        <div className="landing-container">
            <div className="overlay"></div>
            <div className="content">
                <h1 className="welcome-header">WELCOME</h1>
                <LoginButton />
            </div>
        </div>
    );
}

export default Landing;