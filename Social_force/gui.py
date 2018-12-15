import social_force
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap
import numpy as np

class Gui(QWidget):
    def __init__(self, model_map, exit_list, people_list, wall_list):
        def setMap():
            self.mapSize = self.modelMap.shape
            self.sizePerPoint = min(500 / self.mapSize[0], 500 / self.mapSize[1])
            self.paintX0 = (500 - self.sizePerPoint * self.mapSize[0]) / 2 + self.startX0
            self.paintY0 = (500 - self.sizePerPoint * self.mapSize[1]) / 2 + self.startY0
        def initPeople():     
            self.peopleList = []       
            image = QPixmap()  
            image.load("resources/1.png") 
            for p in people_list:
                label = QLabel(self)
                px = p[1] * self.sizePerPoint + self.paintX0
                py = p[0] * self.sizePerPoint + self.paintY0
                label.setGeometry(px, py, self.sizePerPoint * self.peopleRadius * 2, self.sizePerPoint * self.peopleRadius * 2)
                label.setPixmap(image)
                label.setScaledContents(True)
                self.peopleList.append(label)
            self.arriveList = []

        super().__init__()
        self.startX0 = 270
        self.startY0 = 20
        self.peopleRadius = 3
        self.modelMap = model_map
        self.model = social_force.Model(model_map, exit_list, people_list, wall_list)
        setMap()
        initPeople()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateModel)
        self.time = 0
        self.timeInterval = 50
        self.runState = 0
        self.timerInterval = 0 # 50
        self.initUI()
        # self.timer.start(1000)

    def initUI(self):
        self.setGeometry(530, 220, 810, 540)
        self.setFixedSize(810, 540)
        self.setWindowTitle('mathematical modeling')

        self.timeLabel = QLabel(self)
        self.timeLabel.setGeometry(60, 60, 150, 70)
        self.timeLabel.setText('1.34')
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
        self.timeLabel.setText(str(self.time / 1000))
        pList, apList, aNum = self.model.update()
        for i in range(len(aNum)):
            ap = self.peopleList.pop(aNum[i])
            apx = apList[i][1] * self.sizePerPoint + self.paintX0
            apy = apList[i][0] * self.sizePerPoint + self.paintY0
            ap.move(apx, apy)
            # self.arriveList.append(ap)
        for i in range(len(pList)):
            px = pList[i][1] * self.sizePerPoint + self.paintX0
            py = pList[i][0] * self.sizePerPoint + self.paintY0
            self.peopleList[i].move(px, py)
        if (self.peopleList != [] and self.runState):
            self.timer.start(self.timerInterval)
        else:
            self.timer.stop()

    def paintEvent(self, event):
        def drawWall(painter):
            def oneWall(x, y, painter):
                dx = x * self.sizePerPoint + self.paintX0
                dy = y * self.sizePerPoint + self.paintY0
                painter.setBrush(Qt.black)
                painter.drawRect(dx, dy, self.sizePerPoint, self.sizePerPoint)

            painter.setPen(Qt.black)
            for i in range(self.mapSize[0]):
                for j in range(self.mapSize[1]):
                    if self.modelMap[i][j] == 1:
                        oneWall(j, i, painter)

        painter = QPainter()
        painter.begin(self)
        drawWall(painter)

    def step(self):
        if (self.runState != 1):
            self.timer.start(self.timerInterval)

    def run(self):
        sender = self.sender()
        if (sender.text() == "RUN"):
            sender.setText("PAUSE")
            self.runState = 1
            self.timer.start(self.timerInterval)
        else:
            sender.setText("RUN")
            self.runState = 0


if __name__ == '__main__':
    
    sizeX = 50
    sizeY = 50
    wallDescribe = [[24, 25, 1, 18]]
    exitDescribe = [[49, 25], [49, 26]]
    peopleDescribe = [[10, 4], [10, 11], [10, 18], [17, 4], [17, 11]]
    
    APP = QApplication(sys.argv)
    model_map, exit_list, people_list, wall_list = social_force.create_map_people_wall(sizeX, sizeY, wallDescribe, exitDescribe, peopleDescribe)
    ex = Gui(model_map, exit_list, people_list, wall_list)
    sys.exit(APP.exec_())
