#genetic.py

'''
import sys
import copy
import schedule
import node
from repairORTree import *
from constants import *
'''
import random

# state contains two objects for each individual: the schedule and its eval-score
state = []

'''
to do:
start state DONE
define fwert DONE
define fselect
'''


# sortState()
# sort all the individuals in order of their eval-score
def sortState():
    global state
    state = sorted(state, key=lambda st : st[1], reverse=True)

# fWert()
# returns an integer 0 for random generation, 1 for mutation/crossover, 2 for deletion
def fWert():
    if len(state) < 5:
        return 0
    elif len(state) < 50:
        return 1
    else:
        return 2


# fSelect()
# performs random generation, mutation/crossover, or deletion
def fSelect(fWertScore):
    # random generation
    if fWertScore == 0:
        return

    # mutation/crossover
    elif fWertScore == 1:
        # 40% chance of mutation, 60% chance of crossover
        if (random.randint(0,100) < 40):
            # mutation
            sortState()
            return
        else:
            # crossover
            sortState()
            return


    # deletion
    elif fWertScore == 2:
        sortState()
        return


def runGeneticAlgorithm():

    # start with an empty state, declared at the top of the file
    state.append(('five', 5))
    state.append(('too', 2))
    state.append(('ate', 8))
    state.append(('nine', 9))

    
    for i in range(len(state)):
        print(state[i][0] + str(state[i][1]))
    
runGeneticAlgorithm()
