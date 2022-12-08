#genetic.py


import sys
import copy
import schedule
import node
from repairORTree import *
import constants
import evalFunction
import random

import constrFunction

# state contains two objects for each individual: the schedule and its eval-score
state = []


# sortState()
# sort all the individuals in order of their eval-score
def sortState():
    global state
    state = sorted(state, key=lambda s : s[1], reverse=True)

# rouletteSelect()
# takes a list of individuals and returns the one selected by a roulette function
def rouletteSelect(stateList):
    index = random.randint(1, 4)
    sorted(stateList, key=lambda s : s[1])
    print("\nstateList:")
    print(str(stateList))
    print("\n")
    return stateList[len(stateList)-index]

# find which timeslot a schedule contains a game or practice
def findTimeslot(sch, gameprac):
    for assign in sch.getAssignment():
        if assign[0] == gameprac:
            return assign[1], assign[2]
            break
    return -1, -1

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

        newSch = sched.newSchedule()
        for game in gamesList:
            slotNum = random.randint(0, len(validGameSlots)-1)
            slot = validGameSlots[slotNum]
            worked = newSch.addGame(int(slot[0]), int(slot[1]), game, validGameSlots)
            while (not worked):
                slotNum = random.randint(0, len(validGameSlots)-1)
                slot = validGameSlots[slotNum]
                worked = newSch.addGame(int(slot[0]), int(slot[1]), game, validGameSlots)

        for prac in pracList:
            slotNum = random.randint(0, len(validPracSlots)-1)
            slot = validPracSlots[slotNum]
            worked = newSch.addPractice(int(slot[0]), int(slot[1]), prac, validPracSlots)
            while (not worked):
                slotNum = random.randint(0, len(validPracSlots)-1)
                slot = validPracSlots[slotNum]
                worked = newSch.addPractice(int(slot[0]), int(slot[1]), prac, validPracSlots)

        randSchedule = repairSchedule(sched, newSch, True, validGameSlots, validPracSlots, gamesList, pracList)
        state.append((randSchedule, evalFunction.eval(randSchedule)))
        print("randomized eval: "+str(state[len(state)-1][1]))



    # mutation/crossover
    elif fWertScore == 1:
        # 40% chance of mutation, 60% chance of crossover
        if (random.randint(0,100) < 40):
            print("mutating")
            # mutation
            sortState()
            indA = rouletteSelect(state)
            mutant = sched.newSchedule()

            uGames = copy.copy(unassignedGames)
            uPracs = copy.copy(unassignedPracs)

            numGames = len(uGames)//10 + 1
            numPracs = len(uPracs)//10 + 1

            # randomize 10% of the games
            for i in range(numGames):
                # choose a random game to assign
                randIndex = random.randint(0, len(uGames)-1)
                game = uGames[randIndex]
                uGames.remove(game)
                worked = False
                # Try adding the game -> if it can't be added to the random slot, try again
                while worked == False:
                    slot = random.randint(0, len(validGameSlots)-1)
                    day, time = validGameSlots[slot]
                    worked = mutant.addGame(day, time, game, validGameSlots)

            # randomize 10% of the practices
            for i in range(numPracs):
                # choose a random practice to assign
                randIndex = random.randint(0, len(uPracs)-1)
                prac = uPracs[randIndex]
                uPracs.remove(prac)
                worked = False
                # Try adding the practice -> if it can't be added to the random slot, try again
                while worked == False:
                    slot = random.randint(0, len(validPracSlots)-1)
                    day, time = validPracSlots[slot]
                    worked = mutant.addPractice(day, time, prac, validPracSlots)

            # for the rest of the games, follow parent
            for game in uGames:
                # follow parent schedule
                day, time = findTimeslot(indA[0], game)
                if (day != -1 and time != -1):
                    mutant.addGame(day, time, game, validGameSlots)
                else:
                    sys.exit("Parent had no game assigned")

            # for the rest of the practices, follow parent
            for prac in uPracs:
                # follow parent schedule
                day, time = findTimeslot(indA[0], prac)
                if (day != -1 and time != -1):
                    mutant.addPractice(day, time, prac, validPracSlots)
                else:
                    sys.exit("Parent had no practice assigned")
            
            newIndividual = repairSchedule(sched, mutant, True, validGameSlots, validPracSlots, gamesList, pracList)
            state.append((newIndividual, evalFunction.eval(newIndividual)))
            print("mutated eval: "+str(state[len(state)-1][1]))

        else:
            print("crossovering")
            # crossover
            sortState()
            indA = rouletteSelect(state)
            print("indA: "+str(indA))
            sortState()
            temp = copy.copy(state)
            temp.remove(indA)
            indB = rouletteSelect(temp)
            print("indB: "+str(indB))

            child = sched.newSchedule()

            for i in range(len(unassignedGames)):
                game = unassignedGames[i]
                # even games are indA
                if i % 2 == 0:
                    day, time = findTimeslot(indA[0], game)
                    if (day != -1 and time != -1):
                        child.addGame(day, time, game, validGameSlots)
                    else:
                        day, time = findTimeslot(indB[0], game)
                        child.addGame(day, time, game, validGameSlots)
                        if (day != -1 and time != -1):
                            return
                # odd games are indB
                elif i % 2 == 1:
                    day, time = findTimeslot(indB[0], game)
                    if (day != -1 and time != -1):
                        child.addGame(day, time, game, validGameSlots)
                    else:
                        day, time = findTimeslot(indA[0], game)
                        child.addGame(day, time, game, validGameSlots)
                        if (day != -1 and time != -1):
                            return
            
            for i in range(len(unassignedPracs)):
                prac = unassignedPracs[i]
                # even pracs are indA
                if i % 2 == 0:
                    day, time = findTimeslot(indA[0], prac)
                    if (day != -1 and time != -1):
                        child.addPractice(day, time, prac, validPracSlots)
                    else:
                        day, time = findTimeslot(indB[0], prac)
                        child.addPractice(day, time, prac, validPracSlots)
                        if (day != -1 and time != -1):
                            return
                # odd pracs are indB
                elif i % 2 == 1:
                    day, time = findTimeslot(indB[0], prac)
                    if (day != -1 and time != -1):
                        child.addPractice(day, time, prac, validPracSlots)
                    else:
                        day, time = findTimeslot(indA[0], prac)
                        child.addPractice(day, time, prac, validPracSlots)
                        if (day != -1 and time != -1):
                            return
            newIndividual = repairSchedule(sched, child, True, validGameSlots, validPracSlots, gamesList, pracList)
            state.append((newIndividual, evalFunction.eval(newIndividual)))
            print("crossovered eval: "+str(state[len(state)-1][1]))

    # delete bottom 5 
    elif fWertScore == 2:
        sortState()
        state = state[5:]

    return


def runGeneticAlgorithm(s, vG, vP, g, p, pa):

    global sched
    global validGameSlots 
    global validPracSlots 
    global gamesList
    global pracList
    global partAssign
    sched = s
    validGameSlots = vG
    validPracSlots = vP
    gamesList = g
    pracList = p
    partAssign = pa

    # create a list of games and practices that are not automatically assigned
    global unassignedGames
    global unassignedPracs
    unassignedGames = copy.copy(gamesList)
    unassignedPracs = copy.copy(pracList)

    # start with an empty state, declared at the top of the file

    random.seed()
    sortState()
    
    for i in range(100):
        fw = fWert()
        # note: fSelect also updates state
        fSelect(fw)
    
    sortState()
    print("Final eval: "+str(state[len(state)-1][1]))

    '''
    for i in range(len(state)):
        print("eval state "+str(i) + " " + str(state[i][1]))
    '''

