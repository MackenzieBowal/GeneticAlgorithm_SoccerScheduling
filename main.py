#main.py

import sys
import schedule
from constants import *

def parse(file):
    try: inputFile = open(file, 'r')
    except: sys.exit("The first command line argument must be a text file.")
    
    fileContent = inputFile.read()
    fileContent = fileContent.splitlines()
    print(fileContent)
    
    for i in range(len(fileContent)):
        fileContent[i] = fileContent[i].strip()
    
    print(fileContent)
    
    inputFile.close()
    
    category = "";
    for line in fileContent:
        if not (line == ''):
            #Tried using match case notation here but it would only work with python 3.10, check if lab computers have python 3.10 installed
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
                gameMin = int(components[3])
                print(day, time, gameMax, gameMin)
                p1.setGamemax(day, time, gameMax)
                p1.setGamemin(day, time, gameMin)
                #Note: changed notation in setGamemax and setPracticemax in schedule.py to accomodate strings as inputs rather than integers
            
            elif category == "PS":
                temp = line.replace(' ', '')
                components = temp.split(",")
                day = days[components[0]]
                time = times[components[1]]
                pracMax = int(components[2])
                pracMin = int(components[3])
                print(day, time, pracMax, pracMin)
                p1.setPracticemax(day, time, pracMax)
                p1.setPracticemin(day, time, pracMin)
            
            elif category == "G":
                gamesList.append(line)
            
            elif category == "P":
                pracList.append(line)
            
            elif category == "NC":
                components = line.split(",")
                comp1 = components[0].strip()
                comp2 = components[1].strip()
                notCompatible.append(tuple([comp1, comp2]))

#creates an empty schedule
p1 = schedule.Schedule()

p1.setGamemax(days['MO'],times['8:00'],1)
p1.setPracticemax(days['TU'],times['9:30'],2)
p1.setGamemax(days['MO'],times['9:00'],1)
p1.setPracticemax(days['MO'],times['10:00'],1)
p1.setPracticemax(days['FR'],times['15:00'],1)

#add games and practices to schedule
#format: addGame(day of the week, timeslot index, name of game)
#		 addpractice(day of the week, timeslot index, name of practice)
p1.addGame(days['MO'],times['8:00'],'G2')
p1.addPractice(days['TU'],times['9:30'],'P2')
p1.addGame(days['MO'],times['9:00'],'G1')
p1.addPractice(days['TU'],times['9:30'],'P3')
p1.addPractice(days['MO'],times['10:00'],'P4')
p1.addPractice(days['FR'],times['15:00'],'P1')

#prints the schedule
p1.print()

#read the input text file from the command line
try: file = sys.argv[1]
except: sys.exit("Must provide a program description in a text file.")

gamesList = []
pracList = []
notCompatible = []

parse(file)

print(gamesList)
print(pracList)
print(notCompatible)
