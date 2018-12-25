import social_force
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QPixmap, QPainterPath, QPolygonF, QPen  # QColor, QBrush
# import numpy as np
import sys
import map


class Gui(QWidget):
    def __init__(self, wallDescribe, model_map, exit_list, people_list, wall_list, a_star_map_name, thickness, mode, bound, exit_point):
        def setMap():
            self.mapSize = self.modelMap.shape
            self.sizePerPoint = min(500 / self.mapSize[0], 500 / self.mapSize[1])
            self.paintX0 = (500 - self.sizePerPoint * self.mapSize[1]) / 2 + self.startX0
            self.paintY0 = (500 - self.sizePerPoint * self.mapSize[0]) / 2 + self.startY0
            print(self.paintX0, self.paintY0)

        def initPeople():
            self.peopleList = []
            image = QPixmap()
            image.load("1.png")
            r = self.peopleRadius * self.sizePerPoint
            for i in range(len(people_list)):
                p = people_list[i]
                if i < bound:
                    pType = 0
                else:
                    pType = 1
                label = QLabel(self)
                px = (p[1] - self.peopleRadius) * self.sizePerPoint + self.paintX0
                py = (p[0] - self.peopleRadius) * self.sizePerPoint + self.paintY0
                label.setGeometry(px, py, self.sizePerPoint * self.peopleRadius * 2,
                                  self.sizePerPoint * self.peopleRadius * 2)
                label.setPixmap(image)
                label.setScaledContents(True)
                path = QPolygonF()
                path << QPointF(px + r, py + r)
                self.peopleList.append([label, path, pType])
            self.arriveList = []

        super().__init__()
        self.startX0 = 270
        self.startY0 = 20
        self.peopleRadius = 2
        self.modelMap = model_map
        self.model = social_force.Model(wallDescribe, model_map, exit_list, people_list, wall_list, a_star_map_name, thickness, mode, bound, exit_point)
        setMap()
        initPeople()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateModel)
        self.time = 0
        self.timeInterval = 50
        self.runState = 0
        self.timerInterval = 5  # 50
        self.initUI()
        # self.timer.start(1000)

    def initUI(self):
        self.setGeometry(530, 220, 810, 540)
        self.setFixedSize(810, 540)
        self.setWindowTitle('mathematical modeling')

        self.timeLabel = QLabel(self)
        self.timeLabel.setGeometry(60, 60, 150, 70)
        self.timeLabel.setText('0')
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet("QLabel{background:white;font:20pt 'times new roman'}")
        self.stepButton = QPushButton('STEP', self)
        self.stepButton.setGeometry(65, 185, 140, 65)
        self.stepButton.setStyleSheet("QPushButton{font:18pt 'times new roman'}")
        self.stepButton.clicked.connect(self.step)
        self.stepButton = QPushButton('RUN', self)
        self.stepButton.setGeometry(65, 275, 140, 65)
        self.stepButton.setStyleSheet("QPushButton{font:18pt 'times new roman'}")
        self.stepButton.clicked.connect(self.run)
        self.show()

    def updateModel(self):
        self.time += self.timeInterval
        self.timeLabel.setText('%.3f' % (self.time / 1000))
        pList, apList, aNum = self.model.update()
        r = self.peopleRadius * self.sizePerPoint
        for i in range(len(aNum)):
            ap = self.peopleList.pop(aNum[i])
            apx = (apList[i][1] - self.peopleRadius) * self.sizePerPoint + self.paintX0
            apy = (apList[i][0] - self.peopleRadius) * self.sizePerPoint + self.paintY0
            ap[0].move(apx, apy)
            ap[1] << QPointF(apx + r, apy + r)
            self.arriveList.append(ap)
        for i in range(len(pList)):
            px = (pList[i][1] - self.peopleRadius) * self.sizePerPoint + self.paintX0
            py = (pList[i][0] - self.peopleRadius) * self.sizePerPoint + self.paintY0
            self.peopleList[i][0].move(px, py)
            self.peopleList[i][1] << QPointF(px + r, py + r)
        if self.peopleList != [] and self.runState:
            self.timer.start(self.timerInterval)
        else:
            self.timer.stop()

    def paintEvent(self, event):
        def drawWall(painter):
            def oneWall(x, y, painter):
                dx = x * self.sizePerPoint + self.paintX0
                dy = y * self.sizePerPoint + self.paintY0
                painter.setPen(Qt.black)
                painter.setBrush(Qt.black)
                painter.drawRect(dx, dy, self.sizePerPoint, self.sizePerPoint)

            for i in range(self.mapSize[0]):
                for j in range(self.mapSize[1]):
                    if self.modelMap[i][j] == 1:
                        oneWall(j, i, painter)

        def drawPath(painter):
            painter.setBrush(False)
            for pInf in self.peopleList:
                path = QPainterPath()
                p = pInf[1]
                path.addPolygon(p)
                if pInf[2] == 1:
                    painter.setPen(QPen(Qt.blue, 1))
                else:
                    painter.setPen(QPen(Qt.red, 1))
                painter.drawPath(path)
            for pInf in self.arriveList:
                path = QPainterPath()
                p = pInf[1]
                path.addPolygon(p)
                if pInf[2] == 1:
                    painter.setPen(QPen(Qt.blue, 1))
                else:
                    painter.setPen(QPen(Qt.red, 1))
                painter.drawPath(path)

        painter = QPainter()
        painter.begin(self)
        drawWall(painter)
        drawPath(painter)

    def step(self):
        if self.runState != 1:
            self.timer.start(self.timerInterval)

    def run(self):
        sender = self.sender()
        if sender.text() == "RUN":
            sender.setText("PAUSE")
            self.runState = 1
            self.timer.start(self.timerInterval)
        else:
            sender.setText("RUN")
            self.runState = 0
            self.timer.stop()


if __name__ == '__main__':
    sizeX, sizeY, wallDescribe, exitDescribe, peopleDescribe = map.getDes()
    model_map, exit_list, people_list, wall_list = social_force.create_map_people_wall(sizeX, sizeY, wallDescribe,
                                                                                       exitDescribe, peopleDescribe, 5)

    APP = QApplication(sys.argv)
    ex = Gui(wallDescribe, model_map, exit_list, people_list, wall_list, "a_atar_map_name.npy", 5)
    sys.exit(APP.exec_())
