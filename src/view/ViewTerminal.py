import curses

class ViewTerminal:
    def __init__(self, map_obj):
        self.map = map_obj
        self.camera_x = 0
        self.camera_y = 0
        self.screen = None
        self.height = 0
        self.width = 0

        # Vérification initiale de la validité de la carte
        if not self.map or not isinstance(self.map.getMap(), list) or not self.map.getMap():
            raise ValueError("La carte fournie est invalide ou vide.")

    def initialiser(self, stdscr):
        # Initialisation de curses
        curses.use_default_colors()
        curses.curs_set(0)
        stdscr.keypad(True)
        self.screen = stdscr

        # Récupération des dimensions de l'écran
        self.height, self.width = stdscr.getmaxyx()

        # Si la carte est plus petite que l'écran, ajuster les dimensions
        map_data = self.map.getMap()
        map_height = len(map_data)
        map_width = len(map_data[0]) if map_height > 0 else 0
        self.height = min(self.height, map_height)
        self.width = min(self.width, map_width)

    def draw_map(self):
        # Effacer l'écran avant de dessiner
        self.screen.clear()

        # Récupération de la carte et de ses dimensions
        map_data = self.map.getMap()
        map_height = len(map_data)
        map_width = len(map_data[0]) if map_height > 0 else 0

        # Parcourir chaque cellule de l'écran
        for y in range(self.height):
            for x in range(self.width):
                map_x = x + self.camera_x
                map_y = y + self.camera_y

                if 0 <= map_y < map_height and 0 <= map_x < map_width:
                    # Cellule valide dans la carte
                    cellule = map_data[map_y][map_x]
                    caractere = self.obtenir_caractere(cellule)
                else:
                    # En dehors de la carte
                    caractere = ' '

                try:
                    # Afficher le caractère dans la cellule correspondante
                    self.screen.addch(y, x, caractere)
                except curses.error:
                    pass  # Ignorer les erreurs sans interrompre le programme

    def obtenir_caractere(self, cellule):
        # Mapping des cellules de la carte à des caractères
        mapping = {
            ' ': '.',  # Terrain vide
            'W': 'W',  # Forêt
            'G': 'G',  # Or
            'A': 'A',  # Eau
            'T': 'T',  # Terrain
            'B': 'B',  # Bâtiment
            'R': 'R'   # Ressources
        }
        return mapping.get(cellule, '?')

    def deplacer_camera(self, dx, dy):
        # Récupérer les dimensions de la carte
        map_data = self.map.getMap()
        map_height = len(map_data)
        map_width = len(map_data[0]) if map_height > 0 else 0

        # Limiter la caméra à rester dans les limites de la carte
        if map_width > self.width:
            self.camera_x = max(0, min(self.camera_x + dx, map_width - self.width))
        else:
            self.camera_x = 0  # Pas de déplacement horizontal si la carte est plus petite

        if map_height > self.height:
            self.camera_y = max(0, min(self.camera_y + dy, map_height - self.height))
        else:
            self.camera_y = 0  # Pas de déplacement vertical si la carte est plus petite
