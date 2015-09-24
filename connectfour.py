
numNodesExpanded = 0
directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

class InvalidMoveException(Exception):
	"""Exception raised if someone tries to make an invalid move."""

	def __init__(self, column, board):
		"""
		board: the board on which the movement took place
		column: the column to which an addition was attempted
		"""
		self._column = column
		self._board = board

	def __str__(self):
		return "InvalidMoveException: Can't add to column %s on board:\n%s" % (str(self._column), str(self._board))

	def __repr__(self):
		return str(self)


class ConnectFourBoard(object):
	"""
	Store a Connect Four board.

	A Connect Four board is an immutable matrix, laid out as follows:

		0 . . . . . . .
		1 . . . . . . .
		2 . . . . . . .
		3 . . . . . . .
		4 . . . . . . .
		5 . . . . . . .
		  0 1 2 3 4 5 6

	Board columns fill from the bottom (ie., row 6).
	"""

	# The horizontal width of every board
	board_width = 7
	# The vertical height of every board
	board_height = 6

	# Map of board ID numbers to display characters used to print the board
	board_symbols = ['.', 'X', 'O']

	def __init__(self, board_array=None, current_player=1,
		chain_length_goal=4, longest_streak_to_win=False):
		"""
		Create a new ConnectFourBoard.

		If board_array is specified, it should be an MxN matrix of iterables
		(ideally tuples or lists) that will be used to describe the initial
		board state.  Each cell should be either 0, meaning unoccupied, or
		N for some integer N corresponding to a player number.

		Valid player numbers are 1 and 2.
		"""
		if not board_array:
			self._board_array = ((0,) * self.board_width,) * self.board_height
		else:
			# Make sure we're storing tuples, so that they're immutable
			self._board_array = tuple(map(tuple, board_array))
		self._current_player = current_player
		self._chain_length_goal = chain_length_goal
		self._longest_streak_to_win = longest_streak_to_win

	def __str__(self):
		"""Return a string representation of this board."""
		retVal = [str(i) + ' ' + ' '.join([self.board_symbols[x] for x in row])
			for i, row in enumerate(self._board_array)]
		retVal += ['  ' + ' '.join(str(x) for x in range(self.board_width))]
		return '\n' + '\n'.join(retVal) + '\n'

	def __repr__(self):
		""" Return the string representation of a board in the Python shell."""
		return str(self)

	def __hash__(self):
		"""Determine the hash key of a board.  The hash key must be the same on any two identical boards."""
		return hash(self._board_array)

	def __eq__(self, other):
		""" Determine whether two boards are equal. """
		return self._board_array == other._board_array

	def get_current_player_id(self):
		"""Return the ID of the player who should be moving now."""
		return self._current_player

	def get_opposite_player_id(self):
		"""Return the ID of the opponent of the player who should be moving now."""
		return 2 if self._current_player == 1 else 1

	def num_tokens_on_board(self):
		"""
		Returns the total number of tokens (for either player)
		currently on the board.
		"""
		tokens = 0
		for row in self._board_array:
			for col in row:
				if col:
					tokens += 1
		return tokens

	def get_top_elt_in_column(self, column):
		"""
		Return the ID of the player who put the topmost token in
		the specified column.
		Return 0 if the column is empty.
		"""
		for row in self._board_array:
			if row[column]:
				return row[column]
		return 0

	def get_top_of_column(self, column):
		"""
		Return the index of the lowest empty cell in the specified column.
		Return -1 if the column is full.
		"""
		for i in xrange(self.board_height):
			if self._board_array[i][column]:
				return i - 1
		return self.board_height - 1

	def get_cell(self, row, col):
		"""
		Return the ID of the player owning the token in the specified cell.
		Return 0 if it is unclaimed.
		"""
		assert(row < len(self._board_array) and col < len(self._board_array[0]))
		return self._board_array[row][col]

	def do_move(self, column):
		"""
		Execute the specified move as the specified player.
		Return a new board with the result.
		Raise InvalidMoveException if the specified move is invalid.
		"""
		global numNodesExpanded
		numNodesExpanded += 1
		row = self.get_top_of_column(column)
		if row < 0:
			raise InvalidMoveException(column, self)
		new_board = self._board_array
		new_row = (new_board[row][:column] + (self._current_player,) + new_board[row][column+1:],)
		new_board = new_board[:row] + new_row + new_board[row+1:]
		return ConnectFourBoard(new_board, self.get_opposite_player_id(),
			self._chain_length_goal, self._longest_streak_to_win)

	def clone(self):
		"""Return a copy of the game board."""
		return ConnectFourBoard(self._board_array, self._current_player,
			self._chain_length_goal, self._longest_streak_to_win)

	def is_game_over(self):
		""" Return True if the game has been won, False otherwise """
		return self.is_win() or self.is_tie()

	def is_win(self):
		"""
		Return the ID of the player who has won this game.
		Return 0 if it has not yet been won.
		"""
		if self._longest_streak_to_win:
			if self.num_tokens_on_board() < 20:
				return False
			current_streak = self.longest_chain(self.get_current_player_id())
			opponent_streak = self.longest_chain(self.get_opposite_player_id())
			if current_streak > opponent_streak:
				return self.get_current_player_id()
			if opponent_streak > current_streak:
				return self.get_opposite_player_id()
			return 0
		for i in xrange(self.board_height):
			for j in xrange(self.board_width):
				cell_player = self.get_cell(i, j)
				if cell_player and self._is_win_from_cell(i, j):
					return cell_player
		return 0

	def _is_win_from_cell(self, row, col):
		"""
		Return whether there is a winning set of four connected nodes
		containing the specified cell.
		"""
		return self._max_length_from_cell(row, col) >= self._chain_length_goal

	def is_tie(self):
		"""
		Return whether the game has reached a stalemate, assuming that
		self.is_win() returns False.
		"""
		if self._longest_streak_to_win:
			return self.num_tokens_on_board() == 20
		return 0 not in self._board_array[0]

	def get_counts(self, i, j, d, player_id):
		if not (i + d[0] * (self._chain_length_goal-1) in range(self.board_height) and\
				j + d[1] * (self._chain_length_goal-1) in range(self.board_width)):
			return 0

		count = 0
		for k in range(self._chain_length_goal):
			code = self._board_array[i+d[0]*k][j+d[1]*k]
			if code == player_id:
				count += 1
			elif code == 0:
				pass
			else:
				return 0
		return count

	def chain_groups(self, player_id):
		result = {x:0 for x in range(1, self._chain_length_goal)}
		for i in range(self.board_height):
			for j in range(self.board_width):
				for d in directions:
					count = self.get_counts(i, j, d, player_id)
					if count:
						result[count] += 1
		return result

	def longest_chain(self, player_id):
		"""
		Returns the length of the longest chain of tokens controlled by this player,
		0 if the player has no tokens on the board
		"""
		longest = 0
		for i in xrange(self.board_height):
			for j in xrange(self.board_width):
				if self.get_cell(i, j) == player_id:
					longest = max(longest, self._max_length_from_cell(i, j))
		return longest

	def _max_length_from_cell(self, row, col):
		"""Return the max-length chain containing this cell."""
		return 1 + max(
			self._contig_vector_length(row, col, (1, 0)) + self._contig_vector_length(row, col, (-1, 0)),
			self._contig_vector_length(row, col, (0, 1)) + self._contig_vector_length(row, col, (0, -1)),
			self._contig_vector_length(row, col, (1, 1)) + self._contig_vector_length(row, col, (-1, -1)),
			self._contig_vector_length(row, col, (1, -1)) + self._contig_vector_length(row, col, (-1, 1))
		)

	def _contig_vector_length(self, row, col, dir):
		"""
		Starting in the specified cell and going a step of dir = (row_step, col_step),
		count how many consecutive cells are owned by the same player as the starting cell.
		"""
		count = 0
		player_id = self.get_cell(row, col)
		while (0 <= row < self.board_height and 0 <= col < self.board_width and
			player_id == self.get_cell(row, col)):
			row += dir[0]
			col += dir[1]
			count += 1
		return count - 1

	def chain_cells(self, player_id):
		"""
		Returns a set of all cells on the board that are part of a chain controlled
		by the specified player.

		The return value will be a Python set containing tuples of coordinates.
		For example, a return value might look like:

		set([ ( (0,1),(0,2),(0,3) ), ( (0,1),(1,1) ) ])

		This would indicate a contiguous string of tokens from (0,1)-(0,3) and (0,1)-(1,1).

		The coordinates within a tuple are weakly ordered: any coordinates that are
		adjacent in a tuple are also adjacent on the board.

		Note that single lone tokens are regarded as chains of length 1.  This is
		sometimes useful, but sometimes not; however, it's relatively easy to remove
		such elements via list comprehension or via the built-in Python 'filter' function
		as follows (for example):

		>>> my_big_chains = filter(lambda x: len(x) > 1, myBoard.chain_cells(playernum))

		Also recall that you can convert this set to a list as follows:

		>>> my_list = list( myBoard.chain_cells(playernum) )

		The return value is provided as a set because sets are unique and unordered,
		as is this collection of chains.
		"""
		cells = set()
		for i in xrange(self.board_height):
			for j in xrange(self.board_width):
				if self.get_cell(i, j) == player_id:
					cells.update(self._chain_sets_from_cell(i, j))
		return cells

	def _chain_sets_from_cell(self, row, col):
		""" Return the max-length chain containing this cell """
		return [tuple(x) for x in [
			list(reversed(self._contig_vector_cells(row, col, (1, 0)))) + [(row, col)] + self._contig_vector_cells(row, col, (-1, 0)),
			list(reversed(self._contig_vector_cells(row, col, (0, 1)))) + [(row, col)] + self._contig_vector_cells(row, col, (0, -1)),
			list(reversed(self._contig_vector_cells(row, col, (1, 1)))) + [(row, col)] + self._contig_vector_cells(row, col, (-1, -1)),
			list(reversed(self._contig_vector_cells(row, col, (1, -1)))) + [(row, col)] + self._contig_vector_cells(row, col, (-1, 1))
		]]

	def _contig_vector_cells(self, row, col, dir):
		"""
		Return how many consecutive cells are owned by the same player
		as the specified starting cell, stepping by dir = (row_step, col_step).
		"""
		cells = []
		player_id = self.get_cell(row, col)
		while (0 <= row < self.board_height and 0 <= col < self.board_width and
			player_id == self.get_cell(row, col)):
			row += dir[0]
			col += dir[1]
			cells.append((row, col))
		return cells[:-1]


class ConnectFourRunner(object):
	"""
	Runs a game of Connect Four.

	The rules of this Connect Four game are as follows:

	* The game is a two-player game. Players take turns adding tokens to
	  the board.
	* When a token is added to the board, it is added to a particular column.
	  It "falls" to the unoccupied cell in the column with the largest index.
	* The game ends when one of the two players has four consecutive tokens
	  in a row (either horizontally, vertically, or on 45-degree diagonals),
	  or when the board is completely filled. If the game ends with a player
	  having four consecutive diagonal tokens, that player is the winner.

	The game runner is implemented via callbacks: The two players specify
	callbacks to be called when it's their turn. The callback is passed two
	arguments, self and self.get_board(). The callback functions must return
	integers corresponding to the columns they want to drop a token into.
	"""

	def __init__(self, player1_callback, player2_callback, board=None):
		"""Create a new ConnectFourRunner."""
		self._board = board or ConnectFourBoard()
		self.player1_callback = player1_callback
		self.player2_callback = player2_callback

		global numNodesExpanded
		numNodesExpanded = 0

	def get_board(self):
		"""Return the current game board."""
		return self._board

	def run_game(self, verbose=True):
		"""
		Run the test defined by this test runner.
		Print and return the ID of the winning player.
		"""
		player1 = (self.player1_callback, 1, self._board.board_symbols[1])
		player2 = (self.player2_callback, 2, self._board.board_symbols[2])
		while not self._board.is_game_over():
			for callback, id, symbol in (player1, player2):
				if verbose:
					print self._board
				has_moved = False
				while not has_moved:
					try:
						new_column = callback(self._board.clone())
						print "Player %s (%s) puts a token in column %s" % (id, symbol, new_column)
						self._board = self._board.do_move(new_column)
						has_moved = True
					except InvalidMoveException as ex:
						print ex
						print "Illegal move attempted. Please try again."
						continue
				if self._board.is_game_over():
					break
		winner = self._board.is_win()
		if winner:
			print "Win for %s!" % self._board.board_symbols[winner]
		else:
			print "It's a tie! No winner is declared."
		if verbose:
			print self._board
			
		# TODO: return numNodesExpanded?
		return numNodesExpanded
