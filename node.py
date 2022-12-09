#node.py
#Defines node data structure for the nodes passed in Repair OR Tree 

import copy
from constants import *
import schedule

class RepairNode:

    def __init__(self):
        self._id = id(self)
        self.mySched = schedule.Schedule()
        self.gamesLeft = []
        self.pracLeft = []
        self.depth = 0
        # sol-entry [? = 0, yes = 1, no = 2]
        self.solEntry = 0
        self.currGamePrac = ""
        self.isGame = False

    def getCurrGamePrac(self):
        return self.currGamePrac

    def setCurrGamePrac(self, currGamePrac):
        self.currGamePrac = currGamePrac
    
    def getIsGame(self):
        return self.isGame

    def setIsGame(self, isGame):
        self.isGame = isGame
    
    def newNode(self):
        return copy.deepcopy(self)
    
    def getID(self):
        return self._id

    
    def printNodeContent(self):
        print('Node at depth ', self.depth)
        print('\n')
        print('Games left ', self.gamesLeft)
        print('\n')
        print('Practices left ', self.pracLeft)
        print('\n')
        print('Sol entry ', self.solEntry)
        print('\n')
        print(self.mySched.print())
        print('\n')

    def getSchedule(self):
        return self.mySched

    def setUniqueID(self):
        self._id = id(self)

    def setSchedule(self, newSchedule):
        self.mySched = copy.copy(newSchedule)

    def setGamesLeft(self, newGamesLeft):
        self.gamesLeft = newGamesLeft

    def setPracLeft(self, newPracLeft):
        self.pracLeft = newPracLeft

    def setDepth(self, newDepth):
        self.depth = newDepth

    def setSolEntry(self, newSolEntry):
        self.solEntry = newSolEntry

    def getGamesLeft(self):
        return self.gamesLeft

    def getPracLeft(self):
        return self.pracLeft

    def getDepth(self):
        return self.depth

    def getSolEntry(self):
        return self.solEntry

    
    
       
