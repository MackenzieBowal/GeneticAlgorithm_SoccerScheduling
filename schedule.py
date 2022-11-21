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
        self.gamemin = 0
        self.practicemin = 0
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
        self.assignment = []
        
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
        print(sorted(self.assignment))

    def addGame(self, day, time, g):
        add = True
        if day == days['MO']:
            for i in range(0,2): #games on M,W,F are an hour long
                if (not self.schedule[days['MO']][time+i].hasRoomForGame() or
                    not self.schedule[days['WE']][time+i].hasRoomForGame() or
                    not self.schedule[days['FR']][time+i].hasRoomForGame()):
                    add = False
                    print("Can't add another game at that time!")
                    break
            if add:
                self.schedule[days['MO']][time+i].addGame(g)
                self.schedule[days['WE']][time+i].addGame(g)
                self.schedule[days['FR']][time+i].addGame(g)
                
                self.assignment.append(tuple([g,day,time]))

        else: #day == days['TU']
            for i in range(0,3): #games on T,TH are an hour and a half long
                if (not self.schedule[days['TU']][time+i].hasRoomForGame() or
                    not self.schedule[days['TH']][time+i].hasRoomForGame()):
                    add = False
                    print("Can't add another game at that time!")
                    break
            if add:
                self.schedule[days['TU']][time+i].addGame(g)
                self.schedule[days['TH']][time+i].addGame(g)
                
                self.assignment.append(tuple([g,day,time]))

    def addPractice(self, day, time, p):
        add = True
        if day == days['MO']:
            for i in range(0,2): #practices on M,W are an hour long
                if (not self.schedule[days['MO']][time+i].hasRoomForPractice() or
                    not self.schedule[days['WE']][time+i].hasRoomForPractice()):
                    add = False
                    print("Can't add another practice at that time!")
                    break
            if add:
                self.schedule[days['MO']][time+i].addPractice(p)
                self.schedule[days['WE']][time+i].addPractice(p)
                
                self.assignment.append(tuple([p,day,time]))

        elif day == days['TU']:
            for i in range(0,2): #practices on T,TH are an hour long
                if (not self.schedule[days['TU']][time+i].hasRoomForPractice() or
                    not self.schedule[days['TH']][time+i].hasRoomForPractice()):
                    add = False
                    print("Can't add another practice at that time!")
                    break
            if add:
                self.schedule[days['TU']][time+i].addPractice(p)
                self.schedule[days['TH']][time+i].addPractice(p)
                
                self.assignment.append(tuple([p,day,time]))

        else: #day == days['FR']
            for i in range(0,4): #practices on F are two hours long
                if not self.schedule[days['FR']][time+i].hasRoomForPractice():
                    add = False
                    print("Can't add another practice at that time!")
                    break
            if add:
                self.schedule[days['FR']][time+i].addPractice(p)
                
                self.assignment.append(tuple([p,day,time]))
        
    def setGamemax(self, day, time, m):
        if day == days['MO']:
            for i in range(0,2): #set an hour for game on M,W,F
                self.schedule[days['MO']][time+i].setGamemax(m)
                self.schedule[days['WE']][time+i].setGamemax(m)
                self.schedule[days['FR']][time+i].setGamemax(m)
        else: #day == days['TU']
            for i in range(0,3): #set an hour and half for game on T,TH
                self.schedule[days['TU']][time+i].setGamemax(m)
                self.schedule[days['TH']][time+i].setGamemax(m)
    
    def setGamemin(self, day, time, m):
        if day == days['MO']:
            for i in range(0,2): #set an hour for game on M,W,F
                self.schedule[days['MO']][time+i].setGamemin(m)
                self.schedule[days['WE']][time+i].setGamemin(m)
                self.schedule[days['FR']][time+i].setGamemin(m)
        else: #day == days['TU']
            for i in range(0,3): #set an hour and half for game on T,TH
                self.schedule[days['TU']][time+i].setGamemax(m)
                self.schedule[days['TH']][time+i].setGamemax(m)
        
    def setPracticemax(self, day, time, m):
        if day == days['MO']:
            for i in range(0,2): #set an hour for practice on M,W
                self.schedule[days['MO']][time+i].setPracticemax(m)
                self.schedule[days['WE']][time+i].setPracticemax(m)
        elif day == days['TU']:
            for i in range(0,2): #set an hour for practice on T,TH
                self.schedule[days['TU']][time+i].setPracticemax(m)
                self.schedule[days['TH']][time+i].setPracticemax(m)
        else: #day == days['FR']
            for i in range(0,4): #set two hours for practice on F
                self.schedule[days['FR']][time+i].setPracticemax(m)
     
    def setPracticemin(self, day, time, m):
        if day == days['MO']:
            for i in range(0,2): #set an hour for practice on M,W
                self.schedule[days['MO']][time+i].setPracticemin(m)
                self.schedule[days['WE']][time+i].setPracticemin(m)
        elif day == days['TU']:
            for i in range(0,2): #set an hour for practice on T,TH
                self.schedule[days['TU']][time+i].setPracticemin(m)
                self.schedule[days['TH']][time+i].setPracticemin(m)
        else: #day == days['FR']
            for i in range(0,4): #set two hours for practice on F
                self.schedule[days['FR']][time+i].setPracticemin(m)
