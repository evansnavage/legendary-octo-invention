import React, { Component } from 'react';
import { stack as Menu } from 'react-burger-menu'
import './sidemenu.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

class SideMenu extends React.Component {
  showSettings (event) {
    event.preventDefault();
  }

  render () {
    return (
    <div>
      <Menu>
      <div id="add" className="menu-item">
            <a id="add" className="butt-large"><FontAwesomeIcon icon="fa-solid fa-plus" /></a>
            Create
        </div>
        <div id="dashboard" className="menu-item">
            <a id="dashboard" className="butt"><FontAwesomeIcon icon="fa-solid fa-chart-pie" /></a>
            Dashboard
        </div>
        <div id="inventory" className="menu-item">
            <a id="inventory" className="butt"><FontAwesomeIcon icon="fa-solid fa-warehouse" /></a>
            Inventory
        </div>
        <div id="events" className="menu-item">
            <a id="events" className="butt"><FontAwesomeIcon icon="fa-solid fa-face-smile" /></a>
            Events
        </div>

        <div id="home" className="menu-item">
            <a id="settings" className="butt"><FontAwesomeIcon icon="fa-solid fa-gear" /></a>
            Settings
        </div>
      </Menu>
      </div>
    );
  }  
}
export default SideMenu;
