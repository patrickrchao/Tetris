# Patrick Chao and Dillon Yao
# 3/10/18
# TETRIS
# Tetris.py

# High level tetris game manager


import time
from GameState import GameState
import Constants

class Tetris:
    TIMESTEP = Constants.timestep

    def __init__(self):
        self.game_state = GameState()

    def begin(self):
        accumulator = 0
        last = time.time()
        while True:
            curr = time.time()
            frame_time = curr - last
            last = curr
            accumulator += frame_time
            while accumulator >= self.TIMESTEP:
                self.handle_input()
                self.update(self.TIMESTEP)
                accumulator -= self.TIMESTEP

    def handle_input(self):
        self.game_state.handle_input()

    def update(self,dt):
        self.game_state.update(dt)
