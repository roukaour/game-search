# CSE 537 Assignment 2
# Name: Remy Oukaour (107122849), Jian Yang (110168771)
# Email: remy.oukaour@gmail.com, swordyoung@gmail.com

import time
import connectfour
import basicplayer


def run_game(player1, player2, board=None, verbose=True):
	"""Run a game of Connect Four with the two specified players."""
	game = connectfour.ConnectFourRunner(player1, player2, board)
	return game.run_game(verbose)


if __name__ == '__main__':

	#run_game(basicplayer.human_player, basicplayer.alpha_beta_player)
	#exit(0)

	# New vs. Basic
	tick = time.clock()
	run_game(basicplayer.new_player, basicplayer.basic_player)
	tock = time.clock()
	executionTime = tock - tick
	print "New vs. Basic:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", basicplayer.minimax_nodesExpanded
	print

	# Alpha-Beta vs. Basic
	tick = time.clock()
	run_game(basicplayer.alpha_beta_player, basicplayer.basic_player)
	tock = time.clock()
	executionTime = tock - tick
	print "Alpha-Beta vs. Basic:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", basicplayer.alpha_beta_nodesExpanded
