
class Camera_terminal():

    def __init__(self, map):

        self.pos_x = 0
        self.pos_y = 0

        self.map = map

    def move(self, x, y, strdscr):
        if self.pos_x + x < 0 or self.pos_y + y < 0:
            return 0
        elif self.pos_x + strdscr.getmaxyx()[1] + x > self.map.size_map_x - 1 or self.pos_y + strdscr.getmaxyx()[0] + y > self.map.size_map_y - 1:
            return 0
    
        self.pos_x += x
        self.pos_y += y

        return 1