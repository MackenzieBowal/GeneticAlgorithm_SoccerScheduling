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
        fitnesses.append((totalEval - stateList[j][1])*1000)
        totalFitness += fitnesses[j]
        print("individual "+str(j)+" "+str(stateList[j][1])+" has fitness "+str(fitnesses[j]))

    num = random.randint(0, totalFitness)
    index = 0

    while num > 0:
        print("num: "+str(num)+" index: "+str(index))
        num -= fitnesses[index]
        index += 1
    index -= 1

    return stateList[index]

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

        newSch = sched.newSchedule()
        #newSch.addPractice('CMSA U8T1 DIV 01 PRC 02', 1, 18)
        

        passed = constrFunction.check_hc2(newSch)

        if passed:
            print("passed constr")
        else:
            print("did not pass constr")

        return





        randSchedule = repairSchedule(sched, None, False, validGameSlots, validPracSlots, gamesList, pracList)
        '''
        while( randSchedule == None):
            print("Exception 1- no valid schedule found")
            randSchedule = repairSchedule(sched, None, False, validGameSlots, validPracSlots, gamesList, pracList)
        '''
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
        #if (random.randint(0,100) < 40):
        if (1 == 1):
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
                print("randomizing game "+game)
                worked = False
                # Try adding the game -> if it can't be added to the random slot, try again
                while worked == False:
                    slot = random.randint(0, len(validGameSlots)-1)
                    day, time = validGameSlots[slot]
                    worked = mutant.addGame(day, time, game)

            # randomize 10% of the practices
            for i in range(numPracs):
                # choose a random practice to assign
                randIndex = random.randint(0, len(uPracs)-1)
                prac = uPracs[randIndex]
                uPracs.remove(prac)
                print("randomizing prac "+prac)
                worked = False
                # Try adding the practice -> if it can't be added to the random slot, try again
                while worked == False:
                    slot = random.randint(0, len(validPracSlots)-1)
                    day, time = validPracSlots[slot]
                    worked = mutant.addPractice(day, time, prac)

            # for the rest of the games, follow parent
            for game in uGames:
                # follow parent schedule
                print("following parent for game "+game)
                day, time = findTimeslot(indA[0], game)
                if (day != -1 and time != -1):
                    mutant.addGame(day, time, game)
                else:
                    sys.exit("Parent had no game assigned")

            # for the rest of the practices, follow parent
            for prac in uPracs:
                # follow parent schedule
                print("following parent for prac "+prac)
                day, time = findTimeslot(indA[0], prac)
                if (day != -1 and time != -1):
                    mutant.addPractice(day, time, prac)
                else:
                    sys.exit("Parent had no prac assigned")
            
            print("\nMUTANT SCHEDULE:")
            mutant.printSchedule()

        else:
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
                print("assigning game "+game)
                # even games are indA
                if i % 2 == 0:
                    print("even game")
                    day, time = findTimeslot(indA[0], game)
                    print("adding to timeslot "+str(day)+", "+str(time))
                    if (day != -1 and time != -1):
                        child.addGame(day, time, game)
                    else:
                        day, time = findTimeslot(indB[0], game)
                        child.addGame(day, time, game)
                        if (day != -1 and time != -1):
                            return
                # odd games are indB
                elif i % 2 == 1:
                    print("odd game")
                    day, time = findTimeslot(indB[0], game)
                    print("adding to timeslot "+str(day)+", "+str(time))
                    if (day != -1 and time != -1):
                        child.addGame(day, time, game)
                    else:
                        day, time = findTimeslot(indA[0], game)
                        child.addGame(day, time, game)
                        if (day != -1 and time != -1):
                            return
            
            for i in range(len(unassignedPracs)):
                prac = unassignedPracs[i]
                # even pracs are indA
                if i % 2 == 0:
                    day, time = findTimeslot(indA[0], prac)
                    if (day != -1 and time != -1):
                        child.addPractice(day, time, prac)
                    else:
                        day, time = findTimeslot(indB[0], prac)
                        child.addPractice(day, time, prac)
                        if (day != -1 and time != -1):
                            return
                # odd pracs are indB
                elif i % 2 == 1:
                    day, time = findTimeslot(indB[0], prac)
                    child.addPractice(day, time, prac)
                    if (day != -1 and time != -1):
                        child.addPractice(day, time, prac)
                    else:
                        day, time = findTimeslot(indA[0], prac)
                        child.addPractice(day, time, prac)
                        if (day != -1 and time != -1):
                            return
            print("\nCHILD SCHEDULE: ")
            child.printSchedule()


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
    '''
    for gp in partAssign:
        if ("PRC" in gp[0] or "OPN" in gp[0]):
            unassignedPracs.remove(gp[0])
        else:
            print(unassignedGames)
            unassignedGames.remove(gp[0])
    '''

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
    random.seed()
    sortState()

    print("Running fSelect")
    fSelect(0)
    '''
    for i in range(5):
        fw = fWert()

        # note: fSelect also updates state
        fSelect(fw)
    
    sortState()

    for i in range(len(state)):
        print("eval state"+str(i) + " " + str(state[i][1]))

    fSelect(1)

    for i in range(len(state)):
        print("eval state "+str(i) + " " + str(state[i][1]))
    '''

