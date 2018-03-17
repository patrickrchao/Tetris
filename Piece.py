# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# MACHINEEEEEEE LEARNINGGG
# Piece.py

# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# Piece.py
# Contains the Piece game logic

import numpy as np
import random
import Constants
from collections import deque
np.random.seed(1)
random.seed(1)
class Piece:

    bag = deque()

    def __init__(self, current_piece_id,  offsets = None, origin = None,use_default =True):
        self.id = current_piece_id

        #Offsets is a 2x4 numpy matrix
        #Origin is a 2x1 numpy matrix
        if use_default:
            self.offsets = np.copy(Constants.piece_offsets[self.id])
            self.origin = np.copy(Constants.piece_origins[self.id])
        else:
        	self.offsets = np.copy(offsets)
        	self.origin = np.copy(origin)



    def move(self, direction):
        self.origin += direction

    def rotate(self, rotationMatrix):
        self.offsets = rotationMatrix @ self.offsets

    def copy(piece):
        return Piece(piece.id, piece.offsets.copy(), piece.origin.copy(),False)

    # Using the bag of pieces, returns an instance of the next piece
    # Adds another piece to the bag
    def getNextPiece():
        piece_id = Piece.bag.popleft()
        #if bag is getting almost empty, refill bag
        if len(Piece.bag)<=6:
            Piece.fillBag()
        return Piece(piece_id)

     #Initializes the bag of pieces given a bag size
    def fillBag():
        nextPieces = np.arange(1,8).tolist()
        random.shuffle(nextPieces)
        Piece.bag.extend(nextPieces)

