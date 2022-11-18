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
    
    inputFile.close()

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

parse(file)
