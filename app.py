import tkinter as tk
from oval import Oval
from flame import Flame
#  10.8m*10.8m module 90cm 
INIT_WIDTH = 3
INIT_HEIGHT = 2
INIT_AREASIZE = 10
MAGNIFICATION = 2500
OVAL_QUANTITY_LIMIT = 100
IS_MOVING = False   # 楕円が移動中かどうか(移動中: True, 楕円作っている: False)
MODULE = 45 # 90cm

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

        # 文字
        self.canvas.create_text(310, 100, text='1F', font=("HG丸ｺﾞｼｯｸM-PRO",24))
        self.canvas.create_text(990, 100, text='2F', font=("HG丸ｺﾞｼｯｸM-PRO",24))

        # 点線
        for x in range(0, 2000, MODULE):
            for y in range(0, 1000, MODULE):
                self.canvas.create_line(x, 0, x, 0, dash=(1, 5))
                self.canvas.create_line(0, y, 0, y, dash=(1, 5))

        for a in range(0, 2000, MODULE):
            for b in range(0, 1000, MODULE):
                self.canvas.create_line(a, 0, a, 2000, dash=(1, 5))
                self.canvas.create_line(0, b, 2000, b, dash=(1, 5))
        
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
        self.areasize_update_button.place(x=435, y=0)
        
        #　楕円ボタン
        self.oval_button = tk.Button(self, text='楕円', command=self.press_oval)
        self.oval_button.place(x=545, y=0)

        #　四角ボタン
        self.rectangle_button = tk.Button(self, text='四角', command=self.change2rectangle)
        self.rectangle_button.place(x=600, y=0)

        #　外枠ボタン
        self.create_flame_button = tk.Button(self, text='外枠', command=self.create_flame)
        self.create_flame_button.place(x=655, y=0)

        #　重ねるボタン
        self.create_flame_button = tk.Button(self, text='重ねる', command=self.overlap)
        self.create_flame_button.place(x=765, y=0)

        #　階段ボタン
        self.create_flame_button = tk.Button(self, text='階段', command=self.stairs)
        self.create_flame_button.place(x=820, y=0)

        #　整理ボタン
        self.create_flame_button = tk.Button(self, text='整理', command=self.sort_stairs)
        self.create_flame_button.place(x=875, y=0)

        self.canvas.grid(row=1, column=0, columnspan=4)
        #　楕円リスト
        self.oval = []

        # 部屋リスト
        self.room = []
        self.room2 = []

        # 外枠の生成時の採用楕円
        self.oval_flame_creation = []

        #　外枠リスト
        self.flame = []

        #　整理する前の階段リスト
        self.stairs = []

        #　整理した後の階段リスト
        self.stairs2 = []

        #　OvalクラスとAppクラスのキャンバスの統合
        Oval.canvas = self.canvas

        #　FlameクラスとAppクラスのキャンバスの統合
        Flame.canvas = self.canvas
    
    #　階段ボタンが押された時
    def stairs(self):
        self.canvas.bind(sequence='<1>', func = self.create_stairs)

    #　階段を生成
    def create_stairs(self, event):
        start_x = event.x - (MODULE//2)
        start_y = event.y - (3*MODULE//2)
        end_x = event.x + (MODULE//2)
        end_y = event.y + (3*MODULE//2)
        st = Flame(start_x, start_y, end_x, end_y,'blue',5)
        self.stairs.append(st)

    # 階段を点線上に再配置
    def sort_stairs(self):
        for st in self.stairs:
            start_x_dist_min = float('inf')
            start_y_dist_min = float('inf')
            end_x_dist_min = float('inf')
            end_y_dist_min = float('inf')
            start_x2 = st.start_x
            start_y2 = st.start_y
            end_x2 = st.end_x
            end_y2 = st.end_y
            for x in range(0, 2000, MODULE):
                for y in range(0, 2000, MODULE):
                    if abs(start_x2 - x) < start_x_dist_min: # x dist line
                        start_x_dist_min = abs(start_x2 - x)
                        st.start_x = x       
                    if abs(start_y2 - y) < start_y_dist_min: # y dist line
                        start_y_dist_min = abs(start_y2 - y)
                        st.start_y = y       
                    if abs(end_x2 - x) < end_x_dist_min: # x dist line
                        end_x_dist_min = abs(end_x2 - x)
                        st.end_x = x
                    if abs(end_y2 - y) < end_y_dist_min: # y dist line
                        end_y_dist_min = abs(end_y2 - y)
                        st.end_y = y

            stairs = Flame(st.start_x, st.start_y, st.end_x, st.end_y, 'blue', 5)
            self.stairs2.append(stairs)
            self.canvas.delete(st.id)
        
    # 重ねるボタンが押された時、1階に2階の外枠を重ねる（1階に2階の外枠を模した3つ目の外枠を重ねるよう生成）
    def overlap(self):   

        start_x = (self.flame[1].start_x - self.stairs2[1].start_x  + self.stairs2[0].start_x)
        start_y = (self.flame[1].start_y - self.stairs2[1].start_y + self.stairs2[0].start_y)
        end_x = (self.flame[1].end_x - self.stairs2[1].start_x  + self.stairs2[0].start_x)
        end_y = (self.flame[1].end_y - self.stairs2[1].start_y + self.stairs2[0].start_y)
        fla = Flame(start_x, start_y, end_x, end_y, 'green', 3)
        # self.flame.append(fla) 
        for ro in self.room2:
            start_x2 = (ro.start_x - self.stairs2[1].start_x  + self.stairs2[0].start_x)
            start_y2 = (ro.start_y - self.stairs2[1].start_y + self.stairs2[0].start_y)
            end_x2 = (ro.end_x - self.stairs2[1].start_x  + self.stairs2[0].start_x)
            end_y2 = (ro.end_y - self.stairs2[1].start_y + self.stairs2[0].start_y)
            roo = Flame(start_x2, start_y2, end_x2, end_y2, 'green', 3)

    # 外枠ボタンが押されたとき
    def create_flame(self):
        left_most = None
        right_most = None
        up_most = None
        down_most = None
        for oval in self.oval_flame_creation:
            left_most = oval.start_x if left_most is None or oval.start_x < left_most else left_most
            right_most = oval.end_x if right_most is None or oval.end_x > right_most else right_most
            up_most = oval.start_y if up_most is None or oval.start_y < up_most else up_most
            down_most = oval.end_y if down_most is None or oval.end_y > down_most else down_most
        flame = Flame(left_most, up_most, right_most, down_most, 'black', 5)
        self.flame.append(flame)
        self.oval_flame_creation = []
        
    # 楕円を四角に変更
    def change2rectangle(self):
        for ov in self.oval:
            start_x_dist_min = float('inf')
            start_y_dist_min = float('inf')
            end_x_dist_min = float('inf')
            end_y_dist_min = float('inf')
            start_x = ov.start_x
            start_y = ov.start_y
            end_x = ov.end_x
            end_y = ov.end_y
            for x in range(0, 2000, MODULE):
                    for y in range(0, 2000, MODULE):
                        if abs(start_x - x) < start_x_dist_min: # x dist line
                            start_x_dist_min = abs(start_x - x)
                            ov.start_x = x       
                        if abs(start_y - y) < start_y_dist_min: # y dist line
                            start_y_dist_min = abs(start_y - y)
                            ov.start_y = y       
                        if abs(end_x - x) < end_x_dist_min: # x dist line
                            end_x_dist_min = abs(end_x - x)
                            ov.end_x = x
                        if abs(end_y - y) < end_y_dist_min: # y dist line
                            end_y_dist_min = abs(end_y - y)
                            ov.end_y = y
            room = Flame(ov.start_x, ov.start_y, ov.end_x, ov.end_y, 'black', 5)
            if ov.start_x < 560:
                self.room.append(room)
            elif ov.start_x > 560:
                self.room2.append(room)
            # self.room.append(room)
            self.canvas.delete(ov.id)

    #　面積，縦横比の値を更新   
    def update_areasize(self):
        self.areasize = self.areasize_box.get()
        self.height_relative = self.height_relative_box.get()
        self.width_relative = self.width_relative_box.get()

    # 「楕円」ボタンが押された時
    def press_oval(self):
        global IS_MOVING
        IS_MOVING = False
        self.canvas.bind(sequence='<1>', func = self.create_oval)
     
    # 「楕円」ボタンが押された時
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
                self.x = center_x + 1
                self.y = center_y + 1
                ov = Oval(center_x, center_y, center_x-dist_x, center_y-dist_y, center_x+dist_x, center_y+dist_y, size, width, height, self.x, self.y)
                self.oval.append(ov)
                self.oval_flame_creation.append(ov)

                # self.oval[floor].append(ov)
            self.canvas.delete('error_message')
        except ValueError:
            self.canvas.create_text(100, 100, text='数値を入力してください', fill='red', tags='error_message')
    
