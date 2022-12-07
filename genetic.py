#genetic.py


import sys
import copy
import schedule
import node
from repairORTree import *
from constants import *
import evalFunction
import random

# state contains two objects for each individual: the schedule and its eval-score
state = []

'''
to do:
start state DONE
define fwert DONE
define fselect ALMOST DONE
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

    # first 5 are randomly generated
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

        '''
        newSch = sched.newSchedule()
        newSch.getSchedule()[0][1].gamemax = 2
        newSch.getSchedule()[2][1].gamemax = 2
        newSch.getSchedule()[4][1].gamemax = 2
        newSch.printSchedule()

        newSch.addGame(0, 1, 'CMSA U12T1 DIV 01')
        newSch.addGame(0, 1, 'CMSA U12T1 DIV 02')
        newSch.printSchedule()
        e = evalFunction.evalSecDiff(newSch)
        print("eval done: "+ str(e))
        '''
        randSchedule = repairSchedule(sched, None, False, validGameSlots, validPracSlots, gamesList, pracList, constrBundle)
        while( randSchedule == None):
            print("Exception 1- no valid schedule found")
            randSchedule = repairSchedule(sched, None, False, validGameSlots, validPracSlots, gamesList, pracList, constrBundle)

        #else:
            # add random schedule to state
        randSchedule.printSchedule()
        state.append((randSchedule, evalFunction.eval(randSchedule)))
        print("eval: "+str(state[0][1]))

        '''
        randSchedule.getSchedule()[0][2].games.clear()
        randSchedule.getSchedule()[0][2].practices.clear()

        print("evalMinFilled: "+str(evalFunction.evalMinFilled(randSchedule)))
        print("evalPref: "+str(evalFunction.evalPref(randSchedule)))
        print("evalPair: "+str(evalFunction.evalPair(randSchedule)))
        print("evalSecDiff: "+str(evalFunction.evalSecDiff(randSchedule)))

        print(str(evalFunction.eval(randSchedule)))
        '''


    # mutation/crossover
    elif fWertScore == 1:
        # 40% chance of mutation, 60% chance of crossover
        if (random.randint(0,100) < 40):
            # mutation
            sortState()
            indA = rouletteSelect(state)

        else:
            # crossover
            sortState()
            indA = rouletteSelect(state)
            sortState()
            indB = rouletteSelect(state.remove(indA))




    # delete bottom 5 
    elif fWertScore == 2:
        sortState()
        state = state[5:]

    return


def runGeneticAlgorithm(s, vG, vP, g, p, cb):

    global sched
    global validGameSlots 
    global validPracSlots 
    global gamesList
    global pracList
    global constrBundle
    sched = s
    validGameSlots = vG
    validPracSlots = vP
    gamesList = g
    pracList = p
    constrBundle = cb

    # start with an empty state, declared at the top of the file

    '''
    state.append(('five', 5))
    state.append(('too', 2))
    state.append(('ate', 8))
    state.append(('nine', 9))
    state.append(('six', 6))
    state.append(('won', 1))
    state.append(('fore', 4))
    state.append(('two', 2))
    state.append(('three', 3))
    '''

    sortState()

    for i in range(5):
        fw = fWert()

        # note: fSelect also updates state
        fSelect(fw)

    sortState()

    for i in range(len(state)):
        print("eval state"+str(i) + " " + str(state[i][1]))

    fSelect(2)

    for i in range(len(state)):
        print("eval state "+str(i) + " " + str(state[i][1]))

    
