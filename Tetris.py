# Patrick Chao and Dillon Yao
# 3/10/18
# TETRIS
# Tetris.py

# High level tetris game manager


import time
from GameState import GameState

class Tetris:
    TIMESTEP = 0.01
    input_value = ""
    key_logger = {}

    def __init__(self):
        self.game_state = GameState()
        self.begin()

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
        input_value = "ArrowDown"
        self.key_logger[input_value] = True

    def update(self,dt):
        self.game_state.update(dt)

        for key in self.key_logger.keys():
            if key != "None":
                if self.key_logger[key] == True:
                    self.game_state.keyAction(key,dt)
                    self.key_logger[key] == False
        


if __name__ == '__main__':
    Tetris()
