import tkinter as tk
import math
import matplotlib.pyplot as plt
import numpy as np
from oval import Oval
INIT_WIDTH = 3
INIT_HEIGHT = 2
INIT_AREASIZE = 5
MAGNIFICATION = 10000
OVAL_QUANTITY_LIMIT = 100
IS_MOVING = False   # 楕円が移動中かどうか(移動中: True, 楕円作っている: False)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('esquisse')
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        # キャンバスの初期化
        self.canvas = tk.Canvas(self, bg='white', width=1300, height=900)

        #　四角形左上の座標（300,100）右下の座標（840,640）左下（300,640）右上（840,100）面積540＊540=291000
        self.canvas.create_rectangle(300, 100, 840, 640, outline='black', fill='', width=1)

        # 面積のテキストボックス
        self.areasize_lbl = tk.Label(text='面積')
        self.areasize_lbl.place(x=10, y=0)
        self.areasize_box = tk.Entry(width=10)
        self.areasize_box.place(x=50, y=0)
        self.areasize_box.insert(tk.END, INIT_AREASIZE)
        self.areasize = self.areasize_box.get()

        # 縦横比のテキストボックス
        # 縦
        self.height_relative_lbl = tk.Label(text='縦')
        self.height_relative_lbl.place(x=150, y=0)
        self.height_relative_box = tk.Entry(width=10)
        self.height_relative_box.place(x=190, y=0)
        self.height_relative_box.insert(tk.END, INIT_HEIGHT)
        self.height_relative = self.height_relative_box.get()

        # 横
        self.width_relative_lbl = tk.Label(text='横')
        self.width_relative_lbl.place(x=290, y=0)
        self.width_relative_box = tk.Entry(width=10)
        self.width_relative_box.place(x=330, y=0)
        self.width_relative_box.insert(tk.END, INIT_WIDTH)
        self.width_relative = self.width_relative_box.get()
        
        #　更新ボタン
        self.areasize_update_button = tk.Button(self, text='更新', command=self.update_areasize)
        self.areasize_update_button.place(x=430, y=0)

        #　移動ボタン
        self.move_button = tk.Button(self, text='移動', command=self.press_move)
        self.move_button.place(x=470, y=0)
        
        #　楕円ボタン
        self.oval_button = tk.Button(self, text='楕円', command=self.press_oval)
        self.oval_button.place(x=510, y=0)

        #　チェックボタン
        self.check_button = tk.Button(self, text='判定', command=self.check_oval)
        self.check_button.place(x=550, y=0)

        #　表ボタン
        self.check_button = tk.Button(self, text='表', command=self.create_graph)
        self.check_button.place(x=590, y=0)

        self.canvas.grid(row=1, column=0, columnspan=4)
        #　楕円リスト
        self.oval = []
        #　座標ごとの一番近い楕円リスト
        self.data = []
        #　OvalクラスとAppクラスのキャンバスの統合
        Oval.canvas = self.canvas

    #　面積，縦横比の値を更新   
    def update_areasize(self):
        self.areasize = self.areasize_box.get()
        self.height_relative = self.height_relative_box.get()
        self.width_relative = self.width_relative_box.get()

    # 「楕円」ボタンが押された時
    def press_oval(self):
        global IS_MOVING
        IS_MOVING = False
        self.canvas.bind(sequence='<1>', func=self.create_oval)

    # 「移動」ボタンが押された時
    def press_move(self):
        global IS_MOVING
        IS_MOVING = True
        for o in self.oval:
            if o.deleted == False:
                o.bind_move()

    def create_oval(self, event):
        center_x = event.x
        center_y = event.y
        # areasize, width_relative, height_relativeの値をInt型に変換
        try:
            global IS_MOVING
            if IS_MOVING == False:
                size = float(self.areasize) * MAGNIFICATION
                w = float(self.width_relative)
                h = float(self.height_relative)
                width  = ((size * h) / w) ** 0.5  # 楕円の横の長さ
                height = ((size * w) / h) ** 0.5  # 楕円の縦の長さ
                dist_x = ((size * w) / (4 * h)) ** 0.5    # 中心から楕円の端までの距離(x方向)
                dist_y = ((size * h) / (4 * w)) ** 0.5    # 中心から楕円の端までの距離(y方向)
                self.x = center_x+1
                self.y = center_y+1
                ov = Oval(center_x, center_y, center_x-dist_x, center_y-dist_y, center_x+dist_x, center_y+dist_y, size, width, height, self.x, self.y)
                self.oval.append(ov)
            self.canvas.delete('error_message')
        except ValueError:
            self.canvas.create_text(100, 100, text='数値を入力してください', fill='red', tags='error_message')
    
        
if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()