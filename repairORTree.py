#repairORTree.py
#Function Purpose: The primary function is repairSchedule(), you can pass a reference schedule to it and repair it to produce a valid, complete schedule.
#                  If you want to generate a valid, complete schedule from scratch, just set "useInspiration" to False so that the tree executes as a normal OR tree. 

#python main.py test.txt 1 0 1 0 10 10 10 10

import copy
from constants import *
import schedule
import node
from queue import PriorityQueue

#Inputs: template schedule after parsing input, reference schedule if we are using one, Boolean for whether to use reference schedule, list of input-defined game slots, list of input-defined prac slots, all games, all pracs
#Outputs: None if a valid & complete schedule could not be produced, otherwise a valid & complete schedule is returned
#Purpose: takes in a reference schedule and repairs it to make it valid. This function can also be used to generate valid schedules to fill the population at the beginning
def repairSchedule(templateSchedule, inspirationSchedule, useInspiration, listValidGameSlots, listValidPracSlots, listAllGames, listAllPrac):
    #Create root node 
    rootNode = node.RepairNode()
    rootNode.setSchedule(templateSchedule)
    rootNode.setGamesLeft(listAllGames)
    rootNode.setPracLeft(listAllPrac)
    continueExpandingTree = True
    currentNode = rootNode

    counter = 0
  
    while (continueExpandingTree):
        #Define and call Altern
        print("Running round: ", counter)
        counter += 1
        currentNode.getSchedule().print()

        print("List from altern")
        listPossibleExpansions = altern(currentNode, listValidGameSlots, listValidPracSlots)
        
        printAlternGeneration(listPossibleExpansions)

        #Discuss edge case of there being no schedule to return with team, for now I am returning Python's version of Null
        if (listPossibleExpansions == []):
            return None

        #Define fleaf 
        print("reached fleaf")
        currentGameorPrac = ""
        #Find the current game/practice in discussion 
        if (len(currentNode.getGamesLeft())>0):
            gamesAvailable = currentNode.getGamesLeft()
            currentGameorPrac = gamesAvailable[0]

        elif (len(currentNode.getPracLeft())>0):
            pracAvailable = currentNode.getPracLeft()
            currentGameorPrac = pracAvailable[0]

        #Create Priority Queue 
        fringe =  PriorityQueue()
        for item in listPossibleExpansions:
            #if you want to generate a valid schedule without a reference, the useInspiration flag should be False
            if (useInspiration and follows(inspirationSchedule, currentNode, currentGameorPrac)):
                # Priority queue pulls items with lowest priority as most prioritized from the top
                # we add the nodeID as argument because we need to break ties for priorities in the queue (Python syntax)
                fringe.put(((item.getDepth()*2)-1, item.getID(), item))
            else: 
                fringe.put(((item.getDepth()*2), item.getID(), item))

        #Loop is useful to come back to pre-populated fringe when the node selected has an invalid schedule 
        while(True): 
            # the queue returns a tuple
            # format: (priority #, nodeID, node)

            #if all fringe schedules have been checked, then there is no valid schedule that can be produced
            if (fringe.empty()==True):
                return None
            
            checkTuple = fringe.get()
            checkNode = checkTuple[2]

            print("reached ftrans")
            #Get Node from fleaf and Pass to ftrans
            output = ftrans(checkNode)
            print("the ftrans output is ", output)
            if (output == 1):
                #the schedule is complete and meets all hard constraints - DONE
                return checkNode.getSchedule()
            elif (output == 2):
                #the schedule is invalid and we need a new node from the fringe
                continue 
            elif (output == 3):
                #the schedule is valid but incomplete and we pass this node to altern again 
                currentNode = checkNode
                break 


#Inputs: The current node in the OR tree, of type RepairNode
#Outputs: List of possible expansions of the current node's schedule 
#Purpose: Provides a list of options for expansion to fleaf, fleaf takes the output of this function and prioritizes options before proceeding
def altern(currentNode, listValidGameSlots, listValidPracSlots):
    currentSched = currentNode.getSchedule()
    originalGamesLeft = currentNode.getGamesLeft()
    originalPracLeft = currentNode.getPracLeft()

    listOfSchedules = []

    if (len(originalGamesLeft) > 0):
        #Loop through every possible timeslot in schedule 
        for day in range(schedule.numDays):
            for time in range(schedule.numTimeslots):
                if ((day, time) in listValidGameSlots):
                    copySchedule = currentSched.newSchedule()
                    myGamesLeft = originalGamesLeft.copy()
                    print("trying to add game to day/time ", day, time)
                    success = copySchedule.addGame(day, time, myGamesLeft[0])
                    print(success)

                    if success:
                        myGamesLeft.remove(myGamesLeft[0])

                        copyNode = currentNode.newNode()
                        copyNode.setSchedule(copySchedule)
                        copyNode.setGamesLeft(myGamesLeft)
                        copyNode.setDepth(currentNode.getDepth() + 1)
                        #This is done because creating a copy of the current node also duplicates the ID
                        copyNode.setUniqueID()
                        listOfSchedules.append(copyNode)
                    
                    #if adding the game to the schedule fails for some technical reason (possibilities defined in schedule.py),
                    #then we just continue looping through remaining time slots and ignore this one 
    elif (len(originalPracLeft) > 0):
        #Loop through every possible timeslot in schedule 
        for day in range(schedule.numDays):
            for time in range(schedule.numTimeslots):
                if ((day, time) in listValidPracSlots):
                    copySchedule = currentSched.newSchedule()
                    myPracLeft = originalPracLeft.copy()
                    print("trying to add practice to day/time ", day, time)
                    success = copySchedule.addPractice(day, time, myPracLeft[0])

                    if success:
                        myPracLeft.remove(myPracLeft[0])

                        copyNode = currentNode.newNode()
                        copyNode.setSchedule(copySchedule)
                        copyNode.setPracLeft(myPracLeft)
                        copyNode.setDepth(currentNode.getDepth() + 1)
                        #This is done because creating a copy of the current node also duplicates the ID
                        copyNode.setUniqueID()
                        listOfSchedules.append(copyNode)
                    
                    #if adding the practice to the schedule fails for some technical reason (possibilities defined in schedule.py),
                    #then we just continue looping through remaining time slots and ignore this one

    else:
        return []

    return listOfSchedules
  
#Used to debug altern and print content of list
def printAlternGeneration(listSchedules):
    counter = 0
    for node in listSchedules:
        print("Alternative ", counter)
        counter += 1 
        node.getSchedule().print()

#Inputs: reference schedule, current node from altern list, the game/practice we are finding in both schedules 
#Outputs: True if both schedules place the game/practice in the same slot, False otherwise 
#Purpose: Supports prioritization method in fleaf for repair functionality of OR Tree 
def follows(inspirationSchedule, currentNode, currentGameorPrac):
    inspDay = -1
    inspTime = -1

    #1 - Find the day and time at which the inspiration schedule assigns this game or practice
    inspAssignment = inspirationSchedule.getAssignment()
    for slotting in inspAssignment:
        listAssign = slotting[0]
        if (listAssign[0] == currentGameorPrac):
            inspDay = listAssign[1]
            inspTime = listAssign[2]
            break
    
    if (inspDay < 0 or inspTime < 0):
        #the currentGameorPrac is not in the inspirationSchedule (this shouldn't happen, but just in case)
        return False

    #2 - Find this day/time slot in the currentNode's schedule and check if this game or practice is placed here
    currentAssignment = currentNode.getSchedule().getAssignment()
    for slotting in currentAssignment:
        listAssign = slotting[0]
        if (listAssign[1] == inspDay and listAssign[2] == inspTime):
            gameOrPrac = listAssign[0]
            #If yes, return True, otherwise return False because the two schedules placed this game or practice in different slots
            if (gameOrPrac == currentGameorPrac):
                return True 
            else:
                return False

#Inputs: Proposed node for expansion passed from fleaf 
#Outputs: Integer - (1) complete, valid solution found (2) some hard constraints violated (3) incomplete schedule that is valid so far
#Purpose: Supports expansion method in OR Tree 
def ftrans(checkNode):
    passesHardConstraints = False
    if (len(checkNode.getGamesLeft()) > 0):
        passesHardConstraints = constr(checkNode.getSchedule(), True, False, False)
    elif ((len(checkNode.getGamesLeft()) == 0) and (len(checkNode.getPracLeft()) > 0)):
        passesHardConstraints = constr(checkNode.getSchedule(), True, True, False)
    else:
        passesHardConstraints = constr(checkNode.getSchedule(), False, True, True)

    # We don't need to explicitly change the sol-entry because if it is no, the node is discarded because it was already pulled from fringe 
    # If the sol-entry should be yes, we return this schedule in repairSchedule() anyways 
    # The default sol-entry in a node is ? so we don't need to change if the node is passed to altern 
    if (passesHardConstraints and ((checkNode.getGamesLeft() == []) and (checkNode.getPracLeft() == []))):
        # Solution found 
        return 1
    elif (not passesHardConstraints):
        # Discard node
        return 2
    else:
        # Expand node 
        return 3

# THIS IS A SUPER BASIC IMPLEMENTATION OF CONSTR() TO TEST REPAIR TREE - THIS STILL NEEDS TO BE PROPERLY IMPLEMENTED BASED ON pg. 2 OF REPORT 
def constr(someSchedule, partialFlag, gamesDoneFlag, pracDoneFlag):
    numDays = 5
    numTimeslots = 26

    print("checking constraints")

    if (partialFlag):
        #games allocated, practices left
        if (gamesDoneFlag):
            for day in range(numDays): #Days in week
                for time in range(numTimeslots): #Timeslots at half-hour intervals from 8:00-20:30
                    scheduleList = someSchedule.getSchedule()
                    someTimeSlot = scheduleList[day][time]
                    if ((len(someTimeSlot.getGames()) >= someTimeSlot.getGameMin()) and (len(someTimeSlot.getGames()) <= someTimeSlot.getGameMax())):
                        if ((len(someTimeSlot.getPractices()) <= someTimeSlot.getPracMax())):
                            continue
                        else:
                            return False
                    else:
                        return False
        #games left, practices left
        else:
            for day in range(numDays): #Days in week
                for time in range(numTimeslots): #Timeslots at half-hour intervals from 8:00-20:30
                    scheduleList = someSchedule.getSchedule()
                    someTimeSlot = scheduleList[day][time]
                    if ((len(someTimeSlot.getGames()) <= someTimeSlot.getGameMax())):
                        if ((len(someTimeSlot.getPractices()) <= someTimeSlot.getPracMax())):
                            continue
                        else:
                            return False
                    else:
                        return False
    #games allocated, practices allocated 
    else:
        for day in range(numDays): #Days in week
                for time in range(numTimeslots): #Timeslots at half-hour intervals from 8:00-20:30
                    scheduleList = someSchedule.getSchedule()
                    someTimeSlot = scheduleList[day][time]
                    if ((len(someTimeSlot.getGames()) >= someTimeSlot.getGameMin()) and (len(someTimeSlot.getGames()) <= someTimeSlot.getGameMax())):
                        if ((len(someTimeSlot.getPractices()) >= someTimeSlot.getPracMin()) and (len(someTimeSlot.getPractices()) <= someTimeSlot.getPracMax())):
                            continue
                        else:
                            return False
                    else:
                        return False

    return True
                

