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
	for i in xrange(board.board_width):
		try:
			yield (i, board.do_move(i))
		except InvalidMoveException:
			pass


def is_terminal(depth, board):
	"""
	Generic terminal state check, true when maximum depth is reached or
	the game has ended.
	"""
	return depth <= 0 or board.is_game_over()


Node = collections.namedtuple('Node', ('score', 'moves'))


def get_minimax(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn):
	if is_terminal_fn(depth, board):
		return Node(-eval_fn(board), [])
	if True:
		values = [Node(get_minimax(child_board, depth-1, eval_fn,
			get_next_moves_fn, is_terminal_fn), move)
			for move, child_board in get_next_moves_fn(board)]
	else:
		# Debug code
		# TODO: remove me in final submission
		values = []
		for move, child_board in get_next_moves_fn(board):
			print 'moving', move
			print child_board
			submax = get_minimax(child_board, depth-1, eval_fn,
				get_next_moves_fn, is_terminal_fn)
			print 'submax', submax
			values.append(Node(submax, move))
	max_index = max(values, key=lambda x: x.score.score)
	return Node(-max_index.score.score, [max_index.moves] + max_index.score.moves)


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
	result = get_minimax(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn)
	return result.moves[0]


def alpha_beta_search(board, depth,
	# NOTE: You should use get_next_moves_fn when generating
	# next board configurations, and is_terminal_fn when
	# checking game termination.
	# The default functions set here will work
	# for connect_four.
	eval_fn=new_evaluate,
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal):
	# TODO: implement for Assignment 2 Part 3 (30 points)
	# Write an alpha-beta-search procedure that acts like the minimax-search
	# procedure, but uses alpha-beta pruning to avoid searching bad ideas
	# that can't improve the result. The tester will check your pruning by
	# counting the number of static evaluations you make.
	raise NotImplementedError


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
