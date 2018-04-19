export const PIECE_ENUM = {
  EMPTY: {
    color: '#000000'
  },
  I: {
    color: '#3399ff',
    sprite: ''
  },
  J: {
    color: '#0000ff',
    sprite: ''
  },
  L: {
    color: '#ff9900',
    sprite: ''
  },
  O: {
    color: '#ffff00',
    sprite: ''
  },
  S: {
    color: '#00cc00',
    sprite: ''
  },
  T: {
    color: '#cc33ff',
    sprite: ''
  },
  Z: {
    color: '#ff0000',
    sprite: ''
  }
}

export const PIECE_ID_MAP = {
  0: PIECE_ENUM.EMPTY,
  1: PIECE_ENUM.I,
  2: PIECE_ENUM.J,
  3: PIECE_ENUM.L,
  4: PIECE_ENUM.O,
  5: PIECE_ENUM.S,
  6: PIECE_ENUM.T,
  7: PIECE_ENUM.Z
};

export const BOARD_ROWS = 20;
export const BOARD_COLS = 10;
export const STAGING_ROWS = 2;
export const BAG_SIZE = 5;
export const TIMESTEP = 0.01;

export const DRAW_OFFSET = 0.1;
