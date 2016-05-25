def binarySearch(L, v):
	'''docstring for binarySearch:
	binarySearch: List, Number -> Boolean, Number
	This function takes a sorted list L and a number v
	and return a tuple (found,itera) where found is a Boolean corresponding to
	whether v is in L, and itera is the number of iterations it takes
	'''
	if not L:
		return (False, 0)
	right = len(L) - 1
	left = 0
	mid = (left + right) // 2
	found = False
	itera = 0
	while v != L[mid] and right != left:
		itera += 1
		if v > L[mid]:
			left = mid + 1
			mid = (left + right) // 2
		else:
			right = mid - 1
			mid = (left + right) // 2
	if v == L[mid]:
		found = True
	return (found, itera)

def mean(L):
	'''docstring for mean:
	return the mean value of list L
	'''
	sum = 0.0
	for x in L:
		sum += x
	return sum / len(L)

def median(L):
	'''docstring for median:
	return the median value of list L
	'''
	if not L:
		return False
	S = sorted(L)
	if len(L) % 2:
		return L[len(L) / 2]
	else:
		return (L[len(L) / 2] + L[len(L) / 2 - 1]) / 2.0

def bfs(tree, elem):
	'''docstring for bfs:
	breadth first search using queue
	'''
	q = [tree]
	return bfsHelper(q, elem)
def bfsHelper(q, elem):
	if not q:
		return False
	q.reverse()
	check = q.pop()
	print check[0]
	if check[0] == elem:
		return True
	q.reverse()
	for x in check[1:]:
		q.append(x)
	return bfsHelper(q, elem)

	

def dfs(tree, elem):
	'''docstring for dfs:
	depth first search using recursion
	'''
	if not tree:
		return False
	print tree[0]
	if tree[0] == elem:
		return True
	for x in tree[1:]:
		if dfs(x, elem):
			return True
	return False

class TTTBoard(object):
	"""docstring for TTTBoard:
	makeMove: It takes a player and a position and return a new board with 
	new chess putted on. A player is 'X' or 'O'; a position is a integer in
	[0, 8] where the upleft is 0, the right position is 1, and the bottom 
	right is 8.	
	hasWon: It takes a player and returns if the player has won.
	gameOver: It takes nothing and return if game is over, in other word, 
	it returns if the board is full, of one of the player has won.
	clear: It clears the board.
	"""
	def __init__(self):
		self.board = [['*', '*', '*'], ['*', '*', '*'], ['*', '*', '*']]
	def __str__(self):
		ans = ''
		for x in self.board:
			for y in x:
				ans += y
				ans += ' '
			ans += '\n'
		return ans
	def makeMove(self, player, pos):
		self.board[pos / 3][pos % 3] = player
	def hasWon(self, player):
		b = self.board
		return (
			(b[0][0] == player and b[0][1] == player and b[0][2] == player) or 
			#first horizonal line
			(b[1][0] == player and b[1][1] == player and b[1][2] == player) or 
			#second horizonal line
			(b[2][0] == player and b[2][1] == player and b[2][2] == player) or 
			#third horizonal line
			(b[0][0] == player and b[1][0] == player and b[2][0] == player) or 
			#first vertical line
			(b[0][1] == player and b[1][1] == player and b[2][1] == player) or 
			#second vertical line
			(b[0][2] == player and b[1][2] == player and b[2][2] == player) or 
			#third vertical line
			(b[0][0] == player and b[1][1] == player and b[2][2] == player) or 
			#diag
			(b[2][0] == player and b[1][1] == player and b[0][2] == player)    
			#diag
			)


	def gameOver(self):
		full = True
		for x in self.board:
			for y in x:
				full = full and (not ('*' == y))
		return hasWon('X') or hasWon('O') or full


	def clear(self):
		self.board = [['*', '*', '*'], ['*', '*', '*'], ['*', '*', '*']]























