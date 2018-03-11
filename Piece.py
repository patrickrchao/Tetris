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
import Constants
from collections import deque
np.random.seed(5)
class Piece:

    bag = deque()

    def __init__(self, current_piece_id,  offsets = None, origin = None,use_default =True):
        self.id = current_piece_id

        #Offsets is a 2x4 numpy matrix
        #Origin is a 2x1 numpy matrix
        if use_default:
            self.offsets = Constants.piece_offsets[self.id]
            self.origin = Constants.piece_origins[self.id]
        else:
        	self.offsets = offsets
        	self.origin = origin

        	


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
        if len(Piece.bag)<5:
            Piece.fillBag(7)
        return Piece(piece_id)

     #Initializes the bag of pieces given a bag size
    def fillBag(bag_size = 10):
        nextPieces = np.random.randint(1,8,bag_size).tolist()
        Piece.bag.extend(nextPieces)

