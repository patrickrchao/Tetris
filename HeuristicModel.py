import numpy as np
from ItemQueue import Queue
import Piece
from GameState import 

lines_constant = -0.510066
aggregate_height_constant = 0.760666
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
np.array([[0,-1],[1,0]]),
"rot2":
np.array([[-1,0],[0,-1]]),
"rot3":
np.array([[0,1],[-1,0]]),
"DOWN":
np.array([[0],[1]]),
}

class HeuristicModel(Model):
    piece_queue = Queue()
    def get_move(board,piece_id,piece_origin):
        scores = np.zeros(4,2)

        left_piece_origin = np.array([[0],piece_origin[1]])
        curr_offsets = Constants.piece_offsets[piece_id]

        piece = Piece(piece_id,offsets = curr_offsets,origin=left_piece_origin)
        for rotation in range(4):
            scores_per_col = scores_per_col_given_rot(board,piece)
            column_score= np.array([np.argmax(scores_per_col),max(scores_per_col)]) #column, score
            scores[rotation] = column_score.reshape(1,2)
            Piece.rotate(piece, DIRS["rot"+str(rotation)])
        max_score = np.max(scores[:,1])
        max_score_rotate = np.argmax(scores[:,1])
        max_score_column = scores[max_score_rotate,0]


    def board_score(board,piece):
        temp_board = create_temp_board(board,piece)
        lines = lines_cleared(temp_board)
        height = aggrgate_height(temp_board)
        holes = num_holes(temp_board)
        bump = bumpiness(temp_board)
        score = height*lines_constant+lines*aggregate_height_constant+holes*num_holes_constant+bump*bumpiness_constant
        return score

    def scores_per_col_given_rot(board,curr_piece):
        piece = curr_piece.copy()
        scores = np.full((3,), -999999)
        for col in range(board.shape[1]):
            new_height = determineDropHeight(board,piece)
            piece.origin[1] = new_height
            if not collides(board,piece):
                scores[col] = board_score(board,piece.id,piece.offsets,piece.origin)
            Piece.move(piece, DIRS["RIGHT"])

    def determineDropHeight(board,piece):
        test_piece = Piece.copy(piece)
        orig_piece_height = piece.origin[1]
        for i in range(1,Constants.board_rows+2-(int)(np.floor(orig_piece_height))):
            Piece.move(test_piece,DIRS["DOWN"])
            collision = collides(board,test_piece)
            if collision:
                return i + orig_piece_height-1
        return i + origPieceHeight

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

    def create_temp_board(board,piece):
        temp_board = board.copy()
        for i in range(piece.offsets.shape[1]):
            piece_coordinates = (piece.origin + piece.offsets).astype(int)
            temp_board[piece_coordinates[1,i],piece_coordinates[0,i]] = piece.id
        return temp_board

    def aggregate_height(board):
        top_row = get_top_row(board)
        total_height = 0
        for i in range(board.shape[1]):
            total_height += top_row[i]
        return total_height

    def get_top_row(board):
        top_row = np.zeros(board.shape[1])
        for col in range(board.shape[1]):
            row_for:
            for row in range(2,board.shape[0]):
                if board[row,col] != 0:
                    top_row[col] = board.shape[0]-row
                    break row_for
        return top_row

    def num_holes(board):
        count = 0
        for col in range(board.shape[1]):
            block_above = False
            for row in range(board.shape[0]):
                if board[row,col]==1:
                    block_above = True
                elif block_above:
                    count +=1
        return count

    def clearFullRows(board):
        cleared = [np.prod(board[row])!= 0 for row in board.shape[0]] 
        num_cleared = sum(cleared)
        return num_cleared

    def bumpiness(board):
        board_row = get_top_row(board)
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