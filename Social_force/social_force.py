import numpy as np
import A_star
import math


def create_map_people_wall(sizeX, sizeY, wall_describe, exit_describe, people_describe):
    model_map = np.ones(shape=(sizeX, sizeY))
    model_map[1:(sizeX-1), 1:(sizeY-1)] = 0  # wall
    # a = np.random.randint(0, 50, size=(1, 2))
    # model_map[a] = 1  # random table
    for w in wall_describe:
        model_map[w[0]:w[1], w[2]:w[3]] = 1

    # model_map[100, 1:160] = 1
    # exit_list = [[199, 100], [199, 101]]
    for x, y in exit_describe:
        model_map[x][y] = 0
    if people_describe == []:
        # random
        print('wrong')
    # people_list = []
    # for i in range(5):
    #     p = [i * 5 + 25, 50]
    #     if model_map[round(p[0])][round(p[1])] == 1:
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
    def __init__(self, model_map, exit_list, people_list, wall_list):
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
        self.B_i = 0.08 * self.const_number  # units of measurement: dm
        self.k = 1.2 * 10 ** 5  # units of measurement: kg(s**-2)
        self.k_body_effect_coefficient = 2.4 * 10 ** 5 / self.const_number  # units of measurement: kg(dm**-1)(s**-1)
        self.radius = 0.3 * self.const_number  # units of measurement: dm
        self.t_gap = 0.05  # units of measurement: s
        self.mass = 80  # units of measurement: kg
        self.velocity_list[0:len(people_list), 0:2] = self.velocity_i_0

    def a_star(self, start_point, end_point):
        start_x = round(start_point[0])
        start_y = round(start_point[1])
        astar = A_star.A_star(self.model_map, start_x, start_y, end_point[0], end_point[1])
        path = np.array(astar.get_path())
        # print(path)
        return path[0]

    def accelerate(self, i, e):
        ca1 = self.mass * (
                self.velocity_i_0 * e - self.velocity_list[i]) / self.t_gap
        ca2 = [0, 0]
        for j in range(len(self.people_list)):
            if i != j:
                ca2 = ca2 + self.force_people_people(i, j)
        ca3 = [0, 0]
        for w in range(len(self.wall_list)):
            ca3 = ca3 + self.force_people_wall(i, w)
        return (ca1 + ca2 + ca3) / self.mass

    def force_people_people(self, i, j):
        r_ij = self.radius + self.radius
        d_ij = distance(self.people_list[i], self.people_list[j])
        ca1 = self.A_i * math.exp(r_ij - d_ij / self.B_i)
        g = 0 if (d_ij > r_ij) else (r_ij - d_ij)
        ca2 = self.k * g
        n_ij = (self.people_list[i] - self.people_list[j]) / d_ij
        ca3 = (ca1 + ca2) * n_ij
        t_ij = [-n_ij[1], n_ij[0]]
        delta_v_ji = (self.velocity_list[j] - self.velocity_list[i]) * t_ij
        ca4 = self.k_body_effect_coefficient * g * delta_v_ji * t_ij
        return ca3 + ca4

    def force_people_wall(self, i, w):
        r_iw = self.radius + 0
        d_iw = distance(self.people_list[i], self.wall_list[w])
        ca1 = self.A_i * math.exp(r_iw - d_iw / self.B_i)
        g = 0 if (d_iw > r_iw) else (r_iw - d_iw)
        ca2 = self.k * g
        n_iw = (self.people_list[i] - self.wall_list[w]) / d_iw
        ca3 = (ca1 + ca2) * n_iw
        t_iw = [-n_iw[1], n_iw[0]]
        delta_v_wi = (0 - self.velocity_list[i]) * t_iw
        ca4 = self.k_body_effect_coefficient * g * delta_v_wi * (
                self.velocity_list[i][0] * t_iw[0] + self.velocity_list[i][1] * t_iw[1]) * t_iw
        return ca3 + ca4

    def update(self):
        arrive_list = []
        new_velocity_list = []
        new_people_list = []
        for i in range(len(self.people_list)):
            min_length = 99999999999
            e = [0, 0]
            # print(i)
            for j in range(len(self.exit_list)):
                d = self.a_star(self.people_list[i], self.exit_list[j])
                if len(d) < min_length:
                    min_length = len(d)
                    e = d
            a = self.accelerate(i, e)
            print("a: ", a)
            print("old_p: ", self.people_list[i])
            new_people_list.append(self.people_list[i] + self.t_gap * self.velocity_list[
                i] + 0.5 * a * self.t_gap ** 2)  # v0t + 1/2 * a * t**2
            print("new_p: ", new_people_list[i])
            new_velocity_list.append(self.t_gap * a + self.velocity_list[i])  # at + v0
            if [round(new_people_list[i][0]), round(new_people_list[i][1])] in self.exit_list:
                arrive_list.append(i)
        arrive_people_list = self.people_list[arrive_list]
        new_people_list = np.array(new_people_list)
        new_velocity_list = np.array(new_velocity_list)
        self.people_list = np.delete(new_people_list, arrive_list, axis=0)
        self.velocity_list = np.delete(new_velocity_list, arrive_list, axis=0)
        return self.people_list, arrive_people_list, arrive_list
