import numpy as np
from collections import deque
from Piece import Piece
import Constants
from Model import Model
import math
# From https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/

lines_constant = 0.760666
aggregate_height_constant = -0.510066
num_holes_constant = -0.35663 #4
bumpiness_constant = -0.184483 

DIRS = {
#X and Y Location
"LEFT":
np.array([[-1],[0]]),
"RIGHT":
np.array([[1],[0]]),
"rot0":
np.array([[1,0],[0,1]]),
"rot1":
np.array([[0,-1],[1,0]]), #ccw
"rot2":
np.array([[-1,0],[0,-1]]),
"rot3":
np.array([[0,1],[-1,0]]),
"DOWN":
np.array([[0],[1]]),
}

class HeuristicModel(Model):
    
    def get_move_queue(self,board,piece_id,piece_origin):
        scores = np.zeros((4,2))

        left_piece_origin = np.array([[0],piece_origin[1]])
        curr_offsets = Constants.piece_offsets[piece_id]

        piece = Piece(piece_id,offsets = curr_offsets,origin=left_piece_origin)
        for rotation in range(4):
            scores_per_col = HeuristicModel.scores_per_col_given_rot(board,piece)
            #print(scores_per_col)
            column_score= np.array([np.argmax(scores_per_col),max(scores_per_col)]) #column, score
            scores[rotation] = column_score.reshape(1,2)
            Piece.rotate(piece, DIRS["rot"+str(3)])#+str(rotation)])
        #print(scores)
        max_score = np.max(scores[:,1])
        max_score_rotate = np.argmax(scores[:,1])
        max_score_column = scores[max_score_rotate,0]
        #print(max_score,max_score_rotate,max_score_column)
        if max_score_rotate == 3:
            Model.move_queue.appendleft("ccw") #z
        else:
            for _ in range(max_score_rotate):
                Model.move_queue.appendleft("cw") #up

        for _ in range((int)(piece_origin[0]-max_score_column)):
            Model.move_queue.appendleft("left")

        for _ in range((int)(math.ceil(max_score_column-piece_origin[0]))):
            Model.move_queue.appendleft("right")
        Model.move_queue.appendleft("hard")
        #return Model.move_queue


    def board_score(board,piece_origin,piece_offsets):
        temp_board = HeuristicModel.create_temp_board(board,piece_origin,piece_offsets)
        lines = HeuristicModel.clear_full_rows(temp_board)
        height = HeuristicModel.aggregate_height(temp_board)
        holes = HeuristicModel.num_holes(temp_board)
        bump = HeuristicModel.bumpiness(temp_board)
        score = lines*lines_constant+height*aggregate_height_constant+holes*num_holes_constant+bump*bumpiness_constant
        #print(lines,height,holes,bump)
        return score

    def scores_per_col_given_rot(board,curr_piece):
        #print(board)
        #print("orig_x",curr_piece.origin)
        piece = curr_piece.copy()
        piece.origin[0] = piece.origin[0]-4

        #print("curr_x",piece.origin[0])
        scores = np.full((board.shape[1],), -999.0)
        orig_height = piece.origin.copy()[1]
        for col in range(board.shape[1]):
            new_height = HeuristicModel.determine_drop_height(board,piece)
            piece.origin[1] = new_height
            if not HeuristicModel.collides(board,piece):
                scores[col] = HeuristicModel.board_score(board,piece.origin,piece.offsets)
            piece.origin[1] = orig_height
            Piece.move(piece, DIRS["RIGHT"])
            #print(piece.origin)
        return scores

    def determine_drop_height(board,piece):

        test_piece = Piece.copy(piece)
        orig_piece_height = piece.origin[1]
        for i in range(1,Constants.board_rows+2-(int)(np.floor(orig_piece_height))):
            Piece.move(test_piece,DIRS["DOWN"])
            collision = HeuristicModel.collides(board,test_piece)
            if collision:
                return test_piece.origin[1] - 1
        return test_piece.origin[1] 

    #Check if a piece collides or is out of bounds
    #Returns true if they collide false otherwise
    def collides(board,piece):    
        piece_coordinates = (piece.origin + piece.offsets).astype(int)
        #Check if out of board range
        #Change to better max and min over rows and columns
        piece_row_max = np.amax(piece_coordinates[1])
        piece_row_min = np.amin(piece_coordinates[1])
        piece_col_max = np.amax(piece_coordinates[0])
        piece_col_min = np.amin(piece_coordinates[0])

        if piece_row_max < Constants.board_rows+2 and piece_row_min >= 0:
            if piece_col_max < Constants.board_columns and piece_col_min >= 0:
                #Check if piece is valid in location
                transformed_coordinates = (np.array([[1,Constants.board_columns]]) @ piece_coordinates).squeeze()
                #Flatten board
                flat_board = board.flatten()
                board_values = np.take(flat_board,transformed_coordinates)
                if np.sum(board_values)==0:
                    return False
        return True

    def create_temp_board(board,piece_origin,piece_offsets):
        temp_board = board.copy()
        for i in range(piece_offsets.shape[1]):
            piece_coordinates = (piece_origin + piece_offsets).astype(int)
            temp_board[piece_coordinates[1,i],piece_coordinates[0,i]] = 1
        return temp_board

    def aggregate_height(board):
        top_row = HeuristicModel.get_top_row(board)
        total_height = 0
        for i in range(board.shape[1]):
            total_height += top_row[i]
        return total_height

    def get_top_row(board):
        top_row = np.zeros(board.shape[1])
        for col in range(board.shape[1]):
            #row_for:
            for row in range(2,board.shape[0]):
                if board[row,col] != 0:
                    top_row[col] = board.shape[0]-row
                    break #row_for
        return top_row

    def num_holes(board):
        count = 0
        for col in range(board.shape[1]):
            block_above = False
            for row in range(board.shape[0]):
                if board[row,col]!=0:
                    block_above = True
                elif block_above:
                    count +=1
        return count

    #Checks for if a given row is full
    def checkRow(self, row):
        return np.prod(self.board[row])!= 0

    def clear_full_rows(board):
        cleared = [np.prod(board[row])!= 0 for row in range(board.shape[0])] 
        num_cleared = sum(cleared)
        return num_cleared

    def bumpiness(board):
        board_row = HeuristicModel.get_top_row(board)
        total_sum=0
        for i in range(board.shape[1]-1):
            total_sum += abs(board_row[i]-board_row[i+1])
        return total_sum

    def generateMoveQueue(bestCol,maxRot,pieceLeftCol):
        if maxRot==3:
            moveQueue.enqueue(4) #z
        else:
            for _ in range(maxRot):
                moveQueue.enqueue(2) #up

        for _ in range(pieceLeftCol-bestCol):
            moveQueue.enqueue(0)

        for _ in range(bestCol-pieceLeftCol):
            moveQueue.enqueue(1)
        moveQueue.enqueue(3)
        return moveQueue