import React, { memo } from 'react';

import UploadFile from "./components/UploadFile/UploadFIle";

import logo from './assets/image/bankExampleIcon.jpeg';

import './App.css';

const App = () => {
  return (
    <div className="App">
      <div className="App-container">
        <img
          src={logo}
          className="App-logo"
          alt="logo"
        />
        <UploadFile />
      </div>
    </div>
  );
}

export default memo(App);
