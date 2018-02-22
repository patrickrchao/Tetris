# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# MACHINEEEEEEE LEARNINGGG
# GameState.py

#Contains the game state variables
#Tetris Game Logic

import numpy as np
from collections import deque



board_rows = 20
board_columns = 10
bag_size = 5 


class GameState:
	def __init__(self):
		self.grid = np.zeros((board_rows+2,board_columns))
		self.flatGrid = flattenGrid(self.grid)
		self.bag_of_pieces = deque()
		self.bag_of_pieces = self.refillBag(bag_size) #deque of piece ideas
		self.current_piece = self.getNextPiece()
		self.held_piece = 0
		self.score = 0

	#Flattens the grid
	def flattenGrid(grid):
		return grid.flatten()

	# Using the bag of pieces, returns an instance of the next piece
	# Adds another piece to the bag
	def getNextPiece():
		#TODO 
		piece_id = bag_of_pieces.popleft()
		if len(deque)<5:
			fillBag(5)
		#if bag is getting almost empty, refill bag

	# Given a piece id, this returns an instance of the piece class
	def generatePiece(piece_id):
		return Piece(piece_id)
		
 	#Initializes the bag of pieces given a bag size
	def fillBag(bag_size = 10):
		nextPieces = np.random.randint(1,8,bag_size).tolist()
		self.bag_of_pieces.extend(nextPieces)

	#Still temporary
	#Given an action, attempts to perform the action
	def keyAction(key): 
		if key == 'ArrowLeft':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.LEFT) )
        elif key == 'ArrowRight':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.RIGHT))
        elif key == 'ArrowUp' or key == "C":
            self.attemptAction(lambda piece: Piece.rotate(piece, DIRS.CLOCKWISE))
        elif key == 'Z':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.COUNTERCLOCKWISE))
        elif key == 'ArrowDown':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.DOWN))
        elif key == 'Shift':
            self.holdPiece()
        elif key == 'Space':
            self.hardDrop()
        else:
        	return

    def attemptAction(action):
    	test_piece = Piece.copy(self.current_piece)
        action(test_piece)
        success = self.collides(test_piece)
        if success:
            action(self.current_piece)
        return success;



    #Check if a piece collides or is out of bounds
    def collides(piece):    
    	piece_coordinates = piece.origin + piece.offsets

    	#Check if out of board range
    	piece_row_max = np.amax(piece_coordinates[0])
    	piece_row_min = np.amin(piece_coordinates[0])
    	piece_col_max = np.amax(piece_coordinates[1])
    	piece_col_min = np.amin(piece_coordinates[1])

    	if piece_row_min < boardRows and piece_row_min >= 0:
    		if piece_col_max < boardColumns and piece_col_min >= 0:
    			#Check if piece is valid in location
    			transformed_coordinates = np.array([[1,board_columns]]) @ piece_coordinates 
    			grid_values = np.take(self.flatGrid,transformedCoordinates)
    			if np.sum(grid_values)==0:
    				return True
    	return False

    #Check if line needs to be cleared based on current piece
    def checkClear():

    def clearLine(row):

    def incrementScore():

    def holdPiece():


	def generateJSON():
		# TODO

