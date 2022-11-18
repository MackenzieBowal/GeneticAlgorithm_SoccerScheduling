#schedule.py
#Contains the schedule data structure

numDays = 5
numTimeslots = 26

#Stores a list of games and a list of practices at a specific time
class Timeslot:
    
    def __init__(self):
        self.gamemax = 2
        self.practicemax = 2
        self.games = []
        self.practices = []
    
    def __str__(self):
        return f'[{self.games},{self.practices}]'
    
    def addGame(self, g):
        if len(self.games) < self.gamemax:
            self.games.append(g)
        else: print("Can't add another game at that time!")
    
    def addPractice(self, p):
        if len(self.practices) < self.practicemax:
            self.practices.append(p)
        else: print("Can't add another practice at that time!")
    
    def setGamemax(self, m):
        self.gamemax = m
    
    def setPracticemax(self, m):
        self.practicemax = m

class Schedule:
    
    def __init__(self):
        self.schedule = []
        
        for day in range(numDays): #Days in week
            self.schedule.append([])
            for time in range(numTimeslots): #Timeslots at half-hour intervals from 8:00-20:30
                self.schedule[day].append(Timeslot())
    
    def print(self):
        for day in range(numDays):
            print('[', end='')
            for time in range(numTimeslots):
                if time == numTimeslots-1:
                    print(str(self.schedule[day][time]), end='')
                else: print(str(self.schedule[day][time]) + ', ', end='')
            print(']')

    def addGame(self, day, time, g):
        self.schedule[day][time].addGame(g)

    def addPractice(self, day, time, p):
        self.schedule[day][time].addPractice(p)
