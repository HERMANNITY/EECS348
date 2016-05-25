#!/usr/bin/env python
# Team members:
# Sixuan Yu (syj099)
# Guixing Lin (glv321)
# Junhan Liu (jlt587)
# All group members are present and contributing during all work on this project.

import struct, string, math
from copy import deepcopy

class SudokuBoard:
	"""This will be the sudoku board game object your player will manipulate."""
  
	def __init__(self, size, board):
	  """the constructor for the SudokuBoard"""
	  self.BoardSize = size #the size of the board
	  self.CurrentGameBoard= board #the current state of the game board

	def set_value(self, row, col, value):
		"""This function will create a new sudoku board object with the input
		value placed on the GameBoard row and col are both zero-indexed"""

		#add the value to the appropriate position on the board
		self.CurrentGameBoard[row][col]=value
		#return a new board of the same size with the value added
		return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
																  
	def print_board(self):
		"""Prints the current game board. Leaves unassigned spots blank."""
		div = int(math.sqrt(self.BoardSize))
		dash = ""
		space = ""
		line = "+"
		sep = "|"
		for i in range(div):
			dash += "----"
			space += "    "
		for i in range(div):
			line += dash + "+"
			sep += space + "|"
		for i in range(-1, self.BoardSize):
			if i != -1:
				print "|",
				for j in range(self.BoardSize):
					if self.CurrentGameBoard[i][j] > 9:
						print self.CurrentGameBoard[i][j],
					elif self.CurrentGameBoard[i][j] > 0:
						print "", self.CurrentGameBoard[i][j],
					else:
						print "  ",
					if (j+1 != self.BoardSize):
						if ((j+1)//div != j/div):
							print "|",
						else:
							print "",
					else:
						print "|"
			if ((i+1)//div != i/div):
				print line
			else:
				print sep

def parse_file(filename):
	"""Parses a sudoku text file into a BoardSize, and a 2d array which holds
	the value of each cell. Array elements holding a 0 are considered to be
	empty."""

	f = open(filename, 'r')
	BoardSize = int( f.readline())
	NumVals = int(f.readline())

	#initialize a blank board
	board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

	#populate the board with initial values
	for i in range(NumVals):
		line = f.readline()
		chars = line.split()
		row = int(chars[0])
		col = int(chars[1])
		val = int(chars[2])
		board[row-1][col-1]=val
	
	return board
	
def is_complete(sudoku_board):
	"""Takes in a sudoku board and tests to see if it has been filled in
	correctly."""
	BoardArray = sudoku_board.CurrentGameBoard
	size = len(BoardArray)
	subsquare = int(math.sqrt(size))

	#check each cell on the board for a 0, or if the value of the cell
	#is present elsewhere within the same row, column, or square
	for row in range(size):
		for col in range(size):
			if BoardArray[row][col]==0:
				return False
			for i in range(size):
				if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
					return False
				if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
					return False
			#determine which square the cell is in
			SquareRow = row // subsquare
			SquareCol = col // subsquare
			for i in range(subsquare):
				for j in range(subsquare):
					if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
							== BoardArray[row][col])
						and (SquareRow*subsquare + i != row)
						and (SquareCol*subsquare + j != col)):
							return False
	return True

def init_board(file_name):
	"""Creates a SudokuBoard object initialized with values from a text file"""
	board = parse_file(file_name)
	return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
	LCV = False):
	"""Takes an initial SudokuBoard and solves it using back tracking, and zero
	or more of the heuristics and constraint propagation methods (determined by
	arguments). Returns the resulting board solution. """
	size = len(initial_board.CurrentGameBoard)
	# Create a 3D-array to store possible moves for each positions
	moves = [[[x for x in xrange(1,size+1)] for y in xrange(size)] for z in xrange(size)]
	for r in xrange(size):
		for c in xrange(size):
			if initial_board.CurrentGameBoard[r][c]:
				forwardCheck(moves, r, c, initial_board.CurrentGameBoard[r][c])			
	board = backtrack(initial_board, moves, forward_checking, MRV, Degree, LCV)	# Solve
	return board

def backtrack(board, moves, FC, MRV, Degree, LCV, count=0):
	"""Use backtracking to solve the Sudoku puzzle"""
	if MRV:				# Use MRV heuristic
		pos = choosePos_MRV(board.CurrentGameBoard, moves)
	elif Degree:		# Use degree heuristic
		pos = choosePos_Degree(board.CurrentGameBoard)
	else:				# No heuristic used
		pos = choosePos_First(board.CurrentGameBoard)
	r = pos[0]
	c = pos[1]
	if r == -1:			# If the board has been filled
		return board
	values = moves[r][c][:]		# Retrieve possible values of the position from moves
	movesCopy = deepcopy(moves)	# Create a copy of moves
	while values:				# If values is not empty
		if LCV:					# Use LCV heuristic to choose a value
			value = chooseVal_LCV(moves, r, c, values)
		else:					# Trivial heuristic, pop the first value
			value = chooseVal_First(values)
		count += 1
		if validate(board.CurrentGameBoard, pos, value):	# Validate value
			(board.CurrentGameBoard)[r][c] = value			# Assign value to pos
			if FC:											# If forward checking is enabled
				forwardCheck(movesCopy, r, c, value)		# Perfome Forward Checking
			backtrack(board, movesCopy, FC, MRV, Degree, LCV, count)	# Recur
			if is_complete(board):
				return board
			(board.CurrentGameBoard)[r][c] = 0				# Reverse the last assignment
			movesCopy = deepcopy(moves)						# Reset the domain
	return board

def forwardCheck(moves, row, col, value):
	"""Perform Forward Checking to reduce size of domain"""
	boardLength = len(moves)					# Length of board
	blockLength = int(math.sqrt(boardLength))	# Length of a block of the board
	blockRow = row/blockLength					# Row index of the block
	blockCol = col/blockLength					# Col index of the block
	for c in xrange(boardLength):				# Forward check the whole row
		if value in moves[row][c]:
			(moves[row][c]).remove(value)
	for r in xrange(boardLength):				# Forward check the whole column
		if value in moves[r][col]:
			(moves[r][col]).remove(value)
	for r in xrange(blockRow*blockLength, (blockRow+1)*blockLength):	# FC the block
		for c in xrange(blockCol*blockLength, (blockCol+1)*blockLength):
			if value in moves[r][c]:
				(moves[r][c]).remove(value)

def validate(board, pos, value):
	"""Return True if placing value on pos is a valid move, False otherwise"""
	row = pos[0]
	col = pos[1]
	boardLength = len(board)					# Length of board
	blockLength = int(math.sqrt(boardLength))	# Length of a block of the board
	blockRow = row/blockLength					# Row index of the block
	blockCol = col/blockLength					# Col index of the block
	for c in xrange(boardLength):				# Validate row
		if board[row][c] == value:
			return False
	for r in xrange(boardLength): 				# Validate column
		if board[r][col] == value:
			return False
	for r in xrange(blockRow*blockLength, (blockRow+1)*blockLength):	# Validate block
		for c in xrange(blockCol*blockLength, (blockCol+1)*blockLength):
			if board[r][c] == value:
				return False
	return True

def choosePos_First(board):
	"""Return the first empty position (row-major order) of the board,
	return (-1,-1) if the board is full"""
	for r in xrange(len(board)):
		for c in xrange(len(board)):
			if board[r][c] == 0:
				return (r, c)
	return (-1, -1)	# Return (-1, -1) if the board is full

def choosePos_MRV(board, moves):
	"""Return the position with fewest values left, 
	return (-1,-1) if the board is full"""
	pos = (-1, -1)	# Return (-1, -1) if the board is full
	minVal = float("inf")
	for r in xrange(len(board)):
		for c in xrange(len(board)):
			if board[r][c] == 0 and len(moves[r][c]) < minVal:
				minVal = len(moves[r][c])
				pos = (r, c)
	return pos

def choosePos_Degree(board):
	"""Return the position involved in the largest number of constraints 
	on unassigned variables"""
	pos = (-1, -1)	# Return (-1, -1) if the board is full
	maxDegree = -1
	for r in xrange(len(board)):
		for c in xrange(len(board)):
			if board[r][c] == 0:
				degree = choosePos_Degree_helper(board, r, c)
				if degree > maxDegree:
					maxDegree = degree
					pos = (r, c)
	return pos
				
def choosePos_Degree_helper(board, row, col):
	"""Return number of constraints involved of position [row][col]"""
	boardLength = len(board)					# Length of board
	blockLength = int(math.sqrt(boardLength))	# Length of a block of the board
	blockRow = row/blockLength					# Row index of the block
	blockCol = col/blockLength					# Col index of the block
	degree = 0
	for c in xrange(boardLength):				# Count row
		if board[row][c] == 0:
			degree += 1
	for r in xrange(boardLength):				# Count column
		if r != row and board[r][col] == 0:
			degree += 1
	for r in xrange(blockRow*blockLength, (blockRow+1)*blockLength):	# Count block
		for c in xrange(blockCol*blockLength, (blockCol+1)*blockLength):
			if r != row and c != col and board[r][c] == 0:
				degree += 1
	return degree

def chooseVal_First(values):
	"""Return the first value in the domain"""
	return values.pop(0)	

def chooseVal_LCV(moves, row, col, values):
	"""Return the value that rules out the fewest choices for other unassigned variable"""
	boardLength = len(moves)					# Length of board
	blockLength = int(math.sqrt(boardLength))	# Length of a block of the board
	blockRow = row/blockLength					# Row index of the block
	blockCol = col/blockLength					# Col index of the block
	value = -1
	opt = float("inf")
	for val in values:
		count = 0									# Number of choices ruled out
		for c in xrange(boardLength):				# Count row
			if val in moves[row][c]:
				count += 1
		for r in xrange(boardLength):				# Count column
			if r != row and val in moves[r][col]:
				count += 1
		for r in xrange(blockRow*blockLength, (blockRow+1)*blockLength):	# Count block
			for c in xrange(blockCol*blockLength, (blockCol+1)*blockLength):
				if r != row and c != col and val in moves[r][c]:
					count += 1
		if count < opt:
			value = val
			opt = count
	values.remove(value)
	return value



if __name__== "__main__":
	n = 7
	FC = 1
	MRV = 1
	Degree = 0
	LCV = 1
	while n <= 7:
		# s = "input_puzzles/more/16x16/16x16." + str(n) + ".sudoku"
		s = "input_puzzles/easy/25_25.sudoku"
		sb2 = init_board(s)
		n += 1
		print "\nInitial board:"
		sb2.print_board()
		print ""
		solved = solve(sb2, FC, MRV, Degree, LCV)
		print "Solved board:"
		solved.print_board()

