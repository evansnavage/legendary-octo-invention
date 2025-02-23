import React, { useState } from 'react';
import './App.css';
import CreateItem from './create-item/create-item';

function App() {
  return (
    <div className="App">
      <header>
        <p> Penits</p>
      </header>
      <CreateItem />
    </div>
  );
}

export default App;
