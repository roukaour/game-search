import random

from connectfour import *


def run_game(player1, player2, board=None):
	"""Run a game of Connect Four with the two specified players."""
	game = ConnectFourRunner(player1, player2, board)
	return game.run_game()


##############################################
# Evaluation functions
##############################################


def basic_evaluate(board):
	"""
	The original focused-evaluate function from the lab.
	"""
	if board.is_game_over():
		# If the game has been won, we know that it must have been
		# won or ended by the previous move.
		# The previous move was made by our opponent.
		# Therefore, we can't have won, so return -1000.
		# (note that this causes a tie to be treated like a loss)
		score = -1000
	else:
		score = board.longest_chain(board.get_current_player_id()) * 10
		# Prefer having your pieces in the center of the board.
		for row in range(6):
			for col in range(7):
				if board.get_cell(row, col) == board.get_current_player_id():
					score -= abs(3-col)
				elif board.get_cell(row, col) == board.get_other_player_id():
					score += abs(3-col)
	return score


def new_evaluate(board):
	# TODO: implement for Assignment 2 Part 2 (20 points)
	raise NotImplementedError


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


def minimax(board, depth,
	eval_fn=basic_evaluate,
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal,
	verbose=True):
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
	raise NotImplementedError


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
	valid_targets = range(board.board_width)
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
