import schedule

def initiateEval(wmf, wpf, wpr, wsd, pgm, ppm, pref, pnp, ps, pr):
    global wMinFilled, wPref, wPair, wSecDiff, penGameMin
    global penPracticeMin, preferences, penNotPaired, penSection, pair

    wMinFilled = wmf
    wPref = wpf
    wPair = wpr
    wSecDiff = wsd
    penGameMin = pgm
    penPracticeMin = ppm
    preferences = pref
    penNotPaired = pnp
    penSection = ps
    pair = pr

    return


def eval(assign):
    return evalMinFilled(assign)*wMinFilled + evalPref(assign)*wPref + \
    evalPair(assign)*wPair + evalSecDiff(assign)*wSecDiff

def evalMinFilled(assign):
    penalty = 0
    for day in range(schedule.numDays):
        for time in range(schedule.numTimeslots):
            slot = assign[day][time]
            if len(slot.games) < slot.gamemin:
                penalty += penGameMin * (slot.gamemin - len(slot.games))
            if len(slot.practices) < slot.practicemin:
                penalty += penPracticeMin * (slot.practicemin - len(slot.practices))
    return penalty

def evalPref(assign):
    penalty = 0
    for t in preferences:
        if (t[2] not in assign[t[0]][t[1]].games and t[2] not in assign[t[0]][t[1]].practices):
            penalty += t[3]
    return penalty
    
def evalPair(assign):
    penalty = 0
    for day in range(schedule.numDays):
        for time in range(schedule.numTimeslots):
            for p in pair:
                if (p[0] in assign[day][time].games or p[0] in assign[day][time].practices) and (p[1] not in assign[day][time].games or p[1] not in assign[day][time].practices):
                    penalty += penNotPaired
    return penalty

def evalSecDiff(assign):
    penalty = 0
    for day in range(schedule.numDays):
        for time in range(schedule.numTimeslots):
            for i in range(len(assign[day][time].games)):
                temp = assign[day][time].games[i].split()
                for j in range(i+1,len(assign[day][time].games)):
                    temp1 = assign[day][time].games[j].split()
                    if temp[1] == temp1[1]:
                        penalty += penSection
    return penalty