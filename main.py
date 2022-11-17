#main.py
import schedule

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


