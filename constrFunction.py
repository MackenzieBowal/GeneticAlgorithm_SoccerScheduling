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

def check_hc1(sch):
    sched = sch.getSchedule()
    for assign in partAssign:
        league_tier_div = assign[0]
        day = assign[1]
        time = assign[2]
        games_list = sched[days[day]][times[time]].getGames()
        if(league_tier_div not in games_list):
            return False
    
    return True


#Checks to make sure there are no practices for CSMA U12T1S and CSMA U13T1S between 6 and 7 on
#Tuesdays and Thursdays
#Should be true for partial schedules. 

def check_hc2(sch):
    sched = sch.getSchedule()
    prac_at_six = sched[days["TU"]][20].getPractices()
    for prac in prac_at_six:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False
    
    prac_at_six_thirty = sched[days["TU"]][20].getPractices()
    for prac in prac_at_six_thirty:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False

    prac_at_six = sched[days["TH"]][20].getPractices()
    for prac in prac_at_six:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False

    prac_at_six_thirty = sched[days["TH"]][20].getPractices()
    for prac in prac_at_six_thirty:
        if (prac.split()[0] == "CSMA" and (prac.split()[1] == "U12T1S" or prac.split()[1] == "U13T1S")):
            return False

    return True



#Checks to see if there are ever more games assigned than game max. 
#Should always be satisfied, even in partial schedules. 

def check_hc3(sch):
    for day in sch.getSchedule():
        for timeslot in day:
            if(len(timeslot.getGames()) > timeslot.getGameMax()):
                return False
    return True


#Checks to see if there are ever more practices than practice max. 
#Should always be satisifed, even in partial schedules. 

def check_hc4(sch):
    for day in sch.getSchedule():
        for timeslot in day:
            if(len(timeslot.getPractices()) > timeslot.getPracMax()):
                return False
    return True


def check_hc5(sch):
    for day in sch.getSchedule():
        for timeslot in day:
            for game in timeslot.getGames():
                if(game in timeslot.getPractices()):
                    return False
    return True


def check_hc6(sch):
    for a, b in notCompatible:
        for day in sch.getSchedule():
            for timeslot in day:
                if((a in timeslot.getGames() or a in timeslot.getPractices()) and (b in timeslot.getGames() or b in timeslot.getPractices())):
                    return False
    return True


#Checks to see that all monday wednesday friday games are scheduled for the same time. 
#Some partially complete schedules may not follow this check. 
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





##Checks to make sure games in DIV 9 are not scheduled before 18:00
##should pass on all partial schedules. 

def check_hc10(sch):
    for day in sch.getSchedule():
        for time in range(times["18:00"]):
            for games in day[time].getGames():
                if(games.split()[3] == "09"):
                    return False
            for prac in day[time].getPractices():
                if(prac.split()[3] == "09"):
                    return False
    return True
    

#Checks to see if anything has been placed in an unwanted timeslot. 
# Should pass for partial schedules.     

def check_hc11(sch):
    for unwant_sched in unwanted:
        g = unwant_sched[0]
        day = unwant_sched[1]
        time = unwant_sched[2]
        for game in sch.getSchedule()[days[day]][times[time]].getGames():
            if(game == g):
                return False
    
    return True
        


#Makes sure that games aren't hosted between 11:00 and 12:30 on Tuesdays and Thrusdays. 
#Should pass on all partial schedules. 

def check_hc12(sch):
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
    

#Checks to see if any games in the leagues U15, U16, U17 and U19 are in the same timeslot. 
#Should pass on all partial schedules. 
#DOUBLE CHECK TO MAKE SURE THIS MATCHES HARD CONSTRAINTS IN ASSIGN SPECS. 
def check_hc13(sch):
    for day in sch.getSchedule():
        for timeslot in day:
            one_game_found = False
            for game in timeslot.getGames():
                game_list = game.split()
                tier_div = game[1]
                if(tier_div[0:3] == "U15" or tier_div[0:3] == "U16" or tier_div[0:3] == "U17" or tier_div[0:3] == "U19"):
                    if(not one_game_found): 
                        one_game_found = True
                    else:
                        return False
    
    return True
                    

#Checks to make sure that no games in the tear div U12T1S is in the same gameslot. 
#Should pass all partial schedules. 

def check_hc14(sch):
    for day in sch.getSchedule():
        for timeslot in day:
            u12T1S = False
            for game in timeslot.getGames():
                tier_div = game[1]
                if(tier_div == "U12T1S"):
                    if(not u12T1S): 
                        u12T1S = True
                    else: 
                        return False
            for prac in timeslot.getPractices():
                tier_div = prac[1]
                if(tier_div == "U12T1S"):
                    if(not u12T1S): 
                        u12T1S = True
                    else: 
                        return False

    return True
                
#Checks to make sure that no games in the tear div U13T1S is in the same gameslot. 
#Should pass all partial schedules. 


def check_hc15(sch):
    for day in sch.getSchedule():
        for timeslot in day:
            u13T1S = False
            for game in timeslot.getGames():
                tier_div = game[1]
                if(tier_div == "U13T1S"):
                    if(not u13T1S): 
                        u13T1S = True
                    else: 
                        return False
                if(tier_div == "U13T1S"):
                    if(not u13T1S): 
                        u13T1S = True
                    else: 
                        return False
    return True
                


# THIS IS A SUPER BASIC IMPLEMENTATION OF CONSTR() TO TEST REPAIR TREE - THIS STILL NEEDS TO BE PROPERLY IMPLEMENTED BASED ON pg. 2 OF REPORT 
def constr(sch):


    partialFlag = True

    # Check if schedule is complete or not
    if (len(sch.getAssignment()) == len(gamesList) + len(pracList) + len(partAssign)):
        partialFlag = False

    if(not partialFlag):
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
       hc11 = check_hc11(sch)
       hc12 = check_hc12(sch)
       hc13 = check_hc13(sch)
       hc14 = check_hc14(sch)
       hc15 = check_hc15(sch)

       return hc1 and hc2 and hc3 and hc4 and hc5 and hc6 and hc7 and hc8 \
           and hc9 and hc10 and hc11 and hc12 and hc13 and hc14 and hc15
    
    else:
        if(gamesDoneFlag):
            hc1 = check_hc1(sch)
            hc2 = check_hc2(sch)
            hc3 = check_hc3(sch)
            hc4 = check_hc4(sch)
            hc5 = check_hc5(sch)
            hc6 = check_hc6(sch)
            hc7 = check_hc7(sch)
            hc10 = check_hc10(sch)
            hc11 = check_hc11(sch)
            hc12 = check_hc12(sch)
            hc13 = check_hc13(sch)
            hc14 = check_hc14(sch)
            hc15 = check_hc15(sch)

            return hc1 and hc2 and hc3 and hc4 and hc5  and hc6 and hc7 and \
            hc10 and hc11 and hc12 and hc13 and hc15
        
        elif(pracDoneFlag):
            hc1 = check_hc1(sch)
            hc2 = check_hc2(sch)
            hc3 = check_hc3(sch)
            hc4 = check_hc4(sch)
            hc5 = check_hc5(sch)
            hc6 = check_hc6(sch)
            hc8 = check_hc8(sch)
            hc10 = check_hc10(sch)
            hc11 = check_hc11(sch)
            hc12 = check_hc12(sch)
            hc13 = check_hc13(sch)
            hc14 = check_hc14(sch)
            hc15 = check_hc15(sch)

            return  hc1 and hc2 and hc3 and hc4 and hc5 and hc8 and \
            hc10 and hc11 and hc12 and hc13 and hc14 and hc15
        else:
            hc1 = check_hc1(sch)
            hc2 = check_hc2(sch)
            hc3 = check_hc3(sch)
            hc4 = check_hc4(sch)
            hc5 = check_hc5(sch)
            hc6 = check_hc6(sch)
            hc7 = check_hc7(sch)
            hc10 = check_hc10(sch)
            hc11 = check_hc11(sch)
            hc12 = check_hc12(sch)
            hc13 = check_hc13(sch)
            hc14 = check_hc14(sch)
            hc15 = check_hc15(sch)

            return hc1 and hc2 and hc3 and hc4 and hc5 and hc6 and \
            hc10 and hc11 and hc12 and hc13 and hc14 and hc15
