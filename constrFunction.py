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
    """
    for i in range(len(days)):
        for j in range(len(times)):
            slot = sch.getSchedule()[i][j]
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
            if j < 20:
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


                """

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

<<<<<<< HEAD
    #hc1 = check_hc1(sch)
    #hc2 = check_hc2(sch)
    #hc3 = check_hc3(sch)
    '''
    hc4 = check_hc4(sch)
    hc5 = check_hc5(sch)
    hc6 = check_hc6(sch)
    hc7 = check_hc7(sch)
    hc8 = check_hc8(sch)
    hc9 = check_hc9(sch)
    hc10 = check_hc10(sch)

    return hc4 and hc5 and hc6 and hc7 and hc8 and hc9 and hc10
    '''
    return oneBigConstr(sch, currGameOrPrac, isGame)
=======
    return oneBigConstr(sch, time, day)
>>>>>>> 518e399bc741db143f2efba16d56810890eb32ce
