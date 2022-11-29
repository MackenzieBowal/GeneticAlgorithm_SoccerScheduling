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
    state = sorted(state, key=lambda s : s[1], reverse=True)

# rouletteSelect()
# takes a list of individuals and returns the one selected by a roulette function
def rouletteSelect(stateList):
    totalEval = 0
    for i in range(len(stateList)):
        totalEval += stateList[i][1]
    
    fitnesses = []
    totalFitness = 0

    for j in range(len(stateList)):
        fitnesses.append(totalEval - stateList[j][1])
        totalFitness += fitnesses[j]
        print("individual "+stateList[j][0]+" "+str(stateList[j][1])+" has fitness "+str(fitnesses[j]))

    print(totalFitness)

    num = random.randint(0, totalFitness)
    index = 0

    while num > 0:
        print("num: "+str(num)+" index: "+str(index))
        num -= fitnesses[index]
        index += 1
    index -= 1

    return stateList[index]

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
    global state

    # random generation
    if fWertScore == 0:

        return

    # mutation/crossover
    elif fWertScore == 1:
        # 40% chance of mutation, 60% chance of crossover
        if (random.randint(0,100) < 40):
            # mutation
            sortState()
            indA = rouletteSelect(state)
            return
        else:
            # crossover
            sortState()
            indA = rouletteSelect(state)
            sortState()
            indB = rouletteSelect(state.remove(indA))


        return


    # delete bottom 5 
    elif fWertScore == 2:
        sortState()
        state = state[5:]
        return


def runGeneticAlgorithm():

    # start with an empty state, declared at the top of the file
    state.append(('five', 5))
    state.append(('too', 2))
    state.append(('ate', 8))
    state.append(('nine', 9))
    state.append(('six', 6))
    state.append(('won', 1))
    state.append(('fore', 4))
    state.append(('two', 2))
    state.append(('three', 3))

    sortState()

    for i in range(len(state)):
        print(state[i][0] + str(state[i][1]))

    fSelect(1)
    
    for i in range(len(state)):
        print(state[i][0] + str(state[i][1]))
    
runGeneticAlgorithm()
