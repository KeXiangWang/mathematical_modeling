import social_force
from gui import Gui
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    print("The start of the model")

    sizeX = 50
    sizeY = 50
    wallDescribe = [[24, 25, 1, 18]]
    exitDescribe = [[49, 25], [49, 26], [49, 27], [49, 28], [49, 29], [49, 30], [49, 31], [49, 32]]
    peopleDescribe = [[10, 4], [10, 11], [10, 18], [17, 4], [17, 11]]
    model_map, exit_list, people_list, wall_list = social_force.create_map_people_wall(sizeX, sizeY, wallDescribe,
                                                                                       exitDescribe, peopleDescribe)

    APP = QApplication(sys.argv)
    ex = Gui(model_map, exit_list, people_list, wall_list)
    sys.exit(APP.exec_())

    # model = social_force.Model(model_map, exit_list, people_list, wall_list)
    #
    # for i in range(20):
    #     people_list, people_arrive_list, _ = model.update()
    #     print("time:", i, people_list.shape)
