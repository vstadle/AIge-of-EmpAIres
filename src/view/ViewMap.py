import pygame
import sys 

from model.Farm import Farm
from model.Keep import Keep
from model.Barracks import Barracks
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.House import House
from model.Camp import Camp
from model.TownCenter import TownCenter

class ViewMap():

    def __init__(self, map, cmap):
        self.map = map  # Référence vers le modèle Map
        self.cmap = cmap  # Référence vers le contrôleur de la fenêtre
        
        self.GRID_WIDTH = 30  # Largeur de la grille en nombre de cellules
        self.GRID_HEIGHT = 30  # Hauteur de la grille en nombre de cellules
        
        # Information sur la carte
        display_info = pygame.display.Info()
        screen_width, screen_height = display_info.current_w, display_info.current_h

        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        # Taille des cellules
        self.TILE_SIZE = min(window_width // self.GRID_WIDTH, window_height // self.GRID_HEIGHT)

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        
        # Initialisation de la police
        self.font = pygame.font.Font(None, 30)

        # Initialiser la fenêtre avec les dimensions appropriées
        window_width = self.GRID_WIDTH * self.TILE_SIZE
        window_height = self.GRID_HEIGHT * self.TILE_SIZE
        self.screen = pygame.display.set_mode((window_width, window_height))

    def draw_map(self, screen,pos_x,pos_y):
        # Remplir l'écran de blanc
        screen.fill(self.WHITE)

        # Définir le point de départ pour l'affichage
        start_row = 35  # Ligne de départ
        start_col = 35  # Colonne de départ

        # Afficher chaque cellule de la carte
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x = col * self.TILE_SIZE
                y = row * self.TILE_SIZE

                # Dessiner un rectangle pour chaque cellule
                pygame.draw.rect(screen, self.GRAY, (x, y, self.TILE_SIZE, self.TILE_SIZE))

                map_row = pos_y + row
                map_col = pos_x + col

                # Vérifier si les indices sont dans les limites de la carte
                if 0 <= map_row < len(self.map.getMap()) and 0 <= map_col < len(self.map.getMap()[0]):
                    if self.map.getMap()[map_row][map_col] != ' ':
                        text_surface = self.font.render(self.map.getMap()[map_row][map_col], True, self.BLACK)
                        screen.blit(text_surface, (x + self.TILE_SIZE // 4, y + self.TILE_SIZE // 4))

        pygame.display.flip()  # Actualiser l'affichage
