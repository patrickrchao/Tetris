import React, { Component } from 'react';
import Telemetry from './services/telemetry';
import Input from './services/input';
import './App.css';

class Grid extends Component {
  constructor(props) {
    super(props);
    this.state = {
      grid: []
    }
  }

  render() {
    const {grid} = this.state;
    const rows = grid.map((r, i) => <div key={i}>{r}</div>)

    return (
      <div className='grid'>
        {rows}
      </div>
    );
  }

  componentDidMount() {
    Telemetry.addListener('gameframe', (data) => {
      let text = data.data.map(r => r.join(' '));
      this.setState({ grid: text })
    })
  }
}

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
        <Grid />
      </div>
    );
  }
}

export default App;
