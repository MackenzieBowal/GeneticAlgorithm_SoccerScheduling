#main.py

import sys
import copy
import schedule
import node
from repairORTree import*
from constants import *
from genetic import runGeneticAlgorithm
import evalFunction

#Sample Cmd Line
#python main.py test.txt 1 0 1 0 10 10 10 10
#python main.py test2.txt 1 0 1 0 10 10 10 10


"""
parse()
Input: One text file
Returns: One soccer schedule with max/min game and practice values set for each time slot
            DO NOT MODIFY THIS SCHEDULE!
Also assigns any partial assignments and populates a list of games, a list of practices,
    and lists for all soft constraints
"""
def parse(file):
    try: inputFile = open(file, 'r')
    except: sys.exit("The first command line argument must be a text file.")
    
    fileContent = inputFile.read()
    fileContent = fileContent.splitlines()
    
    for i in range(len(fileContent)):
        fileContent[i] = fileContent[i].strip()
    
    inputFile.close()
    
    sched = schedule.Schedule()
    
    category = ""
    for line in fileContent:
        if not (line == ''):
            if(line == "Game slots:"):
                category = "GS"
                continue
            elif(line == "Practice slots:"):
                category = "PS"
                continue
            elif(line == "Games:"):
                category = "G"
                continue
            elif(line == "Practices:"):
                category = "P"
                continue
            elif(line == "Not compatible:"):
                category = "NC"
                continue
            elif(line == "Unwanted:"):
                category = "U"
                continue
            elif(line == "Preferences:"):
                category = "Pref"
                continue
            elif(line == "Pair:"):
                category = "Pair"
                continue
            elif(line == "Partial assignments:"):
                category = "PA"
                continue

            if category == "GS":
                temp = line.replace(' ', '')
                components = temp.split(",")
                day = days[components[0]]
                time = times[components[1]]
                gameMax = int(components[2])
                global numGameSpaces
                numGameSpaces += gameMax
                gameMin = int(components[3])
                sched.setGamemax(day, time, gameMax)
                sched.setGamemin(day, time, gameMin)
                validGameSlots.append((day, time))
            
            elif category == "PS":
                temp = line.replace(' ', '')
                components = temp.split(",")
                day = days[components[0]]
                time = times[components[1]]
                pracMax = int(components[2])
                global numPracSpaces
                numPracSpaces += pracMax
                pracMin = int(components[3])
                sched.setPracticemax(day, time, pracMax)
                sched.setPracticemin(day, time, pracMin)
                validPracSlots.append((day, time))
            
            elif category == "G":
                global numGamesTotal
                numGamesTotal+=1
                if ("CMSA U12T1" in line or "CMSA U13T1" in line):
                    global specialGamesExist
                    specialGamesExist = True
                    specialGamesList.append(line)
                gamesList.append(line)
            
            elif category == "P":
                global numPracsTotal
                numPracsTotal+=1
                if ("CMSA U12T1S" in line or "CMSA U13T1S" in line):
                    global specialPracsExist
                    specialPracsExist = True
                pracList.append(line)
            
            elif category == "NC":
                components = line.split(",")
                comp1 = components[0].strip()
                comp2 = components[1].strip()
                notCompatible.append(tuple([comp1, comp2]))
                
            elif category == "U":
                components = line.split(',')
                game = components[0].strip()
                day = components[1].strip()
                time = components[2].strip()
                unwanted.append(tuple([game, day, time]))
                
            elif category == "Pref":
                components = line.split(',')
                day = components[0].strip()
                time = components[1].strip()
                game = components[2].strip()
                value = int(components[3].strip())
                preferences.append(tuple([day, time, game, value]))
                
            elif category == "Pair":
                components = line.split(',')
                game1 = components[0].strip()
                game2 = components[1].strip()
                pair.append(tuple([game1, game2]))
                
            elif category == "PA":
                components = line.split(',')
                game = components[0].strip()
                day = components[1].strip()
                time = components[2].strip()
                if ("PRC" in game) or ("OPN" in game):
                    sched.addPractice(days[day], times[time], game, validPracSlots)
                    pracList.remove(game)
                else:
                    sched.addGame(days[day], times[time], game, validGameSlots)
                    gamesList.remove(game)
                partassign.append(tuple([game, day, time]))
    return sched


#define soft constraint weightings and penalty values
wMinFilled = sys.argv[2]
wPref = sys.argv[3]
wPair = sys.argv[4]
wSecDiff = sys.argv[5]
penGameMin = sys.argv[6]
penPracticeMin = sys.argv[7]
penNotPaired = sys.argv[8]
penSection = sys.argv[9]

#define lists to store input from the text file
validGameSlots = [] #contains tuples (day, time) for valid ones based on input file - day, time are ints from constants.py
validPracSlots = [] #contains tuples (day, time) for valid ones based on input file - day, time are ints from constants.py
gamesList = []
pracList = []
notCompatible = []
unwanted = []
preferences = []
pair = []
partassign = []

#for checking hard constraints
specialGamesExist = False
specialPracsExist = False
specialGamesList = []
numGamesTotal = 0
numPracsTotal = 0
numGameSpaces = 0
numPracSpaces = 0

# read the input text file from the command line
try: file = sys.argv[1]
except: sys.exit("Must provide a program description in a text file.")

sched = parse(file)

#Check for input validity
if (numGamesTotal > numGameSpaces):
    sys.exit("Too many games for the number of slots")
if (numPracsTotal > numPracSpaces):
    sys.exit("Too many practices for the number of slots")


# Automatically assign hard constraint practices
if (specialGamesExist):
    # U12T1S first
    for game in specialGamesList:
        if ("CMSA U12T1" in game):
            worked = sched.addPractice(days['TU'], times['18:00'], "CMSA U12T1S", validPracSlots)
            if (not worked):
                sys.exit("\nCould not allocate CMSA U12T1S to a valid practice slot\n") 
    for game in specialGamesList:
        if ("CMSA U13T1" in game):
            worked = sched.addPractice(days['TU'], times['18:00'], "CMSA U13T1S", validPracSlots)
            if (not worked):
                sys.exit("\nCould not allocate CMSA U13T1S to a valid practice slot\n") 


print("sched:")
print("Games:", gamesList)
print("Practices:", pracList)
print("Not compatible:", notCompatible)
print("Unwanted:", unwanted)
print("Preferences:", preferences)
print("Pair:", pair)
print("Partial assignments:", partassign)

evalFunction.initiateEval(wMinFilled, wPref, wPair, wSecDiff, penGameMin, penPracticeMin, preferences, penNotPaired, penSection, pair)
constrFunction.initiateConstr(gamesList, pracList, validGameSlots, validPracSlots, notCompatible, unwanted, preferences, pair, partassign)

runGeneticAlgorithm(sched, validGameSlots, validPracSlots, gamesList, pracList, partassign)
