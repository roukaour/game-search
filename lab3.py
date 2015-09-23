# CSE 537 Assignment 2
# Name: Remy Oukaour (107122849), Jian Yang (110168771)
# Email: remy.oukaour@gmail.com, swordyoung@gmail.com

INFINITY = float('inf')

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#	  search to depth 6 to decide on a move. Player AB does alpha-beta
#	  search to depth 6.
#	  The game is played without a time limit. Which player will play better?
#
#	  1. MM will play better than AB.
#	  2. AB will play better than MM.
#	  3. They will play with the same level of skill.
ANSWER1 = 0

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 0

### 2. Connect Four
from connectfour import *
from basicplayer import *

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)
run_game(random_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
	"""
	Given a board, return a numeric rating of how good
	that board is for the current player.
	A return value >= 1000 means that the current player has won;
	a return value <= -1000 means that the current player has lost
	"""	
	raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
def quick_to_win_player(board):
	return minimax(board, depth=4, eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth, eval_fn,
	# NOTE: You should use get_next_moves_fn when generating
	# next board configurations, and is_terminal_fn when
	# checking game termination.
	# The default functions set here will work
	# for connect_four.
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal):
	raise NotImplementedError

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
def alphabeta_player(board):
	return alpha_beta_search(board, depth=8, eval_fn=new_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
def ab_iterative_player(board):
	return run_search_function(board,
		search_fn=alpha_beta_search,
		eval_fn=focused_evaluate,
		timeout=5)
#run_game(human_player, ab_iterative_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#	raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)
