#repairORTree.py
#Function Purpose: The primary function in this file is repairSchedule(), you can pass a reference schedule to it and repair it to produce a valid, complete schedule.
#                  If you want to generate a valid, complete schedule from scratch, just set "useInspiration" to False so that the tree executes as a normal OR tree. 

import copy
from constants import *
import schedule
import node
from queue import PriorityQueue
import sys
import constrFunction


#Inputs: template schedule after parsing input, reference schedule if we are using one, Boolean for whether to use reference schedule, list of input-defined game slots, list of input-defined prac slots, all games, all pracs
#Outputs: None if a valid & complete schedule could not be produced, otherwise a valid & complete schedule is returned
#Purpose: takes in a reference schedule and repairs it to make it valid. This function can also be used to generate valid schedules to fill the population at the beginning.
def repairSchedule(templateSchedule, inspirationSchedule, useInspiration, listValidGameSlots, listValidPracSlots, listAllGames, listAllPrac, iteration):
    #Create root node 
    rootNode = node.RepairNode()
    rootNode.setSchedule(templateSchedule)
    rootNode.setGamesLeft(listAllGames)
    rootNode.setPracLeft(listAllPrac)
    continueExpandingTree = True
    currentNode = rootNode

    counter = 0
    fringe =  PriorityQueue()


    while (continueExpandingTree):
        #Define and call Altern

        counter += 1
        #currentNode.getSchedule().printSchedule()

        listPossibleExpansions = altern(currentNode, listValidGameSlots, listValidPracSlots)
        
        #Uncomment this for debugging 
        #print("List from altern")
        #printAlternGeneration(listPossibleExpansions)

        #Discuss edge case of there being no schedule to return with team, for now I am returning Python's version of Null
        #What behaviour should be exhibited for inputs that cannot create a valid schedule?

        
        #If altern returns an empty list, that doesn't mean a valid schedule can't be produced. It just means
        #we need to try a different branch. It's only if the fringe is empty that a schedule can't be produced.

        if (listPossibleExpansions == []):
            #sys.exit("A valid schedule can not be produced.")
            return None
        
        #Define fleaf - no separate function, it's just defined inside repairSchedule()
        #print("Reached fleaf")

        currentGameorPrac = ""
        #Find the current game/practice in discussion 
        if (len(currentNode.getGamesLeft())>0):
            gamesAvailable = currentNode.getGamesLeft()
            currentGameorPrac = gamesAvailable[0]

        elif (len(currentNode.getPracLeft())>0):
            pracAvailable = currentNode.getPracLeft()
            currentGameorPrac = pracAvailable[0]


        c = 1
        # Add expanded nodes to Priority Queue 
        for item in listPossibleExpansions:
            #if you want to generate a valid schedule without a reference, the useInspiration flag should be False
            if (useInspiration and follows(inspirationSchedule, item, currentGameorPrac)):
                # Priority queue pulls items with lowest number as most prioritized from the top, so we subtract 1 for higher priority 
                # (Note - this is not consistent with Proposal description)
                # We add the nodeID as argument because we need to break ties for priorities in the queue (Python syntax)
                fringe.put(((item.getDepth()*2)-1, item.getID(), item))
            elif (c == iteration):
                fringe.put(((item.getDepth()*2), item.getID(), item))
                c+=1
            else:
                fringe.put(((item.getDepth()*2+c), item.getID(), item))
                c+=1

        #Loop is useful to come back to pre-populated fringe when the node selected has an invalid schedule 
        while(True): 
            # the queue returns a tuple
            # format: (priority #, nodeID, node)

            #if all fringe schedules have been checked, then there is no valid schedule that can be produced
            if (fringe.empty()==True):
                #sys.exit("A valid schedule cannot be produced.")
                return None

            checkTuple = fringe.get()
            checkNode = checkTuple[2]

            #print("Reached ftrans")
            #Get Node from fleaf and Pass to ftrans
            output = ftrans(checkNode)

            #Used for debugging
            #print("the ftrans output is ", output)
            #print("fringe size is "+str(fringe.qsize()))

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
        for (day, time) in listValidGameSlots:
            copySchedule = currentSched.newSchedule()
            myGamesLeft = originalGamesLeft.copy()
            #print("trying to add game to day/time ", day, time)
            success = copySchedule.addGame(day, time, myGamesLeft[0])
            #print(success)

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
        for (day, time) in listValidPracSlots:
            copySchedule = currentSched.newSchedule()
            myPracLeft = originalPracLeft.copy()
            #print("trying to add practice to day/time ", day, time)
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



#Used to debug Altern
def printAlternGeneration(listSchedules):
    counter = 0
    for node in listSchedules:
        print("Alternative ", counter)
        counter += 1 
        node.getSchedule().printSchedule()


#Inputs: reference schedule, current node from altern list, the game/practice we are finding in both schedules 
#Outputs: True if both schedules place the game/practice in the same slot, False otherwise 
#Purpose: Supports prioritization method in fleaf for repair functionality of OR Tree 
#Example: if you use s1 from main.py (run it on test2.txt) as the inspiration schedule and push it through this algo, you get the following assignment
#   Original: [('CMSA U12T1 DIV 01', 0, 2), ('CMSA U12T1 DIV 01 PRC 01', 1, 12), ('CMSA U12T1 DIV 01 PRC 02', 1, 18), ('CMSA U8T1 DIV 01', 0, 2), ('CMSA U8T1 DIV 01 PRC 01', 0, 2), ('CMSA U8T1 DIV 01 PRC 02', 0, 2)]
#   Repaired: [('CMSA U12T1 DIV 01', 1, 12), ('CMSA U12T1 DIV 01 PRC 01', 1, 12), ('CMSA U12T1 DIV 01 PRC 02', 1, 18), ('CMSA U8T1 DIV 01', 0, 2), ('CMSA U8T1 DIV 01 PRC 01', 0, 2), ('CMSA U8T1 DIV 01 PRC 02', 0, 2)]
def follows(inspirationSchedule, currentNode, currentGameorPrac):
    inspDay = -1
    inspTime = -1

    #1 - Find the day and time at which the inspiration schedule assigns this game or practice
    inspAssignment = inspirationSchedule.getAssignment()
    for slotting in inspAssignment:
        if (slotting[0] == currentGameorPrac):
            inspDay = slotting[1]
            inspTime = slotting[2]
            break
    
    if (inspDay < 0 or inspTime < 0):
        #the currentGameorPrac is not in the inspirationSchedule (this shouldn't happen, but just in case)
        return False

    #2 - Find this day/time slot in the currentNode's schedule and check if this game or practice is placed here
    currentAssignment = currentNode.getSchedule().getAssignment()

    for slotting in currentAssignment:
        if (slotting[1] == inspDay and slotting[2] == inspTime):
            gameOrPrac = slotting[0]
            #If yes, return True, otherwise return False because the two schedules placed this game or practice in different slots
            if (gameOrPrac == currentGameorPrac):
                return True 
            else:
                #Need to loop through all allocations for that timeslot and check
                continue
    return False 


#Inputs: Proposed node for expansion passed from fleaf 
#Outputs: Integer - (1) it's a complete, valid solution (2) some hard constraints violated (3) incomplete schedule that is valid so far
#Purpose: Supports expansion method in OR Tree 
def ftrans(checkNode):
    passesHardConstraints = constrFunction.constr(checkNode.getSchedule())
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
