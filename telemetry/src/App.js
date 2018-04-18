import React, { Component } from 'react';
import Telemetry from './services/telemetry';
import Input from './services/input';
import Tetris from './tetris';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.init();
  }

  init() {
    Telemetry.init();
    Input.init();
  }

  render() {
    return (
      <div className="App">
        <Tetris />
      </div>
    );
  }
}

export default App;
