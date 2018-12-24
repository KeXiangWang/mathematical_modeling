import numpy as np
import A_star
import math
import os
from tqdm import tqdm


def create_map_people_wall(sizeX, sizeY, wall_describe, exit_describe, people_describe, thickness):
    model_map = np.ones(shape=(sizeX, sizeY))
    model_map[thickness:(sizeX - thickness), thickness:(sizeY - thickness)] = 0  # wall
    for w in wall_describe:
        model_map[w[0]:w[1], w[2]:w[3]] = 1
    for x, y in exit_describe:
        for i in range(thickness):
            model_map[x][y - i] = 0
    if people_describe:
        # random
        print('wrong')
    # people_list = []
    # for i in range(5):
    #     p = [i * 5 + 25, 50]
    #     if model_map[math.floor(p[0])][math.floor(p[1])] == 1:
    #         continue
    #     people_list.append(p)
    wall_list = []
    for i in range(model_map.shape[0]):
        for j in range(model_map.shape[1]):
            if model_map[i][j] == 1:
                wall_list.append([i, j])
    model_map = np.array(model_map)
    exit_list = np.array(exit_describe)
    people_list = np.array(people_describe, dtype=np.double)
    wall_list = np.array(wall_list)
    return [model_map, exit_list, people_list, wall_list]


def distance(people1, people2):
    return math.sqrt((people1[0] - people2[0]) ** 2 + (people1[1] - people2[1]) ** 2)


class Model:
    def __init__(self, wall_describe, model_map, exit_list, people_list, wall_list, a_star_map_name, thickness):
        # print(exit_list)
        self.wall_describe = wall_describe
        self.model_map = model_map
        self.exit_list = exit_list
        self.people_list = people_list
        self.wall_list = wall_list
        self.velocity_list = np.zeros(shape=(len(people_list), 2))
        self.map_height, self.map_width = self.model_map.shape
        # constant
        self.const_number = 10
        self.velocity_i_0 = 0.8 * self.const_number  # units of measurement: dm/s
        self.A_i = 2000  # units of measurement: N
        self.B_i = 0.08  # units of measurement: m
        self.k = 1.2 * 10 ** 5  # units of measurement: kg(s**-2)
        self.k_body_effect_coefficient = 2.4 * 10 ** 5 / self.const_number  # units of measurement: kg(dm**-1)(s**-1)
        self.radius = 0.2 * self.const_number  # units of measurement: dm
        self.radius_wall = 0.05 * self.const_number  # units of measurement: dm
        self.t_gap = 0.05  # units of measurement: s
        self.mass = 80  # units of measurement: kg
        self.velocity_list[0:len(people_list), 0:2] = 0
        # parameters for control
        self.print_n = 0
        self.easy_model = 1
        # a_star_map preset
        if os.path.isfile(a_star_map_name):
            self.a_star_map = np.load(a_star_map_name)
            print("Loaded the preset a_star_map")
        else:
            self.a_star_map = np.zeros(shape=(self.map_height, self.map_width, 2))
            # a = np.zeros(shape=(self.map_height, self.map_width)) # for observing
            for x in tqdm(range(self.map_height)):
                for y in range(self.map_width):
                    if model_map[x][y] == 1:
                        continue
                    astar = A_star.A_star(self.model_map, x, y, self.exit_list[4][0], self.exit_list[4][1])
                    path = np.array(astar.get_path())
                    self.a_star_map[x][y] = path[0]
                    # a[x][y] = path[0][0]*10 + path[0][1]
            np.save(a_star_map_name, self.a_star_map)
            print("The progress of presetting a_star_map finished! ")

    def a_star(self, start_point, end_point):
        start_x = math.floor(start_point[0])
        start_y = math.floor(start_point[1])
        return self.a_star_map[start_x, start_y]

    def accelerate(self, i, e):
        ca1 = self.mass * (
                self.velocity_i_0 * e - self.velocity_list[i]) / self.t_gap / self.const_number
        ca2 = [0, 0]
        for j in range(len(self.people_list)):
            if i != j:
                ca2 = ca2 + self.force_people_people(i, j)
        ca3 = [0, 0]
        current_wall_list = self.get_wall(i)
        # print(current_wall_list)
        for w in current_wall_list:
            # for w in range(len(self.wall_list)):
            c = self.force_people_wall(i, w)
            ca3 = ca3 + c
        if self.print_n:
            print("ca1: ", ca1, "ca2: ", ca2, "ca3: ", ca3)
        return (ca1 + ca2 + ca3) / self.mass

    def get_wall(self, location):
        current = self.people_list[location]
        walls = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i + j) == 1:
                    target = np.ones(shape=2, dtype=np.int32)
                    target[0] = math.floor((current[0]) if i == 0 else 0 if i == -1 else self.map_height - 1)
                    target[1] = math.floor((current[1]) if j == 0 else 0 if j == -1 else self.map_width - 1)
                    if self.model_map[target[0]][target[1]] == 1:
                        walls.append(target)
        for w in self.wall_describe:
            choice = np.ones(shape=2, dtype=np.int32)
            choice[0] = math.floor(w[0] if current[0] <= w[0] else current[0] if current[0] < w[1] else w[1])
            choice[1] = math.floor(w[2] if current[1] <= w[2] else current[1] if current[1] < w[3] else w[3])
            walls.append(choice)
        return walls

    def force_people_people(self, i, j):
        r_ij = (self.radius + self.radius) / self.const_number
        d_ij = distance(self.people_list[i], self.people_list[j]) / self.const_number
        ca1 = self.A_i * math.exp((r_ij - d_ij) / self.B_i)
        g = 0
        ca2 = self.k * g
        n_ij = (self.people_list[i] - self.people_list[j]) / self.const_number / d_ij
        ca3 = (ca1 + ca2) * n_ij
        t_ij = [-n_ij[1], n_ij[0]]
        delta_v_ji = (self.velocity_list[j] - self.velocity_list[i]) * t_ij
        ca4 = self.k_body_effect_coefficient * g * delta_v_ji * t_ij
        return ca3 + ca4

    def force_people_wall(self, i, w):
        r_iw = (self.radius + self.radius_wall) / self.const_number
        d_iw = distance(self.people_list[i], w) / self.const_number
        # d_iw = distance(self.people_list[i], self.wall_list[w]) / self.const_number
        ca1 = self.A_i * math.exp((r_iw - d_iw) / self.B_i)
        g = 0
        ca2 = self.k * g
        # n_iw = (self.people_list[i] - self.wall_list[w]) / self.const_number / d_iw
        n_iw = (self.people_list[i] - w) / self.const_number / d_iw
        # print(n_iw, w)
        ca3 = (ca1 + ca2) * n_iw
        t_iw = [-n_iw[1], n_iw[0]]
        delta_v_wi = (0 - self.velocity_list[i]) * t_iw
        ca4 = self.k_body_effect_coefficient * g * delta_v_wi * (
                self.velocity_list[i][0] * t_iw[0] + self.velocity_list[i][1] * t_iw[1]) * t_iw
        # if abs(ca3[0]) > 1:
        #     print("ca1 ", ca1, "ca2 ", ca2, "ca3 ", ca3, "n  ", n_iw, "d ", d_iw)
        return ca3 + ca4

    # def touch_wall(self, loc):
    #     for x, y in self.temp_wall_list:
    #         if math.floor(loc[0]) == x and math.floor(loc[1]) == y:
    #             return [math.floor(loc[0]) == x, math.floor(loc[1]) == y]
    #     return [False, False]

    def update(self):
        arrive_list = []
        new_velocity_list = []
        new_people_list = []
        for i in range(len(self.people_list)):
            min_length = 99999999999
            if self.easy_model:
                e = self.a_star(self.people_list[i], self.exit_list[4])
            else:
                e = [0, 0]
                for j in range(len(self.exit_list)):
                    d = self.a_star(self.people_list[i], self.exit_list[j])
                    if len(d) < min_length:
                        min_length = len(d)
                        e = d
            a = self.accelerate(i, e) * self.const_number
            a[0] = a[0] if abs(a[0]) < 100 else np.sign(a[0]) * 100
            a[1] = a[1] if abs(a[1]) < 100 else np.sign(a[1]) * 100
            print(a)
            print_n = self.print_n  # and i == 3
            if print_n:
                print(i, "th:", " accelerate:", a, "e: ", e)
                print("old_p: ", self.people_list[i])
                print("old_v: ", self.velocity_list[i])

            new_people_list.append(self.people_list[i] + self.t_gap * self.velocity_list[
                i] + 0.5 * a * self.t_gap ** 2)  # v0t + 1/2 * a * t**2
            # touch_x, touch_y = self.touch_wall(new_people_list[i])
            # if touch_x:
            #     new_people_list[i][0] = self.people_list[i][0]
            # if touch_y:
            #     new_people_list[i][1] = self.people_list[i][1]

            if print_n:
                print("new_p: ", new_people_list[i])
            new_velocity_list.append(self.t_gap * a + self.velocity_list[i])  # at + v0
            if print_n:
                print("new_v: ", new_velocity_list[i])
            for x, y in self.exit_list:
                if x == math.floor(new_people_list[i][0]) and y == math.floor(new_people_list[i][1]):
                    print([math.floor(new_people_list[i][0]), math.floor(new_people_list[i][1])])
                    arrive_list.append(i)
        arrive_people_list = self.people_list[arrive_list]
        new_people_list = np.array(new_people_list)
        new_velocity_list = np.array(new_velocity_list)
        self.people_list = np.delete(new_people_list, arrive_list, axis=0)
        self.velocity_list = np.delete(new_velocity_list, arrive_list, axis=0)
        # self.velocity_list = np.delete(self.velocity_list, arrive_list, axis=0)
        return self.people_list, arrive_people_list, arrive_list
