# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:45:10 2024

@author: L
"""

from fourInRowGame import Chip, FourInRowGame
import numpy as np
import random

# Create a game
env = FourInRowGame(6, 7)

env.drop(Chip.RED, 0)
#env.drop(Chip.YELLOW, 0)
#env.drop(Chip.RED, 2)
#env.drop(Chip.YELLOW, 2)
#env.drop(Chip.RED, 3)
#env.drop(Chip.YELLOW, 3)
#env.drop(Chip.RED, 1)
#env.drop(Chip.YELLOW, 3)

for r in range(env.rows):
    for c in range(env.columns):
        env.drop(Chip.RED, c)


a,b = cenv.evaluate_positions()
env.print()

env_copy = env.get_env_copy()

a1,b1 = env_copy.evaluate_positions()
env_copy.print()

# Drop different chips into the field
# Warning: the drop() method does not check for victory or what player played last
env.drop(Chip.RED, 0)
env.drop(Chip.YELLOW, 0)
env.drop(Chip.RED, 0)
env.drop(Chip.YELLOW, 0)
env.drop(Chip.RED, 0)
env.drop(Chip.YELLOW, 0)

env.drop(Chip.RED, 6)
env.drop(Chip.YELLOW, 6)

# Print the field in a readable format
env.print()

# Check colum heights
print("Column 0 height:", env.column_height(0))
print("Column 1 height:", env.column_height(1))
print("Column 6 height:", env.column_height(6))

env.check_for_victory()

# some more examples
env_win = FourInRowGame(6, 7)
env_win.drop(Chip.RED, 1)
#env_win.drop(Chip.RED, 2)
env_win.drop(Chip.RED, 2)
env_win.drop(Chip.RED, 3)
env_win.drop(Chip.RED, 3)
env_win.drop(Chip.RED, 3)
env_win.drop(Chip.YELLOW, 0)
env_win.drop(Chip.YELLOW, 0)
env_win.drop(Chip.YELLOW, 1)
env_win.drop(Chip.YELLOW, 2)
env_win.drop(Chip.YELLOW, 2)
env_win.drop(Chip.YELLOW, 3)
env_win.drop(Chip.YELLOW, 4)
env_win.drop(Chip.RED, 4)
env_win.drop(Chip.RED, 5)
env_win.drop(Chip.YELLOW, 4)
env_win.drop(Chip.YELLOW, 5)

#env_win.drop(Chip.YELLOW, 6)
print("Four in a row:", env_win.check_for_victory())
env_win.print()

# for RF learning use the play_game() function
rf_env = FourInRowGame(6, 7)

# play_game() checks for a victory after each move
victory = rf_env.play_game(Chip.YELLOW, 4)

print("Victory:", victory)

rf_env.print()

# to get a simple numpy array representation of the game state use get_simple_slots()
rf_env.get_simple_slots()

#reset the environment

rf_env.reset()
rf_env.print()

# simple reinforcement learning example. It should just show how the environment could be used.
# For example, if one column is full the amount of possible actions change. I am not sure how to
# handle that
# Also representing the state as a single number is possibly very difficult due to the large state space

def random_rf_episode():
    rf_env.reset()
    for i in range(42):# max 42 moves in a game
        if i % 2 == 0:
            #player one
            random_col = random.randint(0, 6)
            # trying to put into full column
            if rf_env.column_height(random_col) == 6:
                return -100 # invalid move is bad
            victory = rf_env.play_game(Chip.YELLOW, random_col)
            if victory:
                return 200 # won the game is good
        else:
            #player two
            random_col = random.randint(0, 6)
            # trying to put into full column
            if rf_env.column_height(random_col) == 6:
                return 0 # invalid move results in no reward
            victory = rf_env.play_game(Chip.RED, random_col)
            if victory:
                return -500 # high penalty for defeat
    return 0

# run this cell multiple times and see different rewards (YELLOW wins gives positive reward)
print("Random reward: ", random_rf_episode())
rf_env.print()




