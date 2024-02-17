# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 22:51:52 2024

@author: L
"""

import math
import random
import time
import numpy as np
from fourInRowGame import Chip, FourInRowGame


tree = {}
tree[1] = { 'player': Chip.RED,
                       'child': [], 'parent': None,
                       'total_node_visits':0, 'total_node_wins':0,
                       'drop':math.inf}

env = FourInRowGame(6, 7)

while not env.check_for_victory():
    red_tree = build_tree(Chip.RED)
    search(red_tree,env)
    drop = best_move(red_tree)
    env.drop(Chip.RED,drop)
    if env.check_for_victory():
        env.print()
        break
    yellow_tree = build_tree(Chip.YELLOW)
    search(yellow_tree,env)
    drop = best_move(yellow_tree)
    env.drop(Chip.YELLOW,drop)
    env.print()
    print('------')


def build_tree(chip_):
    tree = {}
    tree[1] = { 'player': get_opposite_player(chip_),
                           'child': [], 'parent': None,
                           'total_node_visits':0, 'total_node_wins':0,
                           'drop':math.inf}
    return tree

def best_move(tree):
#    if self.root_state.game_over():
#        return -11
    root_childs = tree[1]['child']
    max_value = max([tree[c]['total_node_visits'] for c in root_childs])

    max_nodes = [c for c in root_childs if tree[c]['total_node_visits'] == max_value]
    best_child = random.choice(max_nodes)

    return tree[best_child]['drop']

def search(tree, env):
    start_time = time.process_time()

    num_rollouts = 0
    while num_rollouts < 10000:
        node, env_c = select_nodes(tree,1,env)
        outcome = roll_out(env_c,tree[node]['player'])
        back_propagate(tree,node,outcome)
        num_rollouts += 1 # for calculating statistics

    #run_time = time.process_time() - start_time
    #self.run_time = run_time
    #self.num_rollouts = num_rollouts

def back_propagate(tree, node_id, chip_):
    # For the current player, not the next player
    reward = 0 if chip_ != tree[node_id]['player'] else 1

    while tree[node_id]['parent'] is not None:
        tree[node_id]['total_node_visits'] += 1
        tree[node_id]['total_node_wins'] += reward
        node_id = tree[node_id]['parent']
        
        if chip_ == Chip.EMPTY: # we count it as a loss for every state
            reward = 0
        else:
            reward = 1 - reward # alternates between 0 and 1 because each alternate depth represents different player turns
    tree[node_id]['total_node_visits'] += 1
    
def get_outcome(env):
        if env.check_for_victory():
            if env.check_for_victory_red():
                return Chip.RED
            else:
                return Chip.YELLOW
        else:
            return Chip.EMPTY
    

def roll_out(env,chip_):
    while not env.field_is_full() and not env.check_for_victory():
        chip_ = get_opposite_player(chip_)
        next_move = env.get_next_moves()
        move = random.choice(next_move)
        #print(move,chip_)
        env.drop(chip_,move)
    #env.print()
    return get_outcome(env)

def select_nodes(tree,node_id,env):
    
    node = node_id
    env_c = env.get_env_copy()
    
    while len(tree[node]['child']) != 0:
        children = tree[node]['child']
        
        max_value = max([get_value(tree,n) for n in children])
        max_nodes = [n for n in children if get_value(tree,n) == max_value]

        # randomly select on to expand upon
        node = random.choice(max_nodes)
        env_c.drop(tree[node]['player'],tree[node]['drop'])
        #print(node,tree[node])
        if tree[node]['total_node_visits'] == 0:
            return node,env_c
    
    if not env_c.field_is_full() and not env_c.check_for_victory(): # determines if the state is a terminal state (game over)
        expand(tree, node, env_c)    
        child_nodes = tree[node]['child']
        node = random.choice(child_nodes)
        env_c.drop(tree[node]['player'],tree[node]['drop'])
        #print('expand ',tree[node])
    return node,env_c

def get_opposite_player(chip_):
    if chip_ == Chip.YELLOW:
        return Chip.RED
    else:
        return Chip.YELLOW
    
def expand(tree, node_id, env):
    children = env.get_next_moves()
    for i in children:
        add_children(tree,node_id,i)

    return children    
    

def add_children(tree,parent_id,drop):
    new_id = max(list(tree.keys()))+1
    tree[new_id] = {'player': get_opposite_player(tree[parent_id]['player']),
                           'child': [], 'parent': parent_id,
                           'total_node_visits':0, 'total_node_wins':0,
                           'drop':drop}
    new_childs = tree[parent_id]['child']
    new_childs.append(new_id)
    tree[parent_id]['child'] = new_childs
    

def get_value(tree,node_id):
    if tree[node_id]['total_node_visits'] == 0:
        return math.inf
    elif tree[node_id]['parent'] == None:
        return 0
    else:
        return (tree[node_id]['total_node_wins'] / tree[node_id]['total_node_visits']) + 2 * math.sqrt(math.log(tree[tree[node_id]['parent']]['total_node_visits']) / tree[node_id]['total_node_visits'])
    



