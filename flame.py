class Flame:
    canvas = None

    def __init__(self, start_x, start_y, end_x, end_y, color, width):
       self.start_x = start_x
       self.start_y = start_y
       self.end_x = end_x
       self.end_y = end_y
       self.color = color
       self.id = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline=self.color, fill='', width=width)
