# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 00:19:40 2024

@author: L
"""
from fourInRowGame import Chip, FourInRowGame
import numpy as np
import random
import math
import itertools
from random import sample 
# Create a game

def next_move(env,chip_):
    
    decay_rate = 0.9
    depth = 4
    sample_rate = 0.05
    
    player = chip_
    if player == Chip.RED:
        opponent = Chip.YELLOW
    else:
        opponent = Chip.RED
    
    util_arr = np.zeros(env.columns)
    for i in range(env.columns):
    
        env_c = env.get_env_copy()
        if env_c.column_is_full(i):
            util_arr[i] = -math.inf
            continue
        env_c.drop(player, i)   
        if env_c.column_is_full(i):
            util_arr[i] = -math.inf

        if env_c.check_for_victory():
            util_arr[i] = math.inf
            print('win')
            continue
        
        options = ''.join(str(i) for i in range(env.columns))
    
        draw = itertools.product(options,repeat=(depth*2)-1)
        draw_list = [''.join(d) for d in draw]
        
        sample_list = sample(draw_list, round(len(draw_list)*sample_rate))
    
        counter = 0
        state_util = 0
        for draw in sample_list:
            env_comb = env_c.get_env_copy()
            for count,next_ in enumerate(draw): 
                
                if env_comb.column_is_full(int(next_)):
                    break
                if count%2 == 0:
                    env_comb.drop(opponent,int(next_)) 
                else:
                    env_comb.drop(player,int(next_))
                
                if env_comb.check_for_victory():
                    if count%2  == 0:
                        state_util += (decay_rate**count+1)*-1
                    else:
                        state_util += (decay_rate**count+1)*1                    
                    break
            counter +=1
            if counter%10000 == 0:
                print(i,counter,state_util)
            
        util_arr[i] = state_util
        
    next_move = np.argmax(util_arr)
    return next_move

env = FourInRowGame(6, 7)

while not env.check_for_victory():
    pl1 = next_move(env,Chip.RED)
    env.drop(Chip.RED,pl1)
    env.check_for_victory()
    pl2 = next_move(env,Chip.YELLOW)
    env.drop(Chip.YELLOW,pl2)
    env.check_for_victory()
    env.print()

