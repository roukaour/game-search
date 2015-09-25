# CSE 537 Assignment 2
# Name: Remy Oukaour (107122849), Jian Yang (110168771)
# Email: remy.oukaour@gmail.com, swordyoung@gmail.com

import time
from connectfour import *
from basicplayer import *


def run_game(player1, player2, board=None, verbose=True):
	"""Run a game of Connect Four with the two specified players."""
	game = ConnectFourRunner(player1, player2, board)
	return game.run_game(verbose)


if __name__ == '__main__':

	# New vs. Basic
	minimax_nodesExpanded = 0
	tick = time.clock()
	run_game(new_player, basic_player)
	tock = time.clock()
	executionTime = tock - tick
	print "New vs. Basic:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", minimax_nodesExpanded
	print

	# Alpha-Beta vs. Basic
	alpha_beta_nodesExpanded = 0
	tick = time.clock()
	run_game(alpha_beta_player, basic_player)
	tock = time.clock()
	executionTime = tock - tick
	print "Alpha-Beta vs. Basic:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", alpha_beta_nodesExpanded
