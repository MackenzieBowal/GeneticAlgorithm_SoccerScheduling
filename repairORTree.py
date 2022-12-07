#repairORTree.py
#Function Purpose: The primary function in this file is repairSchedule(), you can pass a reference schedule to it and repair it to produce a valid, complete schedule.
#                  If you want to generate a valid, complete schedule from scratch, just set "useInspiration" to False so that the tree executes as a normal OR tree. 

import copy
from constants import *
import schedule
import node
from queue import PriorityQueue
import sys


#Inputs: template schedule after parsing input, reference schedule if we are using one, Boolean for whether to use reference schedule, list of input-defined game slots, list of input-defined prac slots, all games, all pracs
#Outputs: None if a valid & complete schedule could not be produced, otherwise a valid & complete schedule is returned
#Purpose: takes in a reference schedule and repairs it to make it valid. This function can also be used to generate valid schedules to fill the population at the beginning.
def repairSchedule(templateSchedule, inspirationSchedule, useInspiration, listValidGameSlots, listValidPracSlots, listAllGames, listAllPrac, constrBundle):
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

        print("Running Altern round: ", counter)
        counter += 1
        currentNode.getSchedule().printSchedule()

        listPossibleExpansions = altern(currentNode, listValidGameSlots, listValidPracSlots)
        
        #Uncomment this for debugging 
        #print("List from altern")
        #printAlternGeneration(listPossibleExpansions)

        #Discuss edge case of there being no schedule to return with team, for now I am returning Python's version of Null
        #What behaviour should be exhibited for inputs that cannot create a valid schedule?
        if (listPossibleExpansions == []):
            #sys.exit("A valid schedule can not be produced.")
            return None

        #Define fleaf - no separate function, it's just defined inside repairSchedule()
        print("Reached fleaf")

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
            if (useInspiration and follows(inspirationSchedule, item, currentGameorPrac)):
                # Priority queue pulls items with lowest priority as most prioritized from the top, so we subtract 1 for higher priority (Note - this is not consistent with Proposal description)
                # We add the nodeID as argument because we need to break ties for priorities in the queue (Python syntax)
                fringe.put(((item.getDepth()*2)-1, item.getID(), item))
            else: 
                fringe.put(((item.getDepth()*2), item.getID(), item))

        #Loop is useful to come back to pre-populated fringe when the node selected has an invalid schedule 
        while(True): 
            # the queue returns a tuple
            # format: (priority #, nodeID, node)

            #if all fringe schedules have been checked, then there is no valid schedule that can be produced
            if (fringe.empty()==True):
                #sys.exit("A valid schedule can not be produced.")
                return None

            checkTuple = fringe.get()
            checkNode = checkTuple[2]

            print("Reached ftrans")
            #Get Node from fleaf and Pass to ftrans
            output = ftrans(checkNode, constrBundle)

            #Used for debugging
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
        for day in range(schedule.numDays):
            for time in range(schedule.numTimeslots):
                if ((day, time) in listValidPracSlots):
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
#Outputs: Integer - (1) complete, valid solution found (2) some hard constraints violated (3) incomplete schedule that is valid so far
#Purpose: Supports expansion method in OR Tree 
def ftrans(checkNode, constrBundle):
    passesHardConstraints = False
    if (len(checkNode.getGamesLeft()) > 0):
        passesHardConstraints = constr(checkNode.getSchedule(), True, False, False, constrBundle)
    elif ((len(checkNode.getGamesLeft()) == 0) and (len(checkNode.getPracLeft()) > 0)):
        passesHardConstraints = constr(checkNode.getSchedule(), True, True, False, constrBundle)
    else:
        passesHardConstraints = constr(checkNode.getSchedule(), False, True, True, constrBundle)

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

def check_hc1(someSchedule, partAssign):
    sched = someSchedule.getSchedule()
    for assign in partAssign:
        league_tier_div = assign[0]
        day = assign[1]
        time = assign[2]
        games_list = sched[days[day]][times[time]].getGames()
        if(league_tier_div not in games_list):
            return False
    
    return True


#Checks to make sure there are no practices for CSMA U12T1S and CSMA U13T1S between 6 and 7 on
#Tuesdays and Thursdays
#Should be true for partial schedules. 

def check_hc2(someSchedule):
    sched = someSchedule.getSchedule()
    prac_at_six = sched[days["TU"]][20].getPractices()
    for prac in prac_at_six:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False
    
    prac_at_six_thirty = sched[days["TU"]][20].getPractices()
    for prac in prac_at_six_thirty:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False

    prac_at_six = sched[days["TH"]][20].getPractices()
    for prac in prac_at_six:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False

    prac_at_six_thirty = sched[days["TH"]][20].getPractices()
    for prac in prac_at_six_thirty:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False

    return True

    

#Checks to see if there are ever more games assigned then game max. 
#Should always be satisfied, even in partial schedules. 

def check_hc3(someSchedule):
    for day in someSchedule.getSchedule():
        for timeslot in day:
            if(len(timeslot.getGames()) > timeslot.getGameMax()):
                return False
    return True


#Checks to see if there are ever more practices than practice max. 
#Should always be satisifed, even in partial schedules. 



def check_hc4(someSchedule):
    for day in someSchedule.getSchedule():
        for timeslot in day:
            if(len(timeslot.getPractices()) > timeslot.getPracMax()):
                return False
    return True


def check_hc5(someSchedule):
    for day in someSchedule.getSchedule():
        for timeslot in day:
            for game in timeslot.getGames():
                if(game in timeslot.getPractices()):
                    return False
    return True


def check_hc6(someSchedule, uncompatible):
    for a, b in uncompatible:
        for day in someSchedule.getSchedule():
            for timeslot in day:
                if((a in timeslot.getGames() or a in timeslot.getPractices()) and (b in timeslot.getGames() or b in timeslot.getPractices())):
                    return False
    return True


#Checks to see that all monday wednesday friday games are scheduled for the same time. 
#Some partially complete schedules may not follow this check. 
def check_hc7(someSchedule):
   for i in range(len(someSchedule.getSchedule()[days["MO"]])):
        mon_games = someSchedule.getSchedule()[days["MO"]][i].getGames()
        wed_games = someSchedule.getSchedule()[days["WE"]][i].getGames()
        fri_games = someSchedule.getSchedule()[days["FR"]][i].getGames()
        if(len(mon_games) != len(wed_games) or len(mon_games) != len(fri_games)):
            return False
        for mon_game in mon_games:
            if(mon_game not in wed_games):
                return False
            if(mon_game not in fri_games):
                return False
   return True

#checks to see if Monday/Wednesday practices are at the same time
#may not pass on all partial scehdules

def check_hc8(someSchedule):
    for i in range(len(someSchedule.getSchedule()[days["MO"]])):
        mon_pracs = someSchedule.getSchedule()[days["MO"]][i].getPractices()
        wed_pracs = someSchedule.getSchedule()[days["WE"]][i].getPractices()
        if(len(mon_pracs) != len(wed_pracs)):
            return False
        
        for mon_prac in mon_pracs:
            if(mon_prac not in wed_pracs):
                return False
    
    return True
        

#checks to see if Tuesday/Thrusday games and practices are at the same time
#may not pass on all partial scehdules


def check_hc9(someSchedule):
    for i in range(len(someSchedule.getSchedule()[days["TU"]])):
        tues_games = someSchedule.getSchedule()[days["TU"]][i].getGames()
        thur_games = someSchedule.getSchedule()[days["TH"]][i].getGames()

        tues_pracs = someSchedule.getSchedule()[days["TU"]][i].getPractices()
        thur_pracs = someSchedule.getSchedule()[days["TH"]][i].getPractices()

        if(len(tues_games) != len(thur_games)):
            return False
        if(len(tues_pracs) != len(thur_pracs)):
            return False
        
        for tues_game in tues_games:
            if(tues_game not in thur_games):
                return False
        
        for tues_prac in tues_pracs:
            if tues_prac not in thur_pracs:
                return False
        
    return True





##Checks to make sure games in DIV 9 are not scheduled before 18:00
##should pass on all partial schedules. 

def check_hc10(someSchedule):
    for day in someSchedule.getSchedule():
        for time in range(times["18:00"]):
            for games in day[time].getGames():
                if(games.split()[3] == "09"):
                    return False
            for prac in day[time].getPractices():
                if(prac.split()[3] == "09"):
                    return False
    return True
    

#Checks to see if anything has been placed in an unwanted timeslot. 
# Should pass for partial schedules.     

def check_hc11(someSchedule, unwanted):
    for unwant_sched in unwanted:
        g = unwant_sched[0]
        day = unwant_sched[1]
        time = unwant_sched[2]
        for game in someSchedule.getSchedule()[days[day]][times[time]].getGames():
            if(game == g):
                return False
    
    return True
        


#Makes sure that games aren't hosted between 11:00 and 12:30 on Tuesdays and Thrusdays. 
#Should pass on all partial schedules. 

def check_hc12(someSchedule):
    sched = someSchedule.getSchedule()
    if(len(sched[days["TU"]][6].getGames()) != 0):
        return False
    if(len(sched[days["TU"]][7].getGames()) != 0):
        return False
    if(len(sched[days["TU"]][8].getGames()) != 0):
        return False
    if(len(sched[days["TH"]][6].getGames()) != 0):
        return False
    if(len(sched[days["TH"]][7].getGames()) != 0):
        return False
    if(len(sched[days["TH"]][8].getGames()) != 0):
        return False

    return True
    

#Checks to see if any games in the leagues U15, U16, U17 and U19 are in the same timeslot. 
#Should pass on all partial schedules. 
#DOUBLE CHECK TO MAKE SURE THIS MATCHES HARD CONSTRAINTS IN ASSIGN SPECS. 
def check_hc13(someSchedule):
    for day in someSchedule.getSchedule():
        for timeslot in day:
            one_game_found = False
            for game in timeslot.getGames():
                game_list = game.split()
                tier_div = game[1]
                if(tier_div[0:3] == "U15" or tier_div[0:3] == "U16" or tier_div[0:3] == "U17" or tier_div[0:3] == "U19"):
                    if(not one_game_found): 
                        one_game_found = True
                    else:
                        return False
    
    return True
                    

#Checks to make sure that no games in the tear div U12T1S is in the same gameslot. 
#Should pass all partial schedules. 

def check_hc14(someSchedule):
    for day in someSchedule.getSchedule():
        for timeslot in day:
            u12T1S = False
            for game in timeslot.getGames():
                tier_div = game[1]
                if(tier_div == "U12T1S"):
                    if(not u12T1S): 
                        u12T1S = True
                    else: 
                        return False
            for prac in timeslot.getPractices():
                tier_div = prac[1]
                if(tier_div == "U12T1S"):
                    if(not u12T1S): 
                        u12T1S = True
                    else: 
                        return False

    return True
                
#Checks to make sure that no games in the tear div U13T1S is in the same gameslot. 
#Should pass all partial schedules. 


def check_hc15(someSchedule):
    for day in someSchedule.getSchedule():
        for timeslot in day:
            u13T1S = False
            for game in timeslot.getGames():
                tier_div = game[1]
                if(tier_div == "U13T1S"):
                    if(not u13T1S): 
                        u13T1S = True
                    else: 
                        return False
                if(tier_div == "U13T1S"):
                    if(not u13T1S): 
                        u13T1S = True
                    else: 
                        return False
    return True
                


# THIS IS A SUPER BASIC IMPLEMENTATION OF CONSTR() TO TEST REPAIR TREE - THIS STILL NEEDS TO BE PROPERLY IMPLEMENTED BASED ON pg. 2 OF REPORT 
def constr(someSchedule, partialFlag, gamesDoneFlag, pracDoneFlag, constrBundle):
    if(not partialFlag):
       hc1 = check_hc1(someSchedule, constrBundle.partAssign)
       hc2 = check_hc2(someSchedule)
       hc3 = check_hc3(someSchedule)
       hc4 = check_hc4(someSchedule)
       hc5 = check_hc5(someSchedule)
       hc6 = check_hc6(someSchedule, constrBundle.notCompatible)
       hc7 = check_hc7(someSchedule)
       hc8 = check_hc8(someSchedule)
       hc9 = check_hc9(someSchedule)
       hc10 = check_hc10(someSchedule)
       hc11 = check_hc11(someSchedule, constrBundle.unwanted)
       hc12 = check_hc12(someSchedule)
       hc13 = check_hc13(someSchedule)
       hc14 = check_hc14(someSchedule)
       hc15 = check_hc15(someSchedule)

       return hc1 and hc2 and hc3 and hc4 and hc5 and hc6 and hc7 and hc8 \
           and hc9 and hc10 and hc11 and hc12 and hc13 and hc14 and hc15
    
    else:
        if(gamesDoneFlag):
            hc1 = check_hc1(someSchedule, constrBundle.partAssign)
            hc2 = check_hc2(someSchedule)
            hc3 = check_hc3(someSchedule)
            hc4 = check_hc4(someSchedule)
            hc5 = check_hc5(someSchedule)
            hc6 = check_hc6(someSchedule, constrBundle.notCompatible)
            hc7 = check_hc7(someSchedule)
            hc10 = check_hc10(someSchedule)
            hc11 = check_hc11(someSchedule, constrBundle.unwanted)
            hc12 = check_hc12(someSchedule)
            hc13 = check_hc13(someSchedule)
            hc14 = check_hc14(someSchedule)
            hc15 = check_hc15(someSchedule)

            return hc1 and hc2 and hc3 and hc4 and hc5  and hc6 and hc7 and \
            hc10 and hc11 and hc12 and hc13 and hc15
        
        elif(pracDoneFlag):
            hc1 = check_hc1(someSchedule, constrBundle.partAssign)
            hc2 = check_hc2(someSchedule)
            hc3 = check_hc3(someSchedule)
            hc4 = check_hc4(someSchedule)
            hc5 = check_hc5(someSchedule)
            hc6 = check_hc6(someSchedule, constrBundle.notCompatible)
            hc8 = check_hc8(someSchedule)
            hc10 = check_hc10(someSchedule)
            hc11 = check_hc11(someSchedule, constrBundle.unwanted)
            hc12 = check_hc12(someSchedule)
            hc13 = check_hc13(someSchedule)
            hc14 = check_hc14(someSchedule)
            hc15 = check_hc15(someSchedule)

            return  hc1 and hc2 and hc3 and hc4 and hc5 and hc8 and \
            hc10 and hc11 and hc12 and hc13 and hc14 and hc15
        else:
            hc1 = check_hc1(someSchedule, constrBundle.partAssign)
            hc2 = check_hc2(someSchedule)
            hc3 = check_hc3(someSchedule)
            hc4 = check_hc4(someSchedule)
            hc5 = check_hc5(someSchedule)
            hc6 = check_hc6(someSchedule, constrBundle.notCompatible)
            hc7 = check_hc7(someSchedule)
            hc10 = check_hc10(someSchedule)
            hc11 = check_hc11(someSchedule, constrBundle.unwanted)
            hc12 = check_hc12(someSchedule)
            hc13 = check_hc13(someSchedule)
            hc14 = check_hc14(someSchedule)
            hc15 = check_hc15(someSchedule)

            return hc1 and hc2 and hc3 and hc4 and hc5 and hc6 and \
            hc10 and hc11 and hc12 and hc13 and hc14 and hc15
