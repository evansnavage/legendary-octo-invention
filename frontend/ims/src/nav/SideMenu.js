import React, { Component } from 'react';
import { stack as Menu } from 'react-burger-menu'
import './sidemenu.css'
import { Button } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

class SideMenu extends React.Component {
  showSettings (event) {
    event.preventDefault();
  }

  render () {
    return (
    <div>
      <Menu>
        <div id="home" className="menu-item">
            <a className="dash-butt"><FontAwesomeIcon icon="fa-solid fa-chart-pie" /></a>
            Dashboard
        </div>
        <a id="about" className="menu-item" href="/about">About</a>
        <a id="contact" className="menu-item" href="/contact">Contact</a>
        <a onClick={ this.showSettings } className="menu-item--small" href="">Settings</a>
      </Menu>
      </div>
    );
  }  
}
export default SideMenu;
