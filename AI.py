import random

def runnerAI(unit, bulldogs):
    frame = FrameScan(unit, bulldogs)

    #assigns movement direction to results given
    result = Avoidance(frame)
    
    #if no bulldogs are near move runner right
    if not result[0] and not result[1] and not result[2] and not result[3]:
        result[3] = True

    return result

def bulldogAI(unit, runners,  bulldogs):
    buffer = FrameScan(unit, runners)
    result = [False,False,False,False]
    empty = True
    for i in buffer:
        if i > 0:
            empty = False
    if empty == False:
        maxi = buffer.index(max(buffer))
        if maxi == 0:
            result[0] = True
            result[2] = True
        elif maxi == 1:
            result[0] = True
        elif maxi == 2:
            result[0] = True
            result[3] = True
        elif maxi == 3:
            result[3] = True
        elif maxi == 4:
            result[1] = True
            result[3] = True
        elif maxi == 5:
            result[1] = True
        elif maxi == 6:  
            result[1] = True
            result[2] = True
        elif maxi == 7:
            result[2] = True
    
    if not result[0] and not result[1] and not result[2] and not result[3]:
        frame = FrameScan(unit, bulldogs)
        result = Avoidance(frame)
        if not result[0] and not result[1] and not result[2] and not result[3]:
            result[random.choice([0,1,2,3])] = True

    return result

def FrameScan(unit, group):
    #frame is the area surrounding a unit and 
    #goes clockwise starting in the top left
    #query are the units grid coordinates
    #ticker is the cycles throught the clockwise motion
    frame = [0,0,0,0,0,0,0,0]
    qry = unit.GridCoord
    ticker = [[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]

    for x in ticker:
        for i in group:
            if qry[0]+x[0] == i.GridCoord[0]:
                if qry[1]+x[1] == i.GridCoord[1]:
                    frame[ticker.index(x)] += 1

    return frame

def Avoidance(frame):
    #assigns movement direction to results given
    result = [False,False,False,False]
    if frame[0]>0 or frame[1]>0 or frame[2]>0: 
        result[1] = True #down
    if frame[2]>0 or frame[3]>0 or frame[4]>0: 
        result[2] = True #left
    if frame[4]>0 or frame[5]>0 or frame[6]>0: 
        result[0] = True #up
    if frame[6]>0 or frame[7]>0 or frame[0]>0: 
        result[3] = True #right

    return result