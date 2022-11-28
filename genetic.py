#genetic.py

import sys
import copy
import schedule
import node
from repairORTree import *
from constants import *

state = []

'''


'''

# sortState()
# sort all the individuals in order of their eval-score
def sortState():


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
def fSelect():
    # random generation



    # mutation/crossover



    # deletion



def runGeneticAlgorithm():

    # start with an empty state, declared at the top of the file

