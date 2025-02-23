import React, { Component } from 'react';
import './nav.css';
import SideMenu from './SideMenu.js';

class Navigation extends Component {
    render() {
        return (
            <div className="container">
                <div className="header-container">
                    <div className="left-nav"><SideMenu/></div>
                    <div className="top-header"></div>
                </div>
                <div className="content-area">
                    <div className="main-content">
                        sfklasbjkbjkasfbasjkfjk
                    </div>
                </div>
            </div>
        );
    }
}

export default Navigation;
