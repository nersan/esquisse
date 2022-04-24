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
    
    # 「判定」ボタンが押された時 左上から右へ、その後下へ
    def check_oval(self):
        idx = None
        # dx=[310,330,350,370,390,410,430,450,470,490,510,530,550,570,590,610,630,650,670,690,710,730,750,770,790,810,830]
        # dy=[110,130,150,170,190,210,230,250,270,290,310,330,350,370,390,410,430,450,470,490,510,530,550,570,590,610,630]
        dx=[330,390,450,510,570,630,690,750,810]
        dy=[130,190,250,310,370,430,490,550,610]
        for a in range(len(dy)):
            d = []
            for b in range(len(dx)):
                mini = float('inf')
                X = dx[b]
                Y = dy[a]  
                for i in range(len(self.oval)):
                    o = self.oval[i]
                    # 楕円の端と座標との距離で計算
                    if o.start_x < X <o.end_x and o.end_y < Y < o.start_y:  #楕円の中にある
                        dis = math.sqrt((X-o.center_x)**2+(Y-o.center_y)**2)

                    elif X < o.start_x and Y < o.end_y: #右上 
                        dis = math.sqrt((X-o.start_x)**2+(Y-o.end_y)**2)

                    elif X < o.start_x and o.end_y < Y < o.start_y: #右
                        dis = math.fabs(o.start_x-X)

                    elif X < o.start_x and Y > o.start_y:   #右下
                        dis = math.sqrt((X-o.start_x)**2+(Y-o.start_y)**2)

                    elif o.start_x < X < o.end_x and o.start_y < Y:#下
                        dis = math.fabs(Y-o.start_y)

                    elif X > o.end_x and Y > o.start_y: #左下 
                        dis = math.sqrt((X-o.end_x)**2+(Y-o.start_y)**2)

                    elif o.end_x < X and o.end_y < Y < o.start_y:#左
                        dis = math.fabs(X-o.end_x)
                
                    elif X < o.end_x and Y < o.end_y:   #左上
                        dis = math.sqrt((X-o.end_x)**2+(Y-o.end_y)**2)

                    else:   #上
                        dis = math.fabs(o.end_y-Y)

                    if dis < mini:
                        mini = dis
                        idx = i
                if idx == None:
                    print("楕円がない")
                else:
                    print(idx+1,"番目の楕円",  "距離は",mini)
                    d.append(idx+1)
            self.data.append(d)
     
        print(mini)

    def create_graph(self):
        x1 = np.array([330,390,450,510,570,630,690,750,810])
        y1 = np.array([610,550,490,430,370,310,250,190,130])
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.axis('off')
        global color
        # 表の定義
        # dataをMin-Max正規化
        print(self.data)
        norm_data = (self.data - min(self.data)) / (max(self.data) - min(self.data))
        # cmapを使ってデータのカラー配列を作る
        cm = plt.get_cmap('coolwarm')

        color = cm(norm_data)

        the_table = ax1.table(cellText=np.round(self.data,2), colLabels=np.round(x1,2), rowLabels=np.round(y1,2), loc="center", cellColours=color)
        fig.tight_layout()

        # 表をfigure全体に表示させる
        for pos, cell in the_table.get_celld().items():
            cell.set_height(1/len(self.data))
        plt.show()
        plt.close()
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()