# CSE 537 Assignment 2
# Name: Remy Oukaour (107122849), Jian Yang (110168771)
# Email: remy.oukaour@gmail.com, swordyoung@gmail.com

from connectfour import *
from players import *

# Play a game with random going first and human going second
board = ConnectFourBoard(chain_length_goal=3)
run_game(random_player, human_player, board)
