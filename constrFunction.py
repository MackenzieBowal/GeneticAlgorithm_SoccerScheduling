import schedule
from constants import days, times


def initiateConstr(gl, pl, vgs, vps, nc, unw, pref, pr, pa):
    global gamesList, pracList, validGameSlots, validPracSlots, notCompatible
    global unwanted, preferences, pair, partAssign

    gamesList = gl
    pracList = pl
    validGameSlots = vgs
    validPracSlots = vps
    notCompatible = nc
    unwanted = unw
    preferences = pref
    pair = pr
    partAssign = pa


def findTimeslot(sch, gameprac):
    for assign in sch.getAssignment():
        if assign[0] == gameprac:
            return assign[1], assign[2]
            break
    return -1, -1

def oneBigConstr(sch, isGame, currGameOrPrac):

    #if(isGame):
    day, time = findTimeslot(sch, currGameOrPrac)
    slot = sch.getSchedule()[day][time]
    slotGames = slot.getGames()
    slotPracs = slot.getPractices()

    # hc4
    for game in slotGames:
        gameComponents = game.split(" ")
        for prac in slotPracs:
            pracComponents = prac.split(" ")
            if (gameComponents[0] == pracComponents[0] and gameComponents[1] == pracComponents[1] and \
                    (len(pracComponents) < 6 or gameComponents[3] == pracComponents[3])):
                return False

    # hc5
    for (a, b) in notCompatible:
        if((a in slotGames or a in slotPracs) and (b in slotGames or b in slotPracs)):
                return False

    # hc6
    if time < 20:
        for game in slotGames:
            if ("DIV 9" in game):
                return False
        for prac in slotPracs:
            if ("DIV 9" in prac):
                return False
    
    # hc7
    for unwant_sched in unwanted:
        gameorprac = unwant_sched[0]
        day = unwant_sched[1]
        time = unwant_sched[2]
        for game in sch.getSchedule()[days[day]][times[time]].getGames():
            if(game == gameorprac):
                return False
        for prac in sch.getSchedule()[days[day]][times[time]].getPractices():
            if(prac == gameorprac):
                return False

    # hc8
    sched = sch.getSchedule()
    if(len(sched[days["TU"]][6].getGames()) != 0):
        return False

    # hc9
    for game1 in slotGames:
        if ("U15" in game1 or "U16" in game1 or "U17" in game1 or "U19" in game1):
            for game2 in slotGames:
                if ("U15" in game2 or "U16" in game2 or "U17" in game2 or "U19" in game2) and (game1 != game2):
                    return False

    # hc10
    for p in slotPracs:
        # check U12T1S
        if ("CMSA U12T1S" in p):
            for prac in slotPracs:
                if ("CMSA U12T1 " in prac):
                    return False
            for game in slotGames:
                if ("CMSA U12T1 " in game):
                    return False
        # check U13T1S
        if ("CMSA U13T1S" in p):
            for prac in slotPracs:
                if ("CMSA U13T1 " in prac):
                    return False
            for game in slotGames:
                if ("CMSA U13T1 " in game):
                    return False
            break

    return True


# THIS IS A SUPER BASIC IMPLEMENTATION OF CONSTR() TO TEST REPAIR TREE - THIS STILL NEEDS TO BE PROPERLY IMPLEMENTED BASED ON pg. 2 OF REPORT 
def constr(sch, currGameOrPrac, isGame):

    return oneBigConstr(sch, isGame, currGameOrPrac)
