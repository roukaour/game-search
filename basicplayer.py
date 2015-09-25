import random
import collections
from connectfour import *


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
	# Prefer having your pieces in the center of the board.
	for row in xrange(board.board_height):
		for col in xrange(board.board_width):
			if board.get_cell(row, col) == board.get_current_player_id():
				score -= abs(board.board_width // 2 - col)
			elif board.get_cell(row, col) == board.get_opposite_player_id():
				score += abs(board.board_width // 2 - col)
	return score


def new_evaluate(board):
	# TODO: implement for Assignment 2 Part 2 (20 points)
	if board.is_game_over():
		return -1000
	my_chain_groups = board.chain_groups(board.get_current_player_id())
	other_chain_groups = board.chain_groups(board.get_opposite_player_id())
	return (sum(v * 2**k for k, v in my_chain_groups.items()) -
		sum(v * 2**k for k, v in other_chain_groups.items()))


##############################################
# Search functions (and utility functions)
##############################################


def get_all_next_moves(board):
	"""
	Return a generator of all moves that the current player could take
	from this position.
	"""
	for column in xrange(board.board_width):
		try:
			yield (column, board.do_move(column))
		except InvalidMoveException:
			pass


def is_terminal(board):
	"""
	Generic terminal state check, true when the game has ended.
	"""
	return board.is_game_over()


Node = collections.namedtuple('Node', ('score', 'column'))


def minimax(board, depth,
	eval_fn=basic_evaluate,
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal):
	"""
	Do a minimax search to the specified depth on the specified board.
	Return the column that the search finds to add a token to.

	board: the ConnectFourBoard instance to evaluate
	depth: the depth of the search tree (measured in maximum distance
	       from a leaf to the root)
	eval_fn: (optional) the evaluation function to use to give a value
	         to a leaf of the tree
	"""
	# TODO: implement for Assignment 2 Part 1 (20 points)
	node = minimax_helper(board, depth,
		eval_fn, get_next_moves_fn, is_terminal_fn)
	return node.column


def minimax_helper(board, depth,
	eval_fn, get_next_moves_fn, is_terminal_fn):
	if depth <= 0 or is_terminal_fn(board):
		return Node(-eval_fn(board), None)
	child_nodes = []
	for column, new_board in get_next_moves_fn(board):
		child_node = minimax_helper(new_board, depth - 1,
			eval_fn, get_next_moves_fn, is_terminal_fn)
		child_nodes.append(Node(child_node.score, column))
	max_child_node = max(child_nodes, key=lambda c: c.score)
	return Node(-max_child_node.score, max_child_node.column)


infinity = float('inf')


def alpha_beta_search(board, depth,
	eval_fn=new_evaluate,
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal):
	# TODO: implement for Assignment 2 Part 3 (30 points)
	node = alpha_beta_helper(board, depth,
		Node(-infinity, None), Node(infinity, None), True,
		eval_fn, get_next_moves_fn, is_terminal_fn)
	return node.column


def alpha_beta_helper(board, depth, alpha, beta, is_max,
	eval_fn, get_next_moves_fn, is_terminal_fn):
	print 'alpha', alpha, 'beta', beta
	if depth <= 0 or is_terminal_fn(board):
		return Node(-eval_fn(board), None)
	if is_max:
		v = Node(-infinity, None)
		for column, new_board in get_next_moves_fn(board):
			child_node = alpha_beta_helper(new_board, depth - 1,
				alpha, beta, False, eval_fn, get_next_moves_fn, is_terminal_fn)
			print 'child_node', child_node
			v = Node(max(v.score, child_node.score), column)
			print 'v', v
			alpha = max(alpha, v)
			print 'alpha', alpha
			if beta.score <= alpha.score:
				break
	else:
		v = Node(infinity, None)
		for column, new_board in get_next_moves_fn(board):
			child_node = alpha_beta_helper(new_board, depth - 1,
				alpha, beta, True, eval_fn, get_next_moves_fn, is_terminal_fn)
			print 'child_node', child_node
			v = Node(min(v.score, child_node.score), column)
			print 'v', v
			beta = min(beta, v)
			print 'beta', beta
			if beta.score <= alpha.score:
				break
	return Node(-v.score, v.column)


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
	return minimax(board, depth=4, eval_fn=basic_evaluate)


def new_player(board):
	"""A Connect Four player callback that calls minimax with new_evaluate."""
	return minimax(board, depth=4, eval_fn=new_evaluate)


def alpha_beta_player(board):
	"""A Connect Four player callback that calls alpha_beta_search with new_evaluate."""
	return alpha_beta_search(board, depth=4, eval_fn=new_evaluate)
