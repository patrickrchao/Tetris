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
    def __init__(self,services):
        self.board = np.zeros((Constants.board_rows+2,Constants.board_columns))
        #self.board[-1,:]=np.array([1,1,1,1,0,0,1,1,1,1])
        Piece.fillBag()
        self.current_piece = Piece.getNextPiece()
        self.held_piece = None
        self.score = 0
        self.down_state = False
        self.can_hold = True
        self.time_since_drop = 0
        self.time_per_drop = Constants.max_time_per_drop
        self.down_state_held_time = 0
        self.services = services

        self.services.input.subscribe('action', self.handle_action)
        self.services.input.subscribe('end_action', self.handle_end_action)
        self.counter={'left' :0 ,'right':0,'cw':0,'ccw':0,'soft':0}

    def handle_input(self):
        input = self.services.input
        if Constants.use_model:
            self.handle_action(input.get_next_input(self.board,self.current_piece.id,self.current_piece.origin))
        else:
        #if not Constants.use_model:
            if input.poll('left'):
                if self.counter['left'] % Constants.hold_rate == 0:
                    self.attemptAction(lambda piece: Piece.move(piece, DIRS["LEFT"]))
                self.counter['left'] +=1 
            if input.poll('right'):
                if self.counter['right'] % Constants.hold_rate == 0:
                    self.attemptAction(lambda piece: Piece.move(piece, DIRS["RIGHT"])) 
                self.counter['right'] +=1   
            if input.poll('soft'):
                #if self.counter['soft'] % Constants.hold_rate == 0:
                self.down_state_held_time += Constants.timestep
                self.speedUpDropRate(self.down_state_held_time)
            #self.counter['soft'] +=1    

    #Still temporary
    #Given an action, attempts to perform the action
    def handle_action(self, key):
        print(key)
        action = key['action']             
        if action == 'hold':
            self.holdPiece()
        elif action == 'hard':
            self.hardDrop()
        elif action == 'cw':
            self.attemptAction(lambda piece: Piece.rotate(piece, DIRS["CLOCKWISE"]))
        elif action == 'ccw':
            self.attemptAction(lambda piece: Piece.rotate(piece, DIRS["COUNTERCLOCKWISE"]))
        if Constants.use_model:
            if action == 'left':
                self.attemptAction(lambda piece: Piece.move(piece, DIRS["LEFT"]))
            elif action == 'right':
                self.attemptAction(lambda piece: Piece.move(piece, DIRS["RIGHT"]))
            elif action == 'soft':
                self.down_state_held_time += Constants.timestep
                self.speedUpDropRate(self.down_state_held_time)

    def handle_end_action(self, key):
        action = key['action']
        if action == 'left': 
            self.counter['left'] = 0
        elif action == 'right': 
            self.counter['right'] = 0  
        elif action == 'soft':
            self.resetDropRate()

    def speedUpDropRate(self,dropMetric):
        self.time_per_drop = Constants.max_time_per_drop/(Constants.drop_inertia*dropMetric + 1)

    def resetDropRate(self):
        #print("RESETING")
        self.down_state_held_time = 0
        self.time_per_drop = Constants.max_time_per_drop

    def attemptAction(self, action):
        test_piece = Piece.copy(self.current_piece)
        action(test_piece)
        #print("attempting",action)
        success = not self.collides(test_piece)
        #print(success,(self.current_piece.origin + self.current_piece.offsets).astype(int))
        if success:
            action(self.current_piece)
        return success

    #Check if a piece collides or is out of bounds
    #Returns true if they collide false otherwise
    def collides(self, piece):    
        piece_coordinates = (piece.origin + piece.offsets).astype(int)
        #Check if out of board range

        #Change to better max and min over rows and columns
        piece_row_max = np.amax(piece_coordinates[1])
        piece_row_min = np.amin(piece_coordinates[1])
        piece_col_max = np.amax(piece_coordinates[0])
        piece_col_min = np.amin(piece_coordinates[0])

        #print("in checking collision",piece_coordinates)
        if piece_row_max < Constants.board_rows+2 and piece_row_min >= 0:
            if piece_col_max < Constants.board_columns and piece_col_min >= 0:
                #Check if piece is valid in location
                transformed_coordinates = (np.array([[1,Constants.board_columns]]) @ piece_coordinates).squeeze()
                #print(transformed_coordinates)
                #Flatten board
                flat_board = self.board.flatten()
                board_values = np.take(flat_board,transformed_coordinates)
                #print(board_values)
                if np.sum(board_values)==0:
                    return False
        return True


    # Hold the currently held pieces
    # Replace current piece with held piece
    def holdPiece(self):
        if self.can_hold:
            old_piece_id = self.current_piece.id
            if self.held_piece == None:
                self.current_piece=Piece.getNextPiece()
            else:
                self.current_piece = Piece(self.held_piece)
            self.can_hold = False
            self.held_piece = old_piece_id

    #Hard drops piece
    #Calculates the location where to drop
    #Increments the score for dropping
    #Updates the location and updates to next piece
    def hardDrop(self):
        new_height = self.determineDropHeight()
        #print(new_height)
        distance = new_height-self.current_piece.origin[1]
        self.incrementScore(distance)
        self.current_piece.origin[1] = new_height
        #print("drop",(self.current_piece.origin + self.current_piece.offsets).astype(int))
        self.updateBoardWithPiece(new_height)
        self.clearFullRows()

        self.current_piece = Piece.getNextPiece()

    #Determine the drop height for the current piece by moving down
    def determineDropHeight(self):
        test_piece = Piece.copy(self.current_piece)
        origPieceHeight = self.current_piece.origin[1]
        for i in range(1,Constants.board_rows+3-(int)(np.floor(origPieceHeight))):
            Piece.move(test_piece,DIRS["DOWN"])
            collision = self.collides(test_piece)
            if collision:
                #print("collided",(test_piece.origin + test_piece.offsets).astype(int))
                return test_piece.origin[1] - 1
        return test_piece.origin[1]

    #Check if line needs to be cleared based on current piece
    def clearFullRows(self):
        piece_coordinates = (self.current_piece.origin + self.current_piece.offsets).astype(int)
        piece_rows = np.unique(piece_coordinates[1,:])

        cleared = [self.checkRow(row) for row in piece_rows] 
        rows_to_clear = piece_rows[cleared]
        self.board = np.delete(self.board,np.array([rows_to_clear]),axis=0)
        self.board = np.vstack((np.zeros((len(rows_to_clear),Constants.board_columns)),self.board))

    #Checks for if a given row is full
    def checkRow(self, row):
        return np.prod(self.board[row])!= 0

    #Increments the game score
    def incrementScore(self, score_diff):
        self.score += (int)(np.floor(score_diff))

    def updateBoardWithPiece(self,piece_height=None):
        if piece_height == None:
            piece_height = self.current_piece.origin[1]
        self.resetDropRate()
        self.can_hold = True
        self.down_state_held_time = 0
        current_piece_origin = self.current_piece.origin.copy()
        current_piece_origin[1] = piece_height
        piece_coordinates = (current_piece_origin + self.current_piece.offsets).astype(int)
        for i in range(self.current_piece.offsets.shape[1]):
            self.board[piece_coordinates[1,i],piece_coordinates[0,i]] = self.current_piece.id

    def update(self,dt):
        self.time_since_drop += dt
        if self.time_since_drop >= self.time_per_drop:
            #print(self.time_per_drop)
            self.time_since_drop = 0
            #print("telem",(self.current_piece.origin + self.current_piece.offsets).astype(int))
            self.sendTelemetry()
            success = self.attemptAction(lambda piece: Piece.move(piece, DIRS["DOWN"]))
            if not success:
                self.updateBoardWithPiece()
                self.clearFullRows()
                self.current_piece = Piece.getNextPiece()

    def sendTelemetry(self):
        temp_board = self.board.copy()
        piece_coordinates = (self.current_piece.origin + self.current_piece.offsets).astype(int)
        for i in range(self.current_piece.offsets.shape[1]):
            temp_board[piece_coordinates[1,i],piece_coordinates[0,i]] = self.current_piece.id
        json = temp_board.tolist()
        self.services.telemetry.emit('gameframe', {'data': json})


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