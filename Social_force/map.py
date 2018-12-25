import math
import csv

unitPerMeter = 10
startX = 3.66 - 0.5
startY = 3.689 - 0.5
maxX = 11.96 + 0.5
maxY = 9.97 + 0.5

def changeToCenter(x, y):
    rx = math.floor((maxY - y) * unitPerMeter)
    ry = math.floor((x - startX) * unitPerMeter) 
    return [rx, ry] 

def changeXY(x, y):
    rx = round((maxY - y) * unitPerMeter, 4)
    ry = round((x - startX) * unitPerMeter, 4) 
    return [rx, ry] 

def getDes():
    mapX = 73
    mapY = 94
    deskDes = [[29, 35, 61, 73]]
    exitDes = []
    for i in range(32, 39):
        exitDes.append([i, 93])
    peopleDes = []
    for i in range(1, 27):
        with open("data/#00001横向障碍物-窄门-无奖励-1_v5/" + str(i) + ".txt") as f:
            fcsv = csv.reader(f, delimiter = ' ')
            r = next(fcsv)
            px, py = changeXY(float(r[0]), float(r[4]))
            if px < 7 or px > 73 - 7:
                continue
            elif py < 7 or py > 94 - 7:
                continue
            peopleDes.append([px, py])

    return mapX, mapY, deskDes, exitDes, peopleDes, False, 0, []


if __name__ == '__main__':
    desk = [[9.308, 7.481], [9.308, 7.481 - 0.572], [9.308 + 1.17, 7.481], [9.308 + 1.17, 7.481 - 0.572]]
    wall = [[startX, startY], [startX, maxY], [maxX, startY], [maxX, maxY]]
    fd = []
    for d in desk:
        fd.append(changeToCenter(d[0], d[1]))
    fw = []
    for w in wall:
        fw.append(changeToCenter(w[0], w[1]))
    print(fd, fw)
    print(changeToCenter(11.96, 7.234))