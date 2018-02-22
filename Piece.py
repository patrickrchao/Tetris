# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# MACHINEEEEEEE LEARNINGGG
# Piece.py

#Contains the Piece game logic

import numpy as np

class Piece:

	bag = deque()
	bag = fillBag()

	def __init__(self, current_piece_id, offsets = None, origin = None):
		self.id = current_piece_id

		#Offsets is a 2x4 numpy matrix
		self.offsets = offsets
		if offsets == None:
			self.offsets = #get from constants

		#Origin is a 2x1 numpy matrix
		self.origin = origin
		if origin == None:
			self.origin = #get from constants

	def move(self, direction):
		self.origin -= direction

	def rotate(self, direction):
		multiplier = 1
		if direction == "clockwise":
			multiplier = -1
		rotationMatrix = np.array([[0,-multiplier],[multiplier,0]])
		self.offsets = rotationMatrix@ self.offsets

	def copy(self, piece):
		return Piece(piece.id, piece.offsets, piece.origin)

	# Using the bag of pieces, returns an instance of the next piece
	# Adds another piece to the bag
	def getNextPiece():
		piece_id = bag.popleft()
		#if bag is getting almost empty, refill bag
		if len(bag)<5:
			fillBag(7)
		return Piece(piece_id)

	 #Initializes the bag of pieces given a bag size
	def fillBag(bag_size = 10):
		nextPieces = np.random.randint(1,8,bag_size).tolist()
		bag.extend(nextPieces)