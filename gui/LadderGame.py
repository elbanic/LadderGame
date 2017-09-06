from tkinter import *
from gui.Ladder import Ladder
from const import Const
import random
import time
import math


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Ladder Game")
        self.__start_loc = []

        self.popup = PopupWindow(self.master)
        self.master.wait_window(self.popup.top)

        self.label = Label(master, text="This is Ladder Game!")
        self.label.pack()

        self.canvas = Canvas(master, width=Const.WIDTH, height=Const.HEIGHT)
        self.canvas.pack()

        self.close_button = Button(master, text="Start", command=self.start)
        self.close_button.pack()

        self.start_button = Button(master, text="Close", command=master.quit)
        self.start_button.pack()

        count = max(min(8, int(self.popup.value)), 2)
        self.ladder = Ladder(count)
        self.draw_ladder()

    def draw_ladder(self):
        space_x = (Const.WIDTH - Const.MARGIN * 2) / (self.ladder.x - 1)
        space_y = (Const.HEIGHT - Const.MARGIN * 2) / (self.ladder.y - 2)

        x = self.ladder.x
        y = self.ladder.y
        mat = self.ladder.matrix
        pt_mat = self.ladder.points
        for i in range(0, x):
            pt_mat[0][i]
            self.canvas.create_text(pt_mat[0][i][0], pt_mat[0][i][1] - 10, fill="darkblue", font="Times 15 italic bold",
                                    text=str(i + 1))
            self.canvas.create_line(pt_mat[0][i][0], pt_mat[0][i][1], pt_mat[y - 1][i][0], pt_mat[y - 1][i][1],
                                    fill="#476042", width=3)
            for j in range(1, y - 1):
                if mat[j][i] == 1 and i != x - 1 and mat[j][i + 1] == 1:
                    self.canvas.create_line(pt_mat[j][i][0], pt_mat[j][i][1], pt_mat[j][i + 1][0], pt_mat[j][i][1],
                                            fill="#476042", width=3)

        winner = random.randrange(0, x)
        self.canvas.create_text(pt_mat[0][winner][0], pt_mat[y - 1][winner][1] + 10, fill="darkblue",
                                font="Times 15 italic bold", text=u'당첨!')

    def start(self):
        for i in range(0, self.ladder.x):
            self.draw_path(i, Const.COLOR_LIST[i])

    def draw_path(self, i, color):
        mat = self.ladder.matrix
        points = self.ladder.points
        mat_x = i
        mat_y = 1
        cur_pt = points[0][i]
        next_pt = points[1][i]
        virtical = False
        while next_pt[1] < points[len(points) - 1][0][1]:
            self.animation(cur_pt, next_pt, color)
            if virtical is False \
                    and mat[mat_y][mat_x] == 1 \
                    and mat_x != self.ladder.x - 1 \
                    and mat[mat_y][mat_x + 1] == 1:
                mat_x = mat_x + 1
                virtical = True
            elif virtical is False \
                    and mat[mat_y][mat_x] == 1 \
                    and mat_x != self.ladder.x + 1 \
                    and mat[mat_y][mat_x - 1] == 1:
                mat_x = mat_x - 1
                virtical = True
            else:
                mat_y = mat_y + 1
                virtical = False
            cur_pt = next_pt
            next_pt = points[mat_y][mat_x]
        self.animation(cur_pt, next_pt, color)

    def animation(self, cur_pt, next_pt, color):
        interval = math.sqrt(
            math.pow(next_pt[0] - cur_pt[0], 2) + math.pow(next_pt[1] - cur_pt[1], 2)) / Const.INTERVAL_COUNT
        for i in range(0, Const.INTERVAL_COUNT):
            time.sleep(0.05)
            angle = math.degrees(math.atan2(next_pt[1] - cur_pt[1], next_pt[0] - cur_pt[0]))
            dx = (math.cos(math.radians(angle)) if angle != 90 else 0) * interval
            dy = math.sin(math.radians(angle)) * interval
            temp_x = cur_pt[0] if i == 0 else temp_x + dx
            temp_y = cur_pt[1] if i == 0 else temp_y + dy
            self.canvas.create_line(cur_pt[0], cur_pt[1], temp_x, temp_y, fill=color, width=3)
            self.canvas.update()
        self.canvas.create_line(cur_pt[0], cur_pt[1], next_pt[0], next_pt[1], fill=color, width=3)


class PopupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.l = Label(top, text="Input the Number of People")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()
