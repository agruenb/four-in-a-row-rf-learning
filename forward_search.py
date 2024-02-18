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
#simple example how two forward search players would play against each other
env = FourInRowGame(6, 7)

while not env.check_for_victory():
    pl1 = forward_search_player(env,Chip.RED,4,0.01)
    env.drop(Chip.RED,pl1)
    env.check_for_victory()
    pl2 = forward_search_player(env,Chip.YELLOW,4,0.01)
    env.drop(Chip.YELLOW,pl2)
    env.check_for_victory()
    env.print()

#instantiate a player with the env - current environment, chip_ - color of the player
#depth*2 how deep the tree should go and sample_rate how many samples from all combinations should be picked
#sample rate was introduced to speed up and sample only from a subset
def forward_search_player(env,chip_,depth,sample_rate):
    
    #decay for payouts that are further away in case a high depth is choosen
    decay_rate = 0.9
    
    player = chip_
    if player == Chip.RED:
        opponent = Chip.YELLOW
    else:
        opponent = Chip.RED
    
    #get for the next possible moces a 
    util_arr = np.zeros(env.columns)
    for i in range(env.columns):
        
        #only make moves in columns that are not full
        env_c = env.get_env_copy()
        if env_c.column_is_full(i):
            util_arr[i] = -math.inf
            continue
        env_c.drop(player, i)   
        if env_c.column_is_full(i):
            util_arr[i] = -math.inf

        if env_c.check_for_victory():
            util_arr[i] = math.inf
            #print('win')
            continue
        
        #create products of all possible combinations of all moves
        options = ''.join(str(i) for i in range(env.columns))
        draw = itertools.product(options,repeat=(depth*2)-1)
        draw_list = [''.join(d) for d in draw]
        #create a subset of all states
        sample_list = sample(draw_list, round(len(draw_list)*sample_rate))
        
        #count how often a game is won 
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
                    #as player1 does the 1,3,5.. move only wins after uneven 
                    #moves gives positive reward otherwise opponent has won
                    #with negative reward
                    if count%2  == 0:
                        state_util += (decay_rate**count+1)*-1
                    else:
                        state_util += (decay_rate**count+1)*1                    
                    break
            counter +=1
            if counter%10000 == 0:
                pass#print(i,counter,state_util)
        #update expected utility of the choosen action
        util_arr[i] = state_util
    #return highest utility state
    next_move = np.argmax(util_arr)
    return next_move


