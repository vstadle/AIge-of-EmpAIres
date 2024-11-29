import curses

class ViewTerminal:
    def __init__(self, map_obj):
        self.map = map_obj
        self.camera_x = 0
        self.camera_y = 0
        self.screen = None
        self.height = 0
        self.width = 0
        
    def initialiser(self, stdscr):
        curses.use_default_colors()
        curses.curs_set(0)
        stdscr.keypad(True)
        self.screen = stdscr

        self.height, self.width = stdscr.getmaxyx()

        map_data = self.map.getMap()
        map_height = len(map_data)
        map_width = len(map_data[0]) if map_height > 0 else 0
        self.height = min(self.height, map_height)
        self.width = min(self.width, map_width)

    def draw_map(self):
        self.screen.clear()

        map_data = self.map.getMap()
        map_height = len(map_data)
        map_width = len(map_data[0]) if map_height > 0 else 0

        for y in range(self.height):
            for x in range(self.width):
                map_x = x + self.camera_x
                map_y = y + self.camera_y

                if 0 <= map_y < map_height and 0 <= map_x < map_width:
                    cellule = map_data[map_y][map_x]
                    caractere = self.obtenir_caractere(cellule)
                else:
                    caractere = ' '

                try:
                    self.screen.addch(y, x, caractere)
                except curses.error:
                    pass 

    def obtenir_caractere(self, cellule):
        mapping = {
            ' ': '.',  
            'W': 'W',  
            'G': 'G',  
            'A': 'A', 
            'T': 'T',
            'B': 'B', 
            'R': 'R' 
        }
        return mapping.get(cellule, '?')

    def deplacer_camera(self, dx, dy):
        map_data = self.map.getMap()
        map_height = len(map_data)
        map_width = len(map_data[0]) if map_height > 0 else 0

        if map_width > self.width:
            self.camera_x = max(0, min(self.camera_x + dx, map_width - self.width))
        else:
            self.camera_x = 0

        if map_height > self.height:
            self.camera_y = max(0, min(self.camera_y + dy, map_height - self.height))
        else:
            self.camera_y = 0
