import math
import csv

unitPerMeter = 10
startX = 3.41
startY = 3.21
maxX = 12.64
maxY = 10.28

def changeToCenter(x, y):
    rx = math.floor((maxY - y) * unitPerMeter)
    ry = math.floor((x - startX) * unitPerMeter) 
    return [rx, ry] 

def changeXY(x, y):
    rx = round((maxY - y) * unitPerMeter, 4)
    ry = round((x - startX) * unitPerMeter, 4) 
    return [rx, ry] 

def getDes():
    mapX = 71
    mapY = 91
    deskDes = [[27, 39, 59, 65]]
    exitDes = []
    for i in range(28, 39):
        exitDes.append([i, 90])
    
    peopleDes = []
    for i in range(1, 27):
        with open("resources/采集数据1 - 副本/#00001横向障碍物-窄门-无奖励-1_v5/" + str(i) + ".txt") as f:
            fcsv = csv.reader(f, delimiter = ' ')
            r = next(fcsv)
            px, py = changeXY(float(r[0]), float(r[4]))
            peopleDes.append([px, py])

    return mapX, mapY, deskDes, exitDes, peopleDes

if __name__ == '__main__':
    desk = [[9.33, 7.5], [9.33, 6.32], [9.91, 6.32]]
    wall = [[3.41, 10.28], [3.41, 3.21], [12.46, 7.39], [12.46, 6.39]]
    fd = []
    for d in desk:
        fd.append(changeToCenter(d[0], d[1]))
    fw = []
    for w in wall:
        fw.append(changeToCenter(w[0], w[1]))