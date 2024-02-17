# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 23:23:17 2024

@author: L
"""

from fourInRowGame import Chip, FourInRowGame
import numpy as np
import random
import math

def minimax(env_, depth, maximizingPlayer,next_chip,player):
    if depth == 4:
        print(1)
    move_series = []
    
    if next_chip == Chip.RED:
        opposit = Chip.YELLOW
    else:
        opposit = Chip.RED
    
    if depth == 0 or env_.check_for_victory():
        if player == Chip.RED:
            direction = 1
        else:
            direction = -1
        return direction*env_.evaluate_positions(),[]
    
    if maximizingPlayer:
        max_eval = -math.inf
        max_col = 0
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
    else:
        min_eval = math.inf
        min_col = 0
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
        print(1)
    move_series = []
    
    if next_chip == Chip.RED:
        opposit = Chip.YELLOW
    else:
        opposit = Chip.RED
    
    if depth == 0 or env_.check_for_victory():
        if player == Chip.RED:
            direction = 1
        else:
            direction = -1
        return direction*env_.evaluate_positions(),[]
    
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


env = FourInRowGame(6, 7)
env.drop(Chip.YELLOW, 3)
env.drop(Chip.RED, 4)
env.drop(Chip.YELLOW, 4)
val,moves = minimax(env,5,True,Chip.RED,Chip.RED)

alpha = -math.inf
beta = math.inf

env2 = FourInRowGame(6, 7)
env2.drop(Chip.YELLOW, 3)
env2.drop(Chip.RED, 4)
env2.drop(Chip.YELLOW, 4)
val2,moves2 = alpha_beta_pruning(env2,5,alpha,beta,True,Chip.RED,Chip.RED)


