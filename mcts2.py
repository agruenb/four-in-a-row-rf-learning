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
#simple example how two MCTS players would play against each other
env = FourInRowGame(6, 7)

while not env.check_for_victory():
    red_tree = build_tree(Chip.RED)
    search(red_tree,env,5000)
    drop = best_move(red_tree)
    env.drop(Chip.RED,drop)
    if env.check_for_victory():
        env.print()
        break
    drop = mcts_player(env,Chip.YELLOW,5000)
    env.drop(Chip.YELLOW,drop)
    env.print()
    print('------')

#standard mcts implementation
def mcts_player(env,chip_,rollouts):
    tree = build_tree(chip_)
    search(tree,env,rollouts)
    return best_move(tree)

#build a tree with only the root
def build_tree(chip_):
    tree = {}
    tree[1] = { 'player': get_opposite_player(chip_),
                           'child': [], 'parent': None,
                           'total_node_visits':0, 'total_node_wins':0,
                           'drop':math.inf}
    return tree

#choose best move from the children of the tree
#that is generally the child with the most visits
def best_move(tree):
    root_childs = tree[1]['child']
    max_value = max([tree[c]['total_node_visits'] for c in root_childs])

    max_nodes = [c for c in root_childs if tree[c]['total_node_visits'] == max_value]
    best_child = random.choice(max_nodes)

    return tree[best_child]['drop']

#simulate rollouts many possible games
#choose node with highest UCB until leaf and rollout
def search(tree, env, rollouts):
    start_time = time.process_time()

    num_rollouts = 0
    while num_rollouts < rollouts:
        node, env_c = select_nodes(tree,1,env)
        outcome = roll_out(env_c,tree[node]['player'])
        back_propagate(tree,node,outcome)
        num_rollouts += 1 # for calculating statistics

    
#move the value up alternating between the players
#until root node reached
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
    
# check if outcome is victory by a player or board is full and return
def get_outcome(env):
        if env.check_for_victory():
            if env.check_for_victory_red():
                return Chip.RED
            else:
                return Chip.YELLOW
        else:
            return Chip.EMPTY
    
#make random moves until won or board is full
def roll_out(env,chip_):
    while not env.field_is_full() and not env.check_for_victory():
        chip_ = get_opposite_player(chip_)
        next_move = env.get_next_moves()
        move = random.choice(next_move)
        #print(move,chip_)
        env.drop(chip_,move)
    #env.print()
    return get_outcome(env)

# get children of currenct node until leave (no children) is reached
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

# invert the chip color
def get_opposite_player(chip_):
    if chip_ == Chip.YELLOW:
        return Chip.RED
    else:
        return Chip.YELLOW
    
# add children to the tree for possible next moves    
def expand(tree, node_id, env):
    children = env.get_next_moves()
    for i in children:
        add_children(tree,node_id,i)

    return children    
    
#tree structure was implemented using a dictionary
def add_children(tree,parent_id,drop):
    new_id = max(list(tree.keys()))+1
    tree[new_id] = {'player': get_opposite_player(tree[parent_id]['player']),
                           'child': [], 'parent': parent_id,
                           'total_node_visits':0, 'total_node_wins':0,
                           'drop':drop}
    new_childs = tree[parent_id]['child']
    new_childs.append(new_id)
    tree[parent_id]['child'] = new_childs
    
#calculate UCB from node
def get_value(tree,node_id):
    if tree[node_id]['total_node_visits'] == 0:
        return math.inf
    elif tree[node_id]['parent'] == None:
        return 0
    else:
        return (tree[node_id]['total_node_wins'] / tree[node_id]['total_node_visits']) + 2 * math.sqrt(math.log(tree[tree[node_id]['parent']]['total_node_visits']) / tree[node_id]['total_node_visits'])
    



