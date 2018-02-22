# Patrick Chao and Dillon Yao
# 2/21/18
# TETRIS
# MACHINEEEEEEE LEARNINGGG
# Piece.py

#Contains the Piece game logic

import numpy as np

class Piece:

	def __init__(self,current_piece_id, offsets = None, origin = None):
		self.id = current_piece_id

		#Offsets is a 2x4 numpy matrix
		self.offsets = offsets
		if offsets == None:
			self.offsets = #get from constants

		#Origin is a 2x1 numpy matrix
		self.origin = origin
		if origin == None:
			self.origin = #get from constnats


	def move(direction):
		self.origin -= direction

	def rotate(direction):
		multiplier = 1
		if direction == "clockwise":
			multiplier = -1
		rotationMatrix = np.array([[0,-multiplier],[multiplier,0]])
		self.offsets = rotationMatrix@ self.offsets

	def copy(piece):
		return Piece(piece.id, piece.offsets, piece.origin)

