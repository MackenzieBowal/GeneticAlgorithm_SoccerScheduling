from copy import deepcopy
import schedule
from constants import days, times

def initiateEval(wmf, wpf, wpr, wsd, pgm, ppm, pref, pnp, ps, pr):
    global wMinFilled, wPref, wPair, wSecDiff, penGameMin
    global penPracticeMin, preferences, penNotPaired, penSection, pair

    wMinFilled = int(wmf)
    wPref = int(wpf)
    wPair = int(wpr)
    wSecDiff = int(wsd)
    penGameMin = int(pgm)
    penPracticeMin = int(ppm)
    preferences = pref
    penNotPaired = int(pnp)
    penSection = int(ps)
    pair = pr

    return


def eval(assign):
    print("EVAL: "+str(evalMinFilled(assign)*wMinFilled)+" + " + str(evalPref(assign)*wPref)+" + "+str(evalPair(assign)*wPair)+" + " + str(evalSecDiff(assign)*wSecDiff))
    return evalMinFilled(assign)*wMinFilled + evalPref(assign)*wPref + \
    evalPair(assign)*wPair + evalSecDiff(assign)*wSecDiff

def evalMinFilled(assign):
    penalty = 0
    for day in range(schedule.numDays):
        for time in range(schedule.numTimeslots):
            slot = assign.getSchedule()[day][time]
            if len(slot.games) < slot.gamemin:
                penalty += penGameMin * (slot.gamemin - len(slot.games))
            if len(slot.practices) < slot.practicemin:
                penalty += penPracticeMin * (slot.practicemin - len(slot.practices))
    return penalty

def evalPref(assign):
    penalty = 0
    for t in preferences:
        slotGames = assign.getSchedule()[days[t[0]]][times[t[1]]].games
        slotPractices = assign.getSchedule()[days[t[0]]][times[t[1]]].practices
        if (t[2] not in slotGames and t[2] not in slotPractices):
            penalty += int(t[3])
    return penalty
    
def evalPair(assign):
    penalty = 0
    global pair
    pairCopy = deepcopy(pair)
    for day in range(schedule.numDays):
        for time in range(schedule.numTimeslots):
            slotGames = assign.getSchedule()[day][time].games
            slotPractices = assign.getSchedule()[day][time].practices
            for p in pairCopy:
                if ((p[0] in slotGames or p[0] in slotPractices) and (p[1] not in slotGames or p[1] not in slotPractices)) \
                    or ((p[1] in slotGames or p[1] in slotPractices) and (p[0] not in slotGames or p[0] not in slotPractices)):
                    penalty += penNotPaired
                    pairCopy.remove(p)
    return penalty

def evalSecDiff(assign):
    penalty = 0
    checkedPairs = []
    for day in range(schedule.numDays):
        for time in range(schedule.numTimeslots):
            slotGames = assign.getSchedule()[day][time].games
            for i in range(len(slotGames)):
                temp = slotGames[i].split()
                for j in range(i+1,len(slotGames)):
                    temp1 = slotGames[j].split()
                    if ((slotGames[i], slotGames[j]) not in checkedPairs) and ((slotGames[j], slotGames[i]) not in checkedPairs):
                        if temp[1] == temp1[1] and temp[3] != temp1[3]:
                            penalty += penSection
                            checkedPairs.append((slotGames[i], slotGames[j]))
    return penalty
