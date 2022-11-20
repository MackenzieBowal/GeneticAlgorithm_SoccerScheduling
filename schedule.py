#schedule.py
#Contains the schedule data structure

from constants import *

numDays = 5
numTimeslots = 26

#Stores a list of games and a list of practices at a specific time
class Timeslot:
    
    def __init__(self):
        self.gamemax = 0
        self.practicemax = 0
        self.games = []
        self.practices = []
    
    def __str__(self):
        return f'[{self.games},{self.practices}]'
    
    def addGame(self, g):
        self.games.append(g)
    
    def addPractice(self, p):
        self.practices.append(p)
    
    def setGamemax(self, m):
        self.gamemax = m
    
    def setGamemin(self, m):
        self.gamemin = m
    
    def setPracticemax(self, m):
        self.practicemax = m
    
    def setPracticemin(self, m):
        self.practicemin = m
        
    def hasRoomForGame(self):
        if len(self.games) < self.gamemax:
            return True
        else: return False
        
    def hasRoomForPractice(self):
        if len(self.practices) < self.practicemax:
            return True
        else: return False

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
        if day == days['MO']:
            if (self.schedule[days['MO']][time].hasRoomForGame() and
                self.schedule[days['WE']][time].hasRoomForGame() and
                self.schedule[days['FR']][time].hasRoomForGame()):
                self.schedule[days['MO']][time].addGame(g)
                self.schedule[days['WE']][time].addGame(g)
                self.schedule[days['FR']][time].addGame(g)
            else: print("Can't add another game at that time!")
        else: #day == days['TU']
            if (self.schedule[days['TU']][time].hasRoomForGame() and
                self.schedule[days['TH']][time].hasRoomForGame()):
                self.schedule[days['TU']][time].addGame(g)
                self.schedule[days['TH']][time].addGame(g)
            else: print("Can't add another game at that time!")

    def addPractice(self, day, time, p):
        if day == days['MO']:
            if (self.schedule[days['MO']][time].hasRoomForPractice() and
                self.schedule[days['WE']][time].hasRoomForPractice()):
                self.schedule[days['MO']][time].addPractice(p)
                self.schedule[days['WE']][time].addPractice(p)
            else: print("Can't add another practice at that time!")
        elif day == days['TU']:
            if (self.schedule[days['TU']][time].hasRoomForPractice() and
                self.schedule[days['TH']][time].hasRoomForPractice()):
                self.schedule[days['TU']][time].addPractice(p)
                self.schedule[days['TH']][time].addPractice(p)
            else: print("Can't add another practice at that time!")
        else: #day == days['FR']
            if self.schedule[days['FR']][time].hasRoomForPractice():
                self.schedule[days['FR']][time].addPractice(p)
            else: print("Can't add another practice at that time!")
        
    def setGamemax(self, day, time, m):
        if day == days['MO']:
            self.schedule[days['MO']][time].setGamemax(m)
            self.schedule[days['WE']][time].setGamemax(m)
            self.schedule[days['FR']][time].setGamemax(m)
            
            self.schedule[days['MO']][time+1].setGamemax(m) #set an hour for game on M,W,F
            self.schedule[days['WE']][time+1].setGamemax(m)
            self.schedule[days['FR']][time+1].setGamemax(m)
        else: #day == days['TU']
            self.schedule[days['TU']][time].setGamemax(m)
            self.schedule[days['TH']][time].setGamemax(m)
            
            self.schedule[days['TU']][time+2].setGamemax(m) #set an hour and half for game on T,TH
            self.schedule[days['TH']][time+2].setGamemax(m)
    
    def setGamemin(self, day, time, m):
        if day == days['MO']:
            self.schedule[days['MO']][time].setGamemin(m)
            self.schedule[days['WE']][time].setGamemin(m)
            self.schedule[days['FR']][time].setGamemin(m)
            
            self.schedule[days['MO']][time+1].setGamemin(m)
            self.schedule[days['WE']][time+1].setGamemin(m)
            self.schedule[days['FR']][time+1].setGamemin(m)
        else: #day == days['TU']
            self.schedule[days['TU']][time].setGamemin(m)
            self.schedule[days['TH']][time].setGamemin(m)
            
            self.schedule[days['TU']][time+2].setGamemin(m)
            self.schedule[days['TH']][time+2].setGamemin(m)
        
    def setPracticemax(self, day, time, m):
        if day == days['MO']:
            self.schedule[days['MO']][time].setPracticemax(m)
            self.schedule[days['WE']][time].setPracticemax(m)
            
            self.schedule[days['MO']][time+1].setPracticemax(m)
            self.schedule[days['WE']][time+1].setPracticemax(m)
        elif day == days['TU']:
            self.schedule[days['TU']][time].setPracticemax(m)
            self.schedule[days['TH']][time].setPracticemax(m)
            
            self.schedule[days['TU']][time+2].setPracticemax(m)
            self.schedule[days['TH']][time+2].setPracticemax(m)
        else: #day == days['FR']
            self.schedule[days['FR']][time].setPracticemax(m)
            
            self.schedule[days['FR']][time+4].setPracticemax(m)
     
    def setPracticemin(self, day, time, m):
        if day == days['MO']:
            self.schedule[days['MO']][time].setPracticemin(m)
            self.schedule[days['WE']][time].setPracticemin(m)
            
            self.schedule[days['MO']][time+1].setPracticemin(m)
            self.schedule[days['WE']][time+1].setPracticemin(m)
        elif day == days['TU']:
            self.schedule[days['TU']][time].setPracticemin(m)
            self.schedule[days['TH']][time].setPracticemin(m)
            
            self.schedule[days['TU']][time+2].setPracticemin(m)
            self.schedule[days['TH']][time+2].setPracticemin(m)
        else: #day == days['FR']
            self.schedule[days['FR']][time].setPracticemin(m)
            
            self.schedule[days['FR']][time+4].setPracticemin(m)
