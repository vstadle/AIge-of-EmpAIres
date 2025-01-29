import curses
import logging

from logs.logger import logs
from view.Camera_terminal import Camera_terminal

class ViewTerminal:

    lstColor = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_BLUE, curses.COLOR_YELLOW, curses.COLOR_MAGENTA, curses.COLOR_CYAN]

    def __init__(self, map):
        
        self.GRID_HEIGHT = len(map.map)
        self.GRID_WIDTH = len(map.map[0])

        self.map = map

        self.camera = Camera_terminal(map)

    def draw_map(self, stdscr):
        stdscr.clear()
    
        # Vérification que les couleurs sont initialisées (uniquement une fois)
        if not hasattr(self, 'colors_initialized'):
            self._initialize_colors(stdscr)
            self.colors_initialized = True
    
        # Dimensions de l'écran
        max_x, max_y = stdscr.getmaxyx()
        # Limiter les dimensions visibles aux dimensions de la carte
        visible_rows = min(max_y, self.GRID_HEIGHT)
        visible_cols = min(max_x, self.GRID_WIDTH)

        # Parcourir uniquement la zone visible
        for row in range(visible_rows):
            for col in range(visible_cols):
                map_row = self.camera.pos_x + row
                map_col = self.camera.pos_y + col
                # Vérifier si les indices sont valides pour la carte
                if 0 <= map_row < len(self.map.map) and 0 <= map_col < len(self.map.map[0]):
                    char = self.map.map[map_row][map_col]
                    if char is None or not isinstance(char, str) or len(char) != 1:
                        char = ' '
                
                    # Utiliser getColor à la place de lstColor
                    color_index = self.map.getColor(map_row, map_col)
                    
                    # Trouver l'index de couleur correspondant dans lstColor
                    try:
                        color_index = ViewTerminal.lstColor.index(color_index) + 1 if color_index is not None else 7
                    except ValueError:
                        color_index = 7
                    
                    color_pair = curses.color_pair(color_index)
                else:
                    char = ' '
                    color_pair = curses.color_pair(7)
                
                # Ajouter le caractère à la position (row, col)
                try:
                    stdscr.addch(col, row, char, color_pair)
                except curses.error:
                    pass
        
        # Rafraîchir l'écran une seule fois après avoir dessiné la carte visible
        stdscr.refresh()

    def _initialize_colors(self, stdscr):
        curses.start_color()
        # Initialiser les 6 paires de couleurs pour les joueurs
        for i, color in enumerate(ViewTerminal.lstColor, 1):
            curses.init_pair(i, color, curses.COLOR_BLACK)
        # Couleur par défaut (blanc)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

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