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

# Check partial assignments                                                             DONE
def check_hc1(sch):
    sched = sch.getSchedule()
    for assign in partAssign:
        gameorprac = assign[0]
        day = assign[1]
        time = assign[2]
        slot = sched[days[day]][times[time]]
        games_list = slot.getGames()
        prac_list = slot.getPractices()
        if (gameorprac not in games_list) and (gameorprac not in prac_list):
            return False
    
    return True


#Checks to make sure there are no practices for CSMA U12T1S and CSMA U13T1S between 6 and 7 on
#Tuesdays and Thursdays
#Should be true for all schedules because these practices are added in the parser                   DONE
def check_hc2(sch):
    sched = sch.getSchedule()
    for prac in pracList:
        if ("CMSA U12T1S" in prac or "CMSA U13T1S" in prac):
            Tues_at_six = sched[days["TU"]][times["18:00"]].getPractices()
            for prac in Tues_at_six:
                if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
                    return False
            
            Tues_at_six_thirty = sched[days["TU"]][times['18:30']].getPractices()
            for prac in Tues_at_six_thirty:
                if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
                    return False

            Thurs_at_six = sched[days["TH"]][times["18:00"]].getPractices()
            for prac in Thurs_at_six:
                if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
                    return False

            Thurs_at_six_thirty = sched[days["TH"]][times["18:00"]].getPractices()
            for prac in Thurs_at_six_thirty:
                if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
                    return False

    return True



#Checks to see if there are ever more games/practices assigned than max.                     DONE
#Should always be satisfied, even in partial schedules. 
# Our addGame() and addPractice() functions already check for this

def check_hc3(sch):
    for i in range(len(days)):
        for j in range(len(times)):
            slot = sch.getSchedule()[i][j]
            if len(slot.getGames()) > slot.getGameMax():
                return False   
            if len(slot.getPractices()) > slot.getPracMax():
                return False   
    return True

# Games and practices in the same division can't overlap                                DONE
def check_hc4(sch):
    for i in range(len(days)):
        for j in range(len(times)):
            slot = sch.getSchedule()[i][j]
            for game in slot.getGames():
                gameComponents = game.split(" ")
                for prac in slot.getPractices():
                    pracComponents = prac.split(" ")
                    if (gameComponents[0] == pracComponents[0] and gameComponents[1] == pracComponents[1] and \
                            (len(pracComponents) < 6 or gameComponents[3] == pracComponents[3])):
                        return False
    return True

# Check non-compatibility                                                                                       DONE
def check_hc5(sch):
    for a, b in notCompatible:
        for i in range(len(days)):
            for j in range(len(times)):
                slot = sch.getSchedule()[i][j]
                games = slot.getGames()
                pracs = slot.getPractices()
                if((a in games or a in pracs) and (b in games or b in pracs)):
                        return False
    return True


#Constraints 7, 8, and 9 are already checked when we add a game/practice
'''
def check_hc7(sch):
   for i in range(len(sch.getSchedule()[days["MO"]])):
        mon_games = sch.getSchedule()[days["MO"]][i].getGames()
        wed_games = sch.getSchedule()[days["WE"]][i].getGames()
        fri_games = sch.getSchedule()[days["FR"]][i].getGames()
        if(len(mon_games) != len(wed_games) or len(mon_games) != len(fri_games)):
            return False
        for mon_game in mon_games:
            if(mon_game not in wed_games):
                return False
            if(mon_game not in fri_games):
                return False
   return True

#checks to see if Monday/Wednesday practices are at the same time
#may not pass on all partial scehdules

def check_hc8(sch):
    for i in range(len(sch.getSchedule()[days["MO"]])):
        mon_pracs = sch.getSchedule()[days["MO"]][i].getPractices()
        wed_pracs = sch.getSchedule()[days["WE"]][i].getPractices()
        if(len(mon_pracs) != len(wed_pracs)):
            return False
        
        for mon_prac in mon_pracs:
            if(mon_prac not in wed_pracs):
                return False
    
    return True
        

#checks to see if Tuesday/Thrusday games and practices are at the same time
#may not pass on all partial scehdules


def check_hc9(sch):
    for i in range(len(sch.getSchedule()[days["TU"]])):
        tues_games = sch.getSchedule()[days["TU"]][i].getGames()
        thur_games = sch.getSchedule()[days["TH"]][i].getGames()

        tues_pracs = sch.getSchedule()[days["TU"]][i].getPractices()
        thur_pracs = sch.getSchedule()[days["TH"]][i].getPractices()

        if(len(tues_games) != len(thur_games)):
            return False
        if(len(tues_pracs) != len(thur_pracs)):
            return False
        
        for tues_game in tues_games:
            if(tues_game not in thur_games):
                return False
        
        for tues_prac in tues_pracs:
            if tues_prac not in thur_pracs:
                return False
        
    return True

'''



##Checks to make sure games in DIV 9X are not scheduled before 18:00                            DONE
##should pass on all partial schedules. 

def check_hc6(sch):

    numTimesBeforeSix = 20
    for i in range(len(days)):
        for j in range(numTimesBeforeSix):
            slot = sch.getSchedule()[i][j]
            slotGames = slot.getGames()
            slotPracs = slot.getPractices()
            for game in slotGames:
                if ("DIV 9" in game):
                    return False
            for prac in slotPracs:
                if ("DIV 9" in prac):
                    return False
    return True
    

#Checks to see if anything has been placed in an unwanted timeslot.                                 DONE
# Should pass for partial schedules.     

def check_hc7(sch):
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
    return True
        


#Makes sure that games aren't hosted between 11:00 and 12:30 on Tuesdays and Thursdays.                 DONE
#Should pass on all partial schedules. 

def check_hc8(sch):
    sched = sch.getSchedule()
    if(len(sched[days["TU"]][6].getGames()) != 0):
        return False
    if(len(sched[days["TU"]][7].getGames()) != 0):
        return False
    if(len(sched[days["TU"]][8].getGames()) != 0):
        return False
    if(len(sched[days["TH"]][6].getGames()) != 0):
        return False
    if(len(sched[days["TH"]][7].getGames()) != 0):
        return False
    if(len(sched[days["TH"]][8].getGames()) != 0):
        return False

    return True
    

#Checks to see if any games in the leagues U15, U16, U17 and U19 are in the same timeslot.              DONE
#Should pass on all partial schedules. 
def check_hc9(sch):
    for i in range(len(days)):
        for j in range(len(times)):
            slotGames = sch.getSchedule()[i][j].getGames()
            for game1 in slotGames:
                if ("U15" in game1 or "U16" in game1 or "U17" in game1 or "U19" in game1):
                    for game2 in slotGames:
                        if ("U15" in game2 or "U16" in game2 or "U17" in game2 or "U19" in game2) and (game1 != game2):
                            return False
    return True


#Checks to make sure that no games/practices in the tier div U12T1S or U13T1S is in the same slot.          DONE
#Should pass all partial schedules. 

def check_hc10(sch):

    for i in range(len(days)):
        for j in range(len(times)):
            slot = sch.getSchedule()[i][j]

            for p in slot.getPractices():
                # check U12T1S
                if ("CMSA U12T1S" in p):
                    for prac in slot.getPractices():
                        if ("CMSA U12T1 " in prac):
                            return False
                    for game in slot.getGames():
                        if ("CMSA U12T1 " in game):
                            return False
                # check U13T1S
                if ("CMSA U13T1S" in p):
                    for prac in slot.getPractices():
                        if ("CMSA U13T1 " in prac):
                            return False
                    for game in slot.getGames():
                        if ("CMSA U13T1 " in game):
                            return False

    return True                


# THIS IS A SUPER BASIC IMPLEMENTATION OF CONSTR() TO TEST REPAIR TREE - THIS STILL NEEDS TO BE PROPERLY IMPLEMENTED BASED ON pg. 2 OF REPORT 
def constr(sch):

    hc1 = check_hc1(sch)
    hc2 = check_hc2(sch)
    hc3 = check_hc3(sch)
    hc4 = check_hc4(sch)
    hc5 = check_hc5(sch)
    hc6 = check_hc6(sch)
    hc7 = check_hc7(sch)
    hc8 = check_hc8(sch)
    hc9 = check_hc9(sch)
    hc10 = check_hc10(sch)

    return hc1 and hc2 and hc3 and hc4 and hc5 and hc6 and hc7 and hc8 and hc9 and hc10
