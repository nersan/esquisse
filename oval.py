class Oval:
    canvas = None

    def __init__(self, center_x, center_y, start_x, start_y, end_x, end_y, areasize, width, height, x, y):
        self.center_x = center_x
        self.center_y = center_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.areasize = areasize
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.deleted = False    # 楕円がdeleteされたかどうか(deleteされていればTrue)
        self.id = self.canvas.create_oval(self.start_x, self.start_y, self.end_x, self.end_y, outline='black', fill='', width=5)
        self.canvas.tag_bind(self.id, '<2>', self.delete)

    def bind_move(self):
        # 楕円が移動できるようにキーを割り当て
        self.canvas.tag_bind(self.id, '<1>', self.drag_start)   # クリックし始め
        self.canvas.tag_bind(self.id, '<Button1-Motion>', self.dragging)    # ドラッグ中

    # クリックし始め
    def drag_start(self, event):
        self.x = event.x
        self.y = event.y

    # ドラッグ中
    def dragging(self, event):
        x1 = event.x
        y1 = event.y
        # 楕円の移動
        Oval.canvas.move(self.id, x1-self.x, y1-self.y)
        # 値の更新
        self.center_x = self.center_x + (x1 - self.x)
        self.center_y = self.center_y + (y1 - self.y)
        self.start_x = self.center_x - self.width / 2
        self.start_y = self.center_y - self.height / 2
        self.end_x = self.center_x + self.width / 2
        self.end_y = self.center_y + self.height / 2
        self.x = event.x
        self.y = event.y

    def delete(self, event):
        self.deleted = True
        self.canvas.delete(self.id)