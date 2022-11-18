#main.py
import schedule
import sys

def parse(file):
    try:
        inputFile = open(file, 'r')
    except:
        sys.exit("The first command line argument must be a text file.")
    
    fileContent = inputFile.readlines()
    print(fileContent)
    
    inputFile.close()

#creates an empty schedule
p1 = schedule.Schedule(5) #Note: 5 is a temp value, replace after writing parser

#add games and practices to schedule
#format: addGame(day of the week, timeslot index, name of game)
#		 addpractice(day of the week, timeslot index, name of practice)
p1.addGame(0,0,'G2')
p1.addPractice(1,3,'P2')
p1.addGame(4,2,'G1')
p1.addPractice(1,3,'P3')
p1.addPractice(4,4,'P4')

#prints the schedule
p1.print()

#read the input text file from the command line
try:
    file = sys.argv[1]
except:
    sys.exit("Must provide a program description in a text file.")

parse(file)
