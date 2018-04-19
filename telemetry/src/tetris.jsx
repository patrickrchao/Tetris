import React from 'react';
import Telemetry from './services/telemetry';
import { PIECE_ID_MAP, STAGING_ROWS } from './constants';

class Tetris extends React.Component {
  constructor(props) {
    super(props);
    this.grid = null;
  }

  componentDidMount() {
    Telemetry.addListener('gameframe', data => {
      this.onData(data.data);
    });
    // TODO animation frame stuff
  }

  render() {
    return <canvas id='game' 
              ref={$ => this.drawState = {
                $,
                ctx: $.getContext('2d')
              }} 
              width={355}
              height={705}
            />
  }

  onData(data) {
    if (this.drawing)
      return;
    this.drawing = true;
    this.grid = data.splice(2);
    this.draw();
    this.drawing = false;
  }

  draw() {
    const {ctx} = this.drawState;
    let x = 5;
    let y = 5;
    for (const row of this.grid) {
      for (const square of row) {
        const { color } = PIECE_ID_MAP[square];
        ctx.fillStyle = color;
        ctx.fillRect(x, y, 30, 30);
        x += 35;
      }
      y += 35;
      x = 0;
    }
  }
}

export default Tetris;