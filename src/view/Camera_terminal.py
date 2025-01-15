
class Camera_terminal():

    def __init__(self, map):

        self.pos_x = 0
        self.pos_y = 0

        self.map = map

    def move(self, x, y, strdscr):
    
        if self.pos_x + x >= 0 and self.pos_x + x + strdscr.getmaxyx()[0] <= len(self.map.map):
            self.pos_x += x
        if self.pos_y + y >= 0 and self.pos_y + y + strdscr.getmaxyx()[1] <= len(self.map.map[0]):
            self.pos_y += y