# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:41:33 2019

@author: NATE Z

This program simulates multiple games of war and organizes the game stats into
a dataframe.
"""

import random
import numpy as np
import pandas as pd
import time

deck_size = 52
suits = deck_size/4
WL = 3
num_games = 100000

start = time.time()
#1:wins,value,aces,kings,lowest_num_cards,warswon,dblwarswon,tripwarswon,quadwarswon
#2:wins,value,aces,kings,lowest_num_cards,warswon,dblwarswon,tripwarswon,quadwarswon
#general: longest streak w/out war,lengthofgame





def this_means_war(deck_one,deck_two,cards_one,cards_two,war_count):
        
    if len(deck_one) == 0 or len(deck_two) == 0:
        if len(deck_one) == 0 and len(deck_two) == 0:
            deck_two += cards_two
            deck_one += cards_one
        
        elif len(deck_one) == 0:
            deck_two += cards_two + cards_one + deck_one

        else: # if len(deck_two) == 0:
            deck_one += cards_one + cards_two + deck_two

            
    elif len(deck_two) <WL:
        war_one = deck_one[:WL]
        war_two = deck_two[:]

        del deck_one[:WL]
        del deck_two[:]
        
        if war_two[-1] > war_one[-1]:
            deck_two += cards_two + war_two + cards_one + war_one
        else:
            deck_one += cards_one + war_one + cards_two + war_two

    elif len(deck_one) <WL:
        war_one = deck_one[:]
        war_two = deck_two[:WL]

        del deck_one[:]
        del deck_two[:WL]
        
        if war_one[-1] > war_two[-1]:
            deck_one += cards_one + war_one + cards_two + war_two
        else:
            deck_two += cards_two + war_two + cards_one + war_one
            
    else:
        war_one = deck_one[:WL]
        war_two = deck_two[:WL]

        del deck_one[:WL]
        del deck_two[:WL]
        
        if war_one[-1] > war_two[-1]:
            deck_one += cards_one + war_one + cards_two + war_two
        elif war_two[-1] > war_one[-1]:
            deck_two += cards_two + war_two + cards_one + war_one
        
        else:
            cards_one += war_one
            cards_two += war_two
            war_count += 1
            
            [deck_one,deck_two,war_count] = this_means_war(deck_one,deck_two,cards_one,cards_two,war_count)
            
    return([deck_one,deck_two, war_count])


results = []
for game in range(0,num_games):
    deck = [i % suits for i in range(0,deck_size)]

    random.shuffle(deck)
    
    deck_one = deck[0:int(deck_size/2)]
    deck_two = deck[int(deck_size/2):deck_size]
    one_wins = 0
    two_wins = 0
    one_wars_won = [0,0,0,0,0,0,0,0]
    two_wars_won = [0,0,0,0,0,0,0,0]
    streak_wo_war = 0
    streak = 0
    one_fewest_cards = len(deck_one)
    two_fewest_cards = len(deck_two)
    wars = [0,0,0,0,0,0,0,0]
    one_aces = [sum(1 for i in deck_one if i == suits -1)]
    two_aces = [sum(1 for i in deck_two if i == suits -1)]
    one_kings = [sum(1 for i in deck_one if i == suits - 2)]
    two_kings = [sum(1 for i in deck_two if i == suits - 2)]
    one_value = [int(sum(i for i in deck_one))]
    two_value = [int(sum(i for i in deck_two))]
    
    
    for rounds in range(0,5000):
        
        #print('')
        #print([int(i % suits) for i in deck_one])
        #print([int(i % suits) for i in deck_two])
        

    
        one_fewest_cards = min(len(deck_one), one_fewest_cards)
        two_fewest_cards = min(len(deck_two), two_fewest_cards)
        
# =============================================================================
#         if one_fewest_cards == len(deck_one):
#             one_worst_deck = []
#             one_worst_deck = [int(i % suits) for i in deck_one]
#         if two_fewest_cards == len(deck_two):
#             two_worst_deck = []
#             two_worst_deck = [int(i % suits) for i in deck_two]
# =============================================================================

            
        streak_wo_war = max(streak_wo_war, streak)
        
        if len(deck_one) == 0 or len(deck_two) == 0:
           # print(rounds)
            break
        
        
        card_one = deck_one[0]
        card_two = deck_two[0]
        del deck_one[:1]
        del deck_two[:1]
        
        if card_one > card_two:
            deck_one += [card_one, card_two]
            
        elif card_two > card_one:
            deck_two += [card_two, card_one]
         
        else:
            #print('war')
            streak = -1
            war_count = 1
            one_deck_size = len(deck_one)
            two_deck_size = len(deck_two)
            [deck_one,deck_two,war_count] = this_means_war(deck_one,deck_two,[card_one], [card_two],war_count)
            
            if len(deck_one) > one_deck_size:
                one_wars_won[war_count -1] += 1
            if len(deck_two) > two_deck_size:
                two_wars_won[war_count -1] += 1
                
            wars[war_count-1] +=1
            
        streak += 1
        
        
    length = rounds
    
    if len(deck_one) == len(deck):
        one_wins += 1
        #print('team one wins!')
    elif len(deck_two) == len(deck):
        two_wins += 1
        #print('team two wins!')  
    else:
        print(len(deck_one),deck_one)
        print(len(deck_two),deck_two) 
    
    result = [one_wins] + one_value + one_aces+one_kings + [one_fewest_cards] + one_wars_won +\
            [two_wins] + two_value + two_aces+two_kings + [two_fewest_cards] + two_wars_won +\
            [streak_wo_war] + [length] + wars
    
    results.append(result)
        
results = np.array(results)


columns = ['one_wins', 'one_value', 'one_aces', 'one_kings', 'one_fewest_cards',\
           'one_wars1', 'one_wars2', 'one_wars3','one_wars4','one_wars5','one_wars6',\
           'one_wars7', 'one_wars8', 'two_wins' , 'two_value' , 'two_aces', 'two_kings',\
           'two_fewest_cards' , 'two_wars1', 'two_wars2', 'two_wars3','two_wars4',\
           'two_wars5','two_wars6','two_wars7', 'two_wars8', 'streak_wo_war', 'length',\
           'wars1', 'wars2', 'wars3','wars4','wars5','wars6','wars7', 'wars8']

results = pd.DataFrame(results, columns = columns)

print(time.time()-start)