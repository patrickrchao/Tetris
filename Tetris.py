# Patrick Chao and Dillon Yao
# 3/10/18
# TETRIS
# Tetris.py

# High level tetris game manager


import time
from GameState import GameState
from telemetry import Telemetry
from input_game import Input
import Constants

from ModelInput import ModelInput
from HeuristicModel import HeuristicModel



class Services:
    def __init__(self, input, telemetry):
        self.input = input
        self.telemetry = telemetry

class Tetris:
    TIMESTEP = Constants.timestep
    if Constants.use_model:
        TIMESTEP = Constants.model_timestep
    def __init__(self, socket, sid):
        telemetry = Telemetry(socket, sid)
        if Constants.use_model:
            input = ModelInput(HeuristicModel())
        else:
            input = Input(telemetry)
        self.game_state = GameState(Services(input, telemetry))
        self.terminate = False

    def begin(self):
        accumulator = 0
        last = time.time()
        while not self.terminate:
            curr = time.time()
            frame_time = curr - last
            last = curr
            accumulator += frame_time
            while accumulator >= self.TIMESTEP:
                self.handle_input()
                self.update(self.TIMESTEP)
                accumulator -= self.TIMESTEP

    def end(self):
        self.terminate = True

    def handle_input(self):
        self.game_state.handle_input()

    def update(self,dt):
        self.game_state.update(dt)
