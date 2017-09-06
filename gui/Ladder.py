import random
from const import Const


class Ladder:
    def __init__(self, x: int):
        self.x = x
        # self.y = x + 1
        self.y = x + 3
        self.matrix = [[0 for col in range(self.x)] for row in range(self.y)]
        self.points = [[[0, 0] for col in range(self.x)] for row in range(self.y)]

        temp = list(range(1, self.y - 1))
        random.shuffle(temp)
        lag_count = int(len(temp) / 3)

        occupied = []
        for i in range(0, self.x - 1):
            if i == 0:
                for j in temp[0:lag_count]:
                    self.matrix[j][i] = 1
                    self.matrix[j][i + 1] = 1
                occupied.append(temp[0:lag_count])
            else:
                item = []
                flat_list = [item for sublist in occupied for item in sublist]
                item = list(set(temp) - set(flat_list))
                random.shuffle(item)
                for j in item[0:lag_count]:
                    self.matrix[j][i] = 1
                    self.matrix[j][i + 1] = 1
                occupied.append(item[0:lag_count])
                if len(occupied) > 2:
                    del occupied[0]


        space_x = (Const.WIDTH - Const.MARGIN * 2) / (self.x - 1)
        space_y = (Const.HEIGHT - Const.MARGIN * 2) / (self.y - 1)
        for i in range(0, self.x):
            cur_x = Const.MARGIN if i == 0 else cur_x + space_x
            for j in range(0, self.y):
                cur_y = Const.MARGIN if j == 0 else cur_y + space_y
                self.points[j][i] = [cur_x, cur_y]
