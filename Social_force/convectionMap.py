import math
import csv

unitPerMeter = 10
startX = 1.0
startY = 5 - 0.5
maxX = 1 + 14
maxY = 5 + 4 + 0.5

def changeToCenter(x, y):
    rx = math.floor((maxY - y) * unitPerMeter)
    ry = math.floor((x - startX) * unitPerMeter) 
    return [rx, ry] 

def changeXY(x, y):
    rx = round((maxY - y) * unitPerMeter, 4)
    ry = round((x - startX) * unitPerMeter, 4) 
    return [rx, ry] 

def getDes():
    mapX = 50
    mapY = 140
    exitDes = []
    for i in range(5, 45):
        exitDes.append([i, 0])
    for i in range(5, 45):
        exitDes.append([i, 139])
    exitPoint = [[25, 139], [25, 0]]
    peopleDes = []
    lList = []
    rList = []
    for i in range(1, 27):
        with open("data/#10011对流有奖励1/" + str(i) + ".txt") as f:
            fcsv = csv.reader(f, delimiter = ' ')
            r = next(fcsv)
            px, py = changeXY(float(r[0]), float(r[4]))
            if px < 6 or px > 44:
                continue
            if py < 70:
                lList.append([px, py])
            else:
                rList.append([px, py])
    peopleDes = lList + rList
    groupBound = len(lList)

    return mapX, mapY, [], exitDes, peopleDes, True, groupBound, exitPoint

if __name__ == '__main__':
    
    wall = [[startX, startY], [startX, maxY], [maxX, startY], [maxX, maxY]]
    
    fw = []
    for w in wall:
        fw.append(changeToCenter(w[0], w[1]))
    print(fw)
    exitL = [[1, 5], [1, 9], [15, 5], [15, 9]]
    fe = []
    for e in exitL:
        fe.append(changeToCenter(e[0], e[1]))
    print(fe)