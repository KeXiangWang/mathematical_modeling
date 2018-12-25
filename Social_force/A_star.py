import math

map_width = 0
map_height = 0


def test_a_star(model_map):
    astar = A_star(model_map, 10, 10, 35, 93)
    path = astar.get_path()
    print(path)


def distance(cur, end):
    return abs(cur.x - end.x) + abs(cur.y - end.y)
    # h_diagonal = min(abs(cur.x - end.x), abs(cur.y - end.y))
    # h_straight = (abs(cur.x - end.x) + abs(cur.y - end.y))
    # d = 1
    # d_2 = math.sqrt(2)
    # return d_2 * h_diagonal + d * (h_straight - 2 * h_diagonal)
    # return math.sqrt((cur.x - end.x) ** 2 + (cur.x - end.x) ** 2)


class Node(object):
    def __init__(self, father, x, y, end):
        if x < 0 or x >= map_height or y < 0 or y >= map_width:
            raise Exception('坐标错误')
        self.father = father
        self.x = x
        self.y = y
        if father is not None:
            self.G = father.G + 1 * math.sqrt((x - self.father.x) ** 2 + (y - self.father.y) ** 2)
            self.H = distance(self, end)
            self.F = self.G + self.H
        else:
            self.G = 0
            self.H = 0
            self.F = 0

    def reset_father(self, father, new_g):
        if father is not None:
            self.G = new_g
            self.F = self.G + self.H
        self.father = father


class A_star(object):
    def __init__(self, model_map, start_x, start_y, end_x, end_y):
        self.model_map = model_map
        self.map_height, self.map_width = self.model_map.shape
        global map_width, map_height
        map_width = self.map_width
        map_height = self.map_height
        self.orientation = []
        self.open_list = {}  # 开放列表（也就是有待探查的地点）
        self.close_list = {}  # 关闭列表  (已经探查过的地点和不可行走的地点)
        self.end = Node(None, end_x, end_y, None)
        self.start = Node(None, start_x, start_y, self.end)

    def mark_path(self, node):
        if node.father is None:
            return
        self.orientation.append([node.x - node.father.x, node.y - node.father.y])
        self.mark_path(node.father)

    def min_first_node(self):
        if len(self.open_list) == 0:
            raise Exception('路径不存在')
        _min = 9999999999999999
        _k = (self.start.x, self.start.y)
        for k, v in self.open_list.items():  # 以列表的形式遍历open_list字典
            if _min >= v.F:
                _min = v.F
                _k = k
        return self.open_list[_k]

    def add_adjacent_into_open(self, node):
        # 首先将该节点从开放列表移动到关闭列表之中
        self.open_list.pop((node.x, node.y))
        self.close_list[(node.x, node.y)] = node
        adjacent = []
        # 添加相邻节点的时候要注意边界
        try:  # 上
            adjacent.append(Node(node, node.x, node.y - 1, self.end))
        except Exception as err:
            pass
        try:  # 下
            adjacent.append(Node(node, node.x, node.y + 1, self.end))
        except Exception as err:
            pass
        try:  # 左
            adjacent.append(Node(node, node.x - 1, node.y, self.end))
        except Exception as err:
            pass
        try:  # 右
            adjacent.append(Node(node, node.x + 1, node.y, self.end))
        except Exception as err:
            pass
        try:  # 上
            adjacent.append(Node(node, node.x + 1, node.y - 1, self.end))
        except Exception as err:
            pass
        try:  # 下
            adjacent.append(Node(node, node.x - 1, node.y + 1, self.end))
        except Exception as err:
            pass
        try:  # 左
            adjacent.append(Node(node, node.x - 1, node.y - 1, self.end))
        except Exception as err:
            pass
        try:  # 右
            adjacent.append(Node(node, node.x + 1, node.y + 1, self.end))
        except Exception as err:
            pass
        for a in adjacent:  # 检查每一个相邻的点
            if (a.x, a.y) == (self.end.x, self.end.y):  # 如果是终点，结束
                new_g = node.G + 1
                self.end.reset_father(node, new_g)
                return True
            if (a.x, a.y) in self.close_list:  # 如果在close_list中,不去理他
                continue
            if (a.x, a.y) not in self.open_list:  # 如果不在open_list中，则添加进去
                self.open_list[(a.x, a.y)] = a
            else:  # 如果存在在open_list中，通过G值判断这个点是否更近
                exist_node = self.open_list[(a.x, a.y)]
                new_g = node.G + math.sqrt((a.x - node.x) ** 2 + (a.y - node.y) ** 2)
                if new_g < exist_node.G:
                    exist_node.reset_father(node, new_g)
        return False

    def find_the_path(self):
        self.open_list[(self.start.x, self.start.y)] = self.start

        the_node = self.start
        try:
            while not self.add_adjacent_into_open(the_node):
                the_node = self.min_first_node()
        except Exception as err:
            # 路径找不到
            print(err)
            return False
        return True

    def preset_map(self):
        for i in range(self.model_map.shape[0]):
            for j in range(self.model_map.shape[1]):
                if self.model_map[i][j] == 1:
                    block_node = Node(None, i, j, self.end)
                    self.close_list[(block_node.x, block_node.y)] = block_node

    def get_path(self):
        self.preset_map()
        if (self.start.x, self.start.y) in self.close_list:
            return "fuck!"
        if (self.end.x, self.end.y) in self.close_list:
            return "shit!"
        if self.find_the_path():
            self.mark_path(self.end)
        self.orientation.reverse()
        return self.orientation
