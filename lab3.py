# CSE 537 Assignment 2
# Name: Remy Oukaour (107122849), Jian Yang (110168771)
# Email: remy.oukaour@gmail.com, swordyoung@gmail.com

import time
from connectfour import *
from players import *

if __name__ == '__main__':

	# This is for testing; TODO: remove from final submission
	# Random vs. Random
	tick = time.clock()
	nodesExpanded = run_game(random_player, random_player)
	tock = time.clock()
	executionTime = tock - tick
	print "Random vs. Random:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", nodesExpanded
	print

	# This is for testing; TODO: remove from final submission
	board = ConnectFourBoard(chain_length_goal=4)
	run_game(random_player, human_player, board)
	exit(0)

	# New vs. Basic
	tick = time.clock()
	nodesExpanded = run_game(new_player, basic_player)
	tock = time.clock()
	executionTime = tock - tick
	print "New vs. Basic:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", nodesExpanded
	print

	# Alpha-Beta vs. Basic
	tick = time.clock()
	nodesExpanded = run_game(alpha_beta_player, basic_player)
	tock = time.clock()
	executionTime = tock - tick
	print "Alpha-Beta vs. Basic:"
	print "Execution Time:", executionTime
	print "Nodes Expanded:", nodesExpanded
