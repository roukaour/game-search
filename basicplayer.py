import random
import connectfour

Infinity = float('inf')


##############################################
# Evaluation functions
##############################################


def basic_evaluate(board):
	"""
	The original focused-evaluate function from the lab.
	"""
	if board.is_game_over():
		# If the game has been won, we know that it must have been won or ended
		# by the previous move. The previous move was made by our opponent.
		# Therefore, we can't have won, so return -1000.
		# (Note that this causes a tie to be treated like a loss.)
		return -1000
	score = board.longest_chain(board.get_current_player_id()) * 10
	# Prefer having your pieces in the center of the board
	for row in xrange(board.board_height):
		for col in xrange(board.board_width):
			if board.get_cell(row, col) == board.get_current_player_id():
				score -= abs(board.board_width // 2 - col)
			elif board.get_cell(row, col) == board.get_opposite_player_id():
				score += abs(board.board_width // 2 - col)
	return score


def new_evaluate(board):
	"""
	TODO: improve this position evaluation function and explain it.
	"""
	if board.is_game_over():
		return -1000
	my_chain_groups = board.chain_groups(board.get_current_player_id())
	other_chain_groups = board.chain_groups(board.get_opposite_player_id())
	return (sum(v * 2**k for k, v in my_chain_groups.items()) -
		sum(v * 2**k for k, v in other_chain_groups.items()))


##############################################
# Search utility functions
##############################################


def get_all_next_moves(board):
	"""
	Return a generator of all moves that the current player could take
	from this position.
	"""
	for column in xrange(board.board_width):
		try:
			yield (column, board.do_move(column))
		except connectfour.InvalidMoveException:
			pass


def is_terminal(board):
	"""
	Generic terminal state check, true when the game has ended.
	"""
	return board.is_game_over()


##############################################
# Search functions
##############################################


class Node(object):
	"""Store a node in a Connect Four game search tree."""

	def __init__(self, score, column=None):
		"""Initialize this game tree node."""
		self.score = score
		self.column = column

	def __str__(self):
		"""Return a printable string representation of this node."""
		return 'Node(%s, %d)' % (str(self.score), self.column)

	def __repr__(self):
		"""Return a string representation of this node."""
		return str(self)

	def __neg__(self):
		"""Return this node with a negated score."""
		return Node(-self.score, self.column)

	def __cmp__(self, other):
		"""Return the comparison of this node with another one (1, 0, or -1)."""
		return cmp(self.score, other.score)


minimax_nodesExpanded = 0

def minimax(board, depth, increment,
	eval_fn=basic_evaluate,
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal):
	"""
	Do a minimax search on the specified board to the specified depth.
	Return the column that the search finds to add a token to.

	If increment is True, increment the global variable minimax_nodesExpanded
	for every node that gets expanded.
	"""
	node = minimax_helper(board, depth, increment,
		eval_fn, get_next_moves_fn, is_terminal_fn)
	return node.column

def minimax_helper(board, depth, increment,
	eval_fn, get_next_moves_fn, is_terminal_fn):
	"""
	Do a recursive minimax search on the specified board to the specified depth.
	Return the node with the best score and the corresponding column move.

	If increment is True, increment the global variable minimax_nodesExpanded
	for every node that gets expanded.

	Since Connect Four is a zero-sum game, taking the minimum score on alternate
	levels of the search tree can be replaced by taking the maximum of the
	negated scores. This variant of minimax is called negamax.
	"""
	global minimax_nodesExpanded
	if increment:
		minimax_nodesExpanded += 1
	if depth <= 0 or is_terminal_fn(board):
		return -Node(eval_fn(board))
	best_node = Node(-Infinity)
	for column, new_board in get_next_moves_fn(board):
		child_node = minimax_helper(new_board, depth - 1, increment,
			eval_fn, get_next_moves_fn, is_terminal_fn)
		if child_node > best_node:
			best_node = Node(child_node.score, column)
	return -best_node


alpha_beta_nodesExpanded = 0

def alpha_beta_search(board, depth, increment,
	eval_fn=new_evaluate,
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal):
	"""
	Do a minimax search with alpha-beta pruning on the specified board
	to the specified depth.
	Return the column that the search finds to add a token to.

	If increment is True, increment the global variable alpha_beta_nodesExpanded
	for every node that gets expanded.
	"""
	node = alpha_beta_helper(board, depth, increment, -Infinity, Infinity,
		eval_fn, get_next_moves_fn, is_terminal_fn)
	return node.column

def alpha_beta_helper(board, depth, increment, alpha, beta,
	eval_fn, get_next_moves_fn, is_terminal_fn):
	"""
	Do a recursive minimax search with alpha-beta pruning on the specified board
	to the specified depth.
	Return the column that the search finds to add a token to.

	If increment is True, increment the global variable alpha_beta_nodesExpanded
	for every node that gets expanded.
	"""
	global alpha_beta_nodesExpanded
	if increment:
		alpha_beta_nodesExpanded += 1
	if depth <= 0 or is_terminal_fn(board):
		return -Node(eval_fn(board))
	best_node = Node(-Infinity)
	for column, new_board in get_next_moves_fn(board):
		child_node = alpha_beta_helper(new_board, depth - 1, increment,
			-beta, -alpha, eval_fn, get_next_moves_fn, is_terminal_fn)
		if child_node > best_node:
			best_node = Node(child_node.score, column)
		alpha = max(alpha, best_node.score)
		if alpha >= beta:
			break
	return -best_node


##############################################
# Players
##############################################


def human_player(board):
	"""A Connect Four player callback that asks the user what to do."""
	target = None
	valid_targets = xrange(board.board_width)
	while True:
		target = raw_input('Pick a column #: --> ')
		try:
			target = int(target)
		except ValueError:
			target = None
		if target not in valid_targets:
			print 'Please specify a valid integer column number'
		else:
			break
	return target


def random_player(board):
	"""A Connect Four player callback that picks a column at random."""
	return random.choice([move for move, new_board in get_all_next_moves(board)])


def basic_player(board):
	"""A Connect Four player callback that calls minimax with basic_evaluate."""
	return minimax(board, depth=4, increment=False, eval_fn=basic_evaluate)


def new_player(board):
	"""A Connect Four player callback that calls minimax with new_evaluate."""
	return minimax(board, depth=4, increment=True, eval_fn=new_evaluate)


def alpha_beta_player(board):
	"""A Connect Four player callback that calls alpha_beta_search with new_evaluate."""
	return alpha_beta_search(board, depth=4, increment=True, eval_fn=new_evaluate)
