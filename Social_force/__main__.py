import social_force
from gui import Gui
from PyQt5.QtWidgets import QApplication
import sys
import map
import convectionMap

if __name__ == "__main__":
    print("The start of the model")

    # sizeX = 100
    # sizeY = 100
    # wallDescribe = [[80, 81, 23, 80]]
    # exitDescribe = [[99, 25], [99, 26], [99, 27], [99, 28], [99, 29], [99, 30], [99, 31], [99, 32]]
    # peopleDescribe = [[76.9638, 45.6452],
    #                   [76.3448, 54.3215],
    #                   [65.4089, 53.5671],
    #                   [56.9491, 56.3963],
    #                   [58.1871, 63.1865],
    #                   [67.6786, 61.3004],
    #                   [73.4561, 60.3573],
    #                   [78.4082, 61.3004],
    #                   [75.9321, 69.4109],
    #                   [68.9166, 67.1475],
    #                   [58.3934, 69.9767],
    #                   [57.9808, 75.4466],
    #                   [57.5681, 80.162],
    #                   [67.885, 72.4287],
    #                   [68.9166, 76.9555],
    #                   [75.9321, 78.2758],
    #                   [66.0279, 82.2368],
    #                   [61.9012, 84.1229],
    #                   [68.0913, 87.1408],
    #                   [50.14, 90.1587],
    #                   [56.1237, 8.835],
    #                   [61.6948, 91.8562],
    #                   [68.7103, 90.1944],
    #                   [71.599, 90.9131],
    #                   [77.5828, 91.479],
    #                   [84.5983, 90.7245]
    #                   ]

    # model_map, exit_list, people_list, wall_list = social_force.create_map_people_wall(sizeX, sizeY, wallDescribe,
    #                                                                                    exitDescribe, peopleDescribe)

    thickness = 5
    sizeX, sizeY, wallDescribe, exitDescribe, peopleDescribe, mode, bound, exit_point = convectionMap.getDes()
    # sizeX, sizeY, wallDescribe, exitDescribe, peopleDescribe, mode, bound, exit_point = map.getDes()
    model_map, exit_list, people_list, wall_list = social_force.create_map_people_wall(sizeX, sizeY, wallDescribe,
                                                                                       exitDescribe, peopleDescribe,
                                                                                       thickness)

    APP = QApplication(sys.argv)
    ex = Gui(wallDescribe, model_map, exit_list, people_list, wall_list, "a_atar_map_name.npy", thickness, mode, bound, exit_point)
    sys.exit(APP.exec_())

    # model = social_force.Model(wallDescribe, model_map, exit_list, people_list, wall_list, "a_atar_map_name.npy",
                            #    thickness, encounter_mode=True)
    # model.a_star(people_list[3], exitDescribe[0])

    # for i in range(20):
    #     people_list, people_arrive_list, _ = model.update()
    #     print("time:", i, people_list.shape)
