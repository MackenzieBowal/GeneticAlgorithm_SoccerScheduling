#schedule.py
#Contains the schedule data structure

import copy
from constants import *

numDays = 5
numTimeslots = 26
"""
Timeslot class: One time slot
* Stores a list of games and a list of practices at a specific time
* THIS CLASS IS ONLY USED WITHIN Schedule
"""
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
    
    def getGameMax(self):
        return self.gamemax

    def getPracMax(self):
        return self.practicemax

    def getGameMin(self):
        return self.gamemin

    def getPracMin(self):
        return self.practicemin

    def getGames(self):
        return self.games

    def getPractices(self):
        return self.practices




"""
Schedule class: One soccer schedule
* DO NOT use __init__! The constructor is used by main.py/parse() which creates a template schedule
                        with max/min game and practice values for each time slot
* To create a new soccer schedule: Use Schedule.newSchedule()
                                    This creates a deep copy of the template schedule which can then
                                    be populated with games/practices
* Use Schedule.addGame() and Schedule.addPractice() to add games/practices to a soccer schedule
* The setGamemax() etc. functions are only used by the parser. This information does not change after
    the input file has been parsed
* print() prints the schedule as a 4-dimensional list: schedule[day[time[game/practice]]]
* See the example in main.py for how to create a schedule and populate it with a basic arrangement of
    games and practices
"""
class Schedule:
    
    def __init__(self):
        self.schedule = []
        self.assignment = []
        
        for day in range(numDays): #Days in week
            self.schedule.append([])
            for time in range(numTimeslots): #Timeslots at half-hour intervals from 8:00-20:30
                self.schedule[day].append(Timeslot())
    
    def print(self):
        print('[', end='')
        for day in range(numDays):
            print('[', end='')
            for time in range(numTimeslots):
                if time == numTimeslots-1:
                    print(str(self.schedule[day][time]), end='')
                else: print(str(self.schedule[day][time]) + ', ', end='')
            if day == numDays-1:
                print(']', end='')
            else: print(']')
        print(']')
        print(sorted(self.assignment))

    def newSchedule(self):
        return copy.deepcopy(self)
    
    def getAssignment(self):
        return self.assignment

    def getSchedule(self):
        return self.schedule

    def addGame(self, day, time, g):
        print("in addGame, day = "+str(day)+" time = "+str(time)+" game = "+g)
        add = True
        if day == days['MO']:
            print("in MO")
            for i in range(0,2): #games on M,W,F are an hour long
                print("checking add")
                print(str(self.schedule[days['MO']][time+i].hasRoomForGame()))
                print(str(self.schedule[days['WE']][time+i].hasRoomForGame()))
                print(str(self.schedule[days['FR']][time+i].hasRoomForGame()))

                if (not self.schedule[days['MO']][time+i].hasRoomForGame() or
                    not self.schedule[days['WE']][time+i].hasRoomForGame() or
                    not self.schedule[days['FR']][time+i].hasRoomForGame()):
                    add = False
                    break
            if add:
                for i in range(0,2):
                    print("adding")
                    self.schedule[days['MO']][time+i].addGame(g)
                    self.schedule[days['WE']][time+i].addGame(g)
                    self.schedule[days['FR']][time+i].addGame(g)
                
                self.assignment.append(tuple([g,day,time]))
                return True

        else: #day == days['TU']
            for i in range(0,3): #games on T,TH are an hour and a half long
                if (not self.schedule[days['TU']][time+i].hasRoomForGame() or
                    not self.schedule[days['TH']][time+i].hasRoomForGame()):
                    add = False
                    break
            if add:
                for i in range(0,3):
                    self.schedule[days['TU']][time+i].addGame(g)
                    self.schedule[days['TH']][time+i].addGame(g)
                
                self.assignment.append(tuple([g,day,time]))
                return True
        return False

    def addPractice(self, day, time, p):
        add = True
        if day == days['MO']:
            for i in range(0,2): #practices on M,W are an hour long
                if (not self.schedule[days['MO']][time+i].hasRoomForPractice() or
                    not self.schedule[days['WE']][time+i].hasRoomForPractice()):
                    add = False
                    break
            if add:
                for i in range(0,2):
                    self.schedule[days['MO']][time+i].addPractice(p)
                    self.schedule[days['WE']][time+i].addPractice(p)
                
                self.assignment.append(tuple([p,day,time]))
                return True

        elif day == days['TU']:
            for i in range(0,2): #practices on T,TH are an hour long
                if (not self.schedule[days['TU']][time+i].hasRoomForPractice() or
                    not self.schedule[days['TH']][time+i].hasRoomForPractice()):
                    add = False
                    break
            if add:
                for i in range(0,2):
                    self.schedule[days['TU']][time+i].addPractice(p)
                    self.schedule[days['TH']][time+i].addPractice(p)
                
                self.assignment.append(tuple([p,day,time]))
                return True

        else: #day == days['FR']
            for i in range(0,4): #practices on F are two hours long
                if not self.schedule[days['FR']][time+i].hasRoomForPractice():
                    add = False
                    break
            if add:
                for i in range(0,4):
                    self.schedule[days['FR']][time+i].addPractice(p)
                
                self.assignment.append(tuple([p,day,time]))
                return True
        return False
        
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
                self.schedule[days['TU']][time+i].setGamemin(m)
                self.schedule[days['TH']][time+i].setGamemin(m)
        
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
