# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# GameState.py

#Contains the game state variables
#Tetris Game Logic

import numpy as np

from Piece import Piece
import Constants

class GameState:
    def __init__(self):
        self.grid = np.zeros((Constants.board_rows+2,Constants.board_columns))
        self.grid[-1,:]=np.array([1,1,1,1,0,0,1,1,1,1])
        Piece.fillBag()
        self.current_piece = Piece.getNextPiece()
        self.held_piece = 0
        self.score = 0
        self.down_state = False
        self.can_hold = True
        self.time_since_drop = 0
        self.time_per_drop = Constants.max_time_per_drop
        self.down_state_held_time = 0

    #Still temporary
    #Given an action, attempts to perform the action
    def keyAction(self, key,dt): 
        if key == 'ArrowLeft':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS["LEFT"]) )
        elif key == 'ArrowRight':
            self.attemptAction(lambda piece: Piece.move(piece, DIRS["RIGHT"]))
        elif key == 'ArrowUp' or key == "C":
            self.attemptAction(lambda piece: Piece.rotate(piece, DIRS["CLOCKWISE"]))
        elif key == 'Z':
            self.attemptAction(lambda piece: Piece.rotate(piece, DIRS["COUNTERCLOCKWISE"]))
        elif key == 'ArrowDownReleased':
            self.down_state_held_time = 0
            self.time_per_drop = Constants.max_time_per_drop
        elif key == 'ArrowDown':
            self.down_state_held_time += dt
            self.time_per_drop = Constants.max_time_per_drop/(Constants.drop_inertia*self.down_state_held_time + 1)
        elif key == 'Shift':
            self.holdPiece()
        elif key == 'Space':
            self.hardDrop()
        else:
            return

    def attemptAction(self, action):
        test_piece = Piece.copy(self.current_piece)
        action(test_piece)
        success = not self.collides(test_piece)
        if success:
            action(self.current_piece)
        return success

    #Check if a piece collides or is out of bounds
    #Returns true if they collide false otherwise
    def collides(self, piece):    
        piece_coordinates = (piece.origin + piece.offsets).astype(int)
        #Check if out of board range
        piece_row_max = np.amax(piece_coordinates[1])
        piece_row_min = np.amin(piece_coordinates[1])
        piece_col_max = np.amax(piece_coordinates[0])
        piece_col_min = np.amin(piece_coordinates[0])

        if piece_row_max < Constants.board_rows+2 and piece_row_min >= 0:
            if piece_col_max < Constants.board_columns and piece_col_min >= 0:
                #Check if piece is valid in location
                transformed_coordinates = (np.array([[1,Constants.board_columns]]) @ piece_coordinates).squeeze()
                #print(transformed_coordinates)
                #Flatten Grid

                flat_grid = self.grid.flatten()
                grid_values = np.take(flat_grid,transformed_coordinates)
                #print(grid_values)
                if np.sum(grid_values)==0:
                    return False
        return True


    # Hold the currently held piece
    # Replace current piece with held piece
    def holdPiece(self):
        if self.can_hold:
            old_piece_id = self.current_piece
            if self.held_piece == None:
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
        
        self.updateBoardWithPiece()
        self.clearFullRows()
        self.current_piece = Piece.getNextPiece()

    #Determine the drop height for the current piece by moving down
    def determineDropHeight(self):
        #print(self.current_piece.origin)
        test_piece = Piece.copy(self.current_piece)
        maxHeight = self.current_piece.origin[1,0]
        for i in range(1,Constants.board_rows+2-(int)(np.ceil(maxHeight))):
            success = self.collides(test_piece)
            currentRow = i + maxHeight
            if not success:
                return currentRow-1
            Piece.move(test_piece,DIRS["DOWN"])
        return maxHeight

    #Check if line needs to be cleared based on current piece
    def clearFullRows(self):
        piece_coordinates = (self.current_piece.origin + self.current_piece.offsets).astype(int)
        piece_rows = np.unique(piece_coordinates[1,:])

        cleared = [self.checkRow(row) for row in piece_rows] 
        rows_to_clear = piece_rows[cleared]
        self.grid = np.delete(self.grid,np.array([rows_to_clear]),axis=0)
        self.grid = np.vstack((np.zeros((len(rows_to_clear),Constants.board_columns)),self.grid))

    #Checks for if a given row is full
    def checkRow(self, row):
        return np.prod(self.grid[row])!= 0

    #Increments the game score
    def incrementScore(self, score_diff):
        self.score += score_diff

    def updateBoardWithPiece(self):
        self.down_state_held_time = 0
        for i in range(self.current_piece.offsets.shape[1]):
            piece_coordinates = (self.current_piece.origin + self.current_piece.offsets).astype(int)
            self.grid[piece_coordinates[1,i],piece_coordinates[0,i]] = self.current_piece.id

    def update(self,dt):
        self.time_since_drop += dt
        if self.time_since_drop >= self.time_per_drop:
            self.printBoard()
            self.time_since_drop = 0
            success = self.attemptAction(lambda piece: Piece.move(piece, DIRS["DOWN"]))
            if not success:
                self.updateBoardWithPiece()
                self.clearFullRows()
                self.current_piece = Piece.getNextPiece()



    def generateJSON(self):
        # TODO
        return 

    def printBoard(self):
        temp_grid = self.grid.copy()
        piece_coordinates = (self.current_piece.origin + self.current_piece.offsets).astype(int)
        for i in range(self.current_piece.offsets.shape[1]):
            temp_grid[piece_coordinates[1,i],piece_coordinates[0,i]] = self.current_piece.id+0.5
        print(temp_grid)


DIRS = {
#X and Y Location
"LEFT":
np.array([[-1],[0]]),
"RIGHT":
np.array([[1],[0]]),
"COUNTERCLOCKWISE":
np.array([[0,-1],[1,0]]),
"CLOCKWISE":
np.array([[0,1],[-1,0]]),
"DOWN":
np.array([[0],[1]]),



}