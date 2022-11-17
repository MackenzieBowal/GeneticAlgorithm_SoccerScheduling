#schedule.py
#Creates the schedule data structure


class Schedule:
    
    schedule = []
    
    def __init__(self, numTimeSlots):
        self.numTimeSlots = numTimeSlots; #number of time slots determined from input file (varies for each test case)
        
        for i in range(5): #Days in week
        	Schedule.schedule.append([])
        	for j in range(numTimeSlots): #Time slots
        		Schedule.schedule[i].append([])
        		for k in range(2): #Create game and practice lists
        			Schedule.schedule[i][j].append([])
    
    def print(self):
        for i in range(5):
	        print(Schedule.schedule[i])

    def addGame(self, dayIdx, timeIdx, value):
        Schedule.schedule[timeIdx][dayIdx][0].append(value)

    def addPractice(self, dayIdx, timeIdx, value):
        Schedule.schedule[timeIdx][dayIdx][1].append(value)
