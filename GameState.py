# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# MACHINEEEEEEE LEARNINGGG
# GameState.py

#Contains the game state variables
#Tetris Game Logic

import numpy as np
from collections import deque
import Piece


board_rows = 20
board_columns = 10
bag_size = 5 


class GameState:
	def __init__(self):
		self.grid = np.zeros((board_rows+2,board_columns))
		self.flat_grid = flattenGrid(self.grid)
		self.current_piece = Piece.getNextPiece()
		self.held_piece = 0
		self.score = 0
		self.down_state = False
		self.can_hold = True

	#Flattens the grid
	def flattenGrid(self, grid):
		return grid.flatten()

	#Still temporary
	#Given an action, attempts to perform the action
	def keyAction(self, key): 


		if key == 'ArrowLeft':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.LEFT) )
        elif key == 'ArrowRight':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.RIGHT))
        elif key == 'ArrowUp' or key == "C":
            self.attemptAction(lambda piece: Piece.rotate(piece, DIRS.CLOCKWISE))
        elif key == 'Z':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS.COUNTERCLOCKWISE))
        elif key == 'ArrowDownReleased':
            self.down_state = False
        elif key == 'ArrowDown':
            self.down_state = True
        elif key == 'Shift':
            self.holdPiece()
        elif key == 'Space':
            self.hardDrop()
        else:
        	return

    def attemptAction(self, action):
    	test_piece = Piece.copy(self.current_piece)
        action(test_piece)
        success = self.collides(test_piece)
        if success:
            action(self.current_piece)
        return success;



    #Check if a piece collides or is out of bounds
    def collides(self, piece):    
    	piece_coordinates = piece.origin + piece.offsets

    	#Check if out of board range
    	piece_row_max = np.amax(piece_coordinates[0])
    	piece_row_min = np.amin(piece_coordinates[0])
    	piece_col_max = np.amax(piece_coordinates[1])
    	piece_col_min = np.amin(piece_coordinates[1])

    	if piece_row_min < board_rows and piece_row_min >= 0:
    		if piece_col_max < board_columns and piece_col_min >= 0:
    			#Check if piece is valid in location
    			transformed_coordinates = np.array([[1,board_columns]]) @ piece_coordinates 
    			grid_values = np.take(self.flat_grid,transformedCoordinates)
    			if np.sum(grid_values)==0:
    				return True
    	return False



    # Hold the currently held piece
    # Replace current piece with held piece
    def holdPiece(self):

    	if self.can_hold:
    		old_piece_id = self.current_piece
    		if self.held_piece = None
    			self.current_piece=Piece.getNextPiece()
    		else:
    			self.current_piece = Piece.generatePiece(self.held_piece)
    		self.can_hold = False
    		self.held_piece = old_piece_id

    #Hard drops piece
    #Calculates the location where to drop
    #Increments the score for dropping
    #Updates the location and updates to next piece
    def hardDrop(self):
    	new_height = self.determineDropHeight()
    	distance = new_height-self.current_piece.origin[1]
    	self.incrementScore(distance)
    	self.current_piece.origin[1] = new_height
    	#Needs some pause here
    	self.current_piece = Piece.getNextPiece()

    #Determine the drop height for the current piece by moving down
    def determineDropHeight(self):
    	test_piece = Piece.copy(self.current_piece)
        
    	maxHeight = current_piece.origin[0,1]
    	for i in range(board_rows-maxHeight):
    		success = self.collides(test_piece)
    		currentRow = i + maxHeight
    		if !success:
    			return maxHeight
    		maxHeight = i
    		Piece.move(test_piece,DIRS.DOWN)
    	return maxHeight

    #Check if line needs to be cleared based on current piece
    def clearFullRows(self):
    	piece_rows = np.unique(self.current_piece[0])
    	cleared = [checkRow(row) for row in piece_rows] 
    	rows_to_clear = piece_rows[cleared]
    	self.grid = np.delete(self.grid,np.array([rows_to_clear]),axis=0)
    	self.grid = np.vstack(np.zeros(len(rows_to_clear),board_columns),self.grid)
    	self.flat_grid = self.flattenGrid()

    #Checks for if a given row is full
    def checkRow(self, row):
    	return np.prod(self.grid[row])!= 0

    #Increments the game score
    def incrementScore(self, score_diff):
    	self.score += score_diff


	def generateJSON(self):
		# TODO

