# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 23:23:17 2024

@author: L
"""

from fourInRowGame import Chip, FourInRowGame
import numpy as np
import random
import math

#simple example how two minimax players would play against each other
env = FourInRowGame(6, 7)

while not env.check_for_victory():
    pl1 = minimax_player(env,Chip.RED,5)
    env.drop(Chip.RED,pl1)
    if env.check_for_victory():
        env.print()
        break
    pl2 = minimax_player(env,Chip.YELLOW,5)
    env.drop(Chip.YELLOW,pl2)
    env.check_for_victory()
    env.print()
    print('------')


#instantiate a player with the env - current environment, chip_ - color of the player
#depth how deep the tree should go and pruning if pruning should be applied 
def minimax_player(env,chip_,depth,pruning = True):
    alpha = -math.inf
    beta = math.inf
    
    #if only a short window is used to look forward place first move in middle
    # as it is proven to be the best move
    new_game = True
    for col in range(env.columns):
        if env.column_height(col) != 0:
            new_game = False
    if new_game == True and depth < 7:
        return math.floor(env.columns/2)
            
    #choose between model with or without pruning
    if pruning == True:
        min_eval, move_series = alpha_beta_pruning(env,depth,alpha,beta,True,chip_,chip_)
    else:
        min_eval, move_series = minimax(env,depth,True,chip_,chip_)
    return move_series[0]


#env is the current board, depth how deep the tree should be build further
#maximizingPlayer a boolean if min or max should be searched
#next_chip is the chip placed in the next round and player is the next player
def minimax(env_, depth, maximizingPlayer,next_chip,player):
    if depth == 4:
        pass#print(1)
    move_series = []
    
    #figure out next chip for recursive call of next move
    if next_chip == Chip.RED:
        opposit = Chip.YELLOW
    else:
        opposit = Chip.RED
    
    #if max depth is reached or game is won by one side evaluate
    #as evaluate position is build from the red players view
    #inverse if player has yellow chips
    if depth == 0 or env_.check_for_victory():
        if player == Chip.RED:
            direction = 1
        else:
            direction = -1
        return direction*env_.evaluate_positions(),[]
    
    
    #is player is maximising set his value to negative infinity
    #if the eval function of one action is better, set as new eval
    if maximizingPlayer:
        max_eval = -math.inf
        max_col = 0
        #get all possible next moves and recursivly call them
        for next_ in env_.get_next_moves():
            env_next = env_.get_env_copy()
            env_next.drop(next_chip,int(next_)) 
            eval_,prev_moves = minimax(env_next, depth - 1, False,opposit,player)
            if eval_ > max_eval: 
                #max_eval = max(max_eval, eval_)
                max_eval = eval_
                max_col = next_
                move_series = prev_moves
        move_series.insert(0,max_col)
        return max_eval, move_series
    #is player is minimizing set his value to  infinity
    #if the eval function of one action is worse, set as new eval
    else:
        min_eval = math.inf
        min_col = 0
        #get all possible next moves and recursivly call them
        for next_ in env_.get_next_moves():
            env_next = env_.get_env_copy()
            env_next.drop(next_chip,int(next_)) 
            eval_,prev_moves = minimax(env_next, depth - 1, True,opposit,player)
            if eval_ < min_eval: 
                #min_eval = min(min_eval, eval_)
                min_eval = eval_
                min_col = next_
                move_series = prev_moves
        move_series.insert(0,min_col)
        return min_eval, move_series

def alpha_beta_pruning(env_, depth, alpha, beta, maximizingPlayer,next_chip,player):
    if depth == 4:
        pass#print(1)
    move_series = []
    
    #figure out next chip for recursive call of next move    
    if next_chip == Chip.RED:
        opposit = Chip.YELLOW
    else:
        opposit = Chip.RED
        
    #if max depth is reached or game is won by one side evaluate
    #as evaluate position is build from the red players view
    #inverse if player has yellow chips    
    if depth == 0 or env_.check_for_victory():
        if player == Chip.RED:
            direction = 1
        else:
            direction = -1
        return direction*env_.evaluate_positions(),[]

    #is player is maximising set his value to negative infinity
    #if the eval function of one action is better, set as new eval
    
    if maximizingPlayer:
        max_eval = -math.inf
        max_col = 0
        for next_ in env_.get_next_moves():
            env_next = env_.get_env_copy()
            env_next.drop(next_chip,int(next_)) 
            eval_,prev_moves = alpha_beta_pruning(env_next, depth - 1, alpha, beta, False,opposit,player)
            if eval_ > max_eval: #max_eval = max(max_eval, eval_)
                max_eval = eval_
                max_col = next_
                move_series = prev_moves
            
            alpha = max(alpha, eval_)
            if beta <= alpha:
                #print('pruning',depth)
                break
        
        move_series.insert(0,max_col)
        return max_eval, move_series
    else:
        min_eval = math.inf
        min_col = 0
        for next_ in env_.get_next_moves():
            env_next = env_.get_env_copy()
            env_next.drop(next_chip,int(next_)) 
            eval_,prev_moves = alpha_beta_pruning(env_next, depth - 1, alpha, beta, True,opposit,player)
            if eval_ < min_eval: #min_eval = min(min_eval, eval_)
                min_eval = eval_
                min_col = next_
                move_series = prev_moves
                
            beta = min(beta, eval_)
            if beta <= alpha:
                #print('pruning',depth)
                break
        
        move_series.insert(0,min_col)
        return min_eval, move_series






