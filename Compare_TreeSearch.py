# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 18:57:21 2024

@author: L
"""

import time
import pandas as pd
import math

#MCTS vs Forward Search
mcts_fwd_20 = {}
for i in range(0,20):
    env = FourInRowGame(6, 7)
    
    mcts_fwd_eval= []
    rounds = 0
    while not env.check_for_victory() and not env.field_is_full():
        start_time = time.process_time()
        drop = forward_search_player(env,Chip.RED,4,0.01)
        env.drop(Chip.RED,drop)
        run_time_fwd = time.process_time() - start_time
        if env.check_for_victory():
            env.print()
            break

        start_time = time.process_time()
        drop = mcts_player(env,Chip.YELLOW,5000)
        env.drop(Chip.YELLOW,drop)
        env.print()
        run_time_mcts = time.process_time() - start_time
        
        print('')
        print(run_time_fwd,run_time_mcts)
        rounds +=1
        mcts_fwd_eval.append([run_time_fwd,run_time_mcts,rounds])
        
    if env.field_is_full():
        chip_ = 'DRAW'
        algo_ = ''        
    elif env.check_for_victory_red():
        chip_ = 'RED'
        algo_ = 'FWD'
    else:
        chip_ = 'Yellow'
        algo_ = 'MCTS'
    print(chip_,algo_,i)   
    mcts_fwd_20[i] = { 'winner': chip_, 'algorithm': algo_,'Round': rounds,
                   'time 1': sum([x[0] for x in mcts_fwd_eval])/len(mcts_fwd_eval), 'time 2': sum([x[1] for x in mcts_fwd_eval])/len(mcts_fwd_eval)}
#Statistics in  df_mcts_fwd_gr  
df_mcts_fwd = pd.DataFrame.from_dict(mcts_fwd_20)
df_mcts_fwd = df_mcts_fwd.T
df_mcts_fwd_gr = df_mcts_fwd.groupby(['winner','algorithm']).agg({'Round':['count','mean'],'time 1':'mean','time 2':'mean'})

#FWD vs Pruning
fwd_ab_20 = {}
for i in range(0,20):
    env = FourInRowGame(6, 7)
    
    fwd_prun_eval= []
    rounds = 0
    while not env.check_for_victory() and not env.field_is_full():
        start_time = time.process_time()
        drop = forward_search_player(env,Chip.RED,4,0.01)
        env.drop(Chip.RED,drop)
        run_time_fwd = time.process_time() - start_time
        if env.check_for_victory():
            env.print()
            break
        
        start_time = time.process_time()
        drop = minimax_player(env,Chip.YELLOW,5)
        env.drop(Chip.YELLOW,drop)
        env.print()
        run_time_mcts = time.process_time() - start_time
        
        print('')
        print(run_time_fwd,run_time_mcts)
        rounds +=1
        fwd_prun_eval.append([run_time_fwd,run_time_mcts,rounds])
        
    if env.field_is_full():
        chip_ = 'DRAW'
        algo_ = ''        
    elif env.check_for_victory_red():
        chip_ = 'RED'
        algo_ = 'FWD'
    else:
        chip_ = 'Yellow'
        algo_ = 'Prunnig'
    print(chip_,algo_,i)   
    fwd_ab_20[i] = { 'winner': chip_, 'algorithm': algo_,'Round': rounds,
                   'time 1': sum([x[0] for x in fwd_prun_eval])/len(fwd_prun_eval), 'time 2': sum([x[1] for x in fwd_prun_eval])/len(fwd_prun_eval)}
#Statistics in  df_fwd_ab_gr      
df_fwd_ab = pd.DataFrame.from_dict(fwd_ab_20)
df_fwd_ab = df_fwd_ab.T
df_fwd_ab_gr = df_fwd_ab.groupby(['winner','algorithm']).agg({'Round':['count','mean'],'time 1':'mean','time 2':'mean'})

#MCTS vs Pruning
mcts_ab_20 = {}
for i in range(0,20):
    env = FourInRowGame(6, 7)
    
    mcts_prun_eval= []
    rounds = 0
    while not env.check_for_victory() and not env.field_is_full():
        start_time = time.process_time()
        drop = minimax_player(env,Chip.RED,5)
        env.drop(Chip.RED,drop)
        run_time_fwd = time.process_time() - start_time
        if env.check_for_victory():
            env.print()
            break
        
        start_time = time.process_time()
        drop = mcts_player(env,Chip.YELLOW,5000)
        env.drop(Chip.YELLOW,drop)
        env.print()
        run_time_mcts = time.process_time() - start_time
        
        print('')
        print(run_time_fwd,run_time_mcts)
        rounds +=1
        mcts_prun_eval.append([run_time_fwd,run_time_mcts,rounds])
        
    if env.field_is_full():
        chip_ = 'DRAW'
        algo_ = ''        
    elif env.check_for_victory_red():
        chip_ = 'RED'
        algo_ = 'Prunnig'
    else:
        chip_ = 'Yellow'
        algo_ = 'MCTS'
    print(chip_,algo_,i)   
    mcts_ab_20[i] = { 'winner': chip_, 'algorithm': algo_,'Round': rounds,
                   'time 1': sum([x[0] for x in mcts_prun_eval])/len(mcts_prun_eval), 'time 2': sum([x[1] for x in mcts_prun_eval])/len(mcts_prun_eval)}
#Statistics in  df_mcts_ab_gr      
df_mcts_ab = pd.DataFrame.from_dict(mcts_ab_20)
df_mcts_ab = df_mcts_ab.T
df_mcts_ab_gr = df_mcts_ab.groupby(['winner','algorithm']).agg({'Round':['count','mean'],'time 1':'mean','time 2':'mean'})
     
    