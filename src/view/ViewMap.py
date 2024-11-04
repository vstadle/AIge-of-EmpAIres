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
        self.TILE_SIZE_2_5D = self.TILE_SIZE
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN = (34, 139, 34)    # Bois
        self.YELLOW = (255, 215, 0)   # Or
        
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
    def draw_map_2_5d(self, screen, pos_x, pos_y):
        # Remplir l'écran de blanc
        screen.fill(self.WHITE)

        # Propriétés de projection isométrique
        iso_offset_x = self.TILE_SIZE_2_5D // 2
        iso_offset_y = self.TILE_SIZE_2_5D // 4

        # Parcours de la carte pour dessiner les ressources
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                map_row = pos_y + row
                map_col = pos_x + col

                # Vérifier si les indices sont dans les limites de la carte
                if 0 <= map_row < len(self.map.getMap()) and 0 <= map_col < len(self.map.getMap()[0]):
                    tile = self.map.getMap()[map_row][map_col]

                    # Calcul de la position isométrique
                    x = (col - row) * iso_offset_x + self.GRID_WIDTH * self.TILE_SIZE_2_5D // 2 
                    y = (col + row) * iso_offset_y 

                    # Définir la couleur en fonction de la ressource
                    if tile == "W":  # Bois
                        color = self.GREEN
                    elif tile == "G":  # Or
                        color = self.YELLOW
                    elif tile == "T":
                        color = self.GRAY
                    else:
                        color = self.BLACK  # Case vide

                    # Dessiner le rectangle coloré pour représenter la ressource
                    pygame.draw.rect(screen, color, (x, y, self.TILE_SIZE_2_5D, self.TILE_SIZE_2_5D // 2))

        mini_map_width = 200
        mini_map_height = 200
        mini_map_x = screen.get_width() - mini_map_width - 10 
        mini_map_y = screen.get_height() - mini_map_height - 10 

        # Dessiner le fond de la mini-carte
        pygame.draw.rect(screen, self.GRAY, (mini_map_x, mini_map_y, mini_map_width, mini_map_height))

        # Dessiner un contour pour la mini-carte
        pygame.draw.rect(screen, self.BLACK, (mini_map_x, mini_map_y, mini_map_width, mini_map_height), 2)

        # Dessiner la carte dans la mini-carte
        for mini_row in range(len(self.map.getMap())):
            for mini_col in range(len(self.map.getMap()[0])):
                mini_tile = self.map.getMap()[mini_row][mini_col]

                # Échelle pour la mini-carte
                mini_x = mini_col * (mini_map_width / len(self.map.getMap()[0]))
                mini_y = mini_row * (mini_map_height / len(self.map.getMap()))

                # Définir la couleur en fonction de la ressource
                if mini_tile == "W":  # Bois
                    mini_color = self.GREEN
                elif mini_tile == "G":  # Or
                    mini_color = self.YELLOW
                elif mini_tile == "T":
                    mini_color = self.GRAY
                else:
                    mini_color = self.BLACK  # Case vide

                # Dessiner le rectangle coloré pour représenter la ressource dans la mini-carte
                pygame.draw.rect(screen, mini_color, (mini_x + mini_map_x, mini_y + mini_map_y, mini_map_width / len(self.map.getMap()[0]), mini_map_height / len(self.map.getMap())))

        # Dessiner la position actuelle sur la mini-carte (représentée par un rectangle rouge)
        mini_map_scale_x = mini_map_width / len(self.map.getMap()[0]) 
        mini_map_scale_y = mini_map_height / len(self.map.getMap()) 
        current_pos_x = pos_x * mini_map_scale_x + mini_map_x
        current_pos_y = pos_y * mini_map_scale_y + mini_map_y
        rectangle_size = 50
        pygame.draw.rect(screen, (255, 0, 0), (current_pos_x, current_pos_y, rectangle_size, rectangle_size))

        pygame.display.flip()
    def draw_map_2_5d(self, screen, pos_x, pos_y):
        # Remplir l'écran de blanc
        screen.fill(self.WHITE)

        # Propriétés de projection isométrique
        iso_offset_x = self.TILE_SIZE_2_5D // 2
        iso_offset_y = self.TILE_SIZE_2_5D // 4

        # Parcours de la carte pour dessiner les ressources
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                map_row = pos_y + row
                map_col = pos_x + col

                # Vérifier si les indices sont dans les limites de la carte
                if 0 <= map_row < len(self.map.getMap()) and 0 <= map_col < len(self.map.getMap()[0]):
                    tile = self.map.getMap()[map_row][map_col]

                    # Calcul de la position isométrique
                    x = (col - row) * iso_offset_x + self.GRID_WIDTH * self.TILE_SIZE_2_5D // 2 
                    y = (col + row) * iso_offset_y 

                    # Définir la couleur en fonction de la ressource
                    if tile == "W":  # Bois
                        color = self.GREEN
                    elif tile == "G":  # Or
                        color = self.YELLOW
                    elif tile == "T":
                        color = self.GRAY
                    else:
                        color = self.BLACK  # Case vide

                    # Dessiner le rectangle coloré pour représenter la ressource
                    pygame.draw.rect(screen, color, (x, y, self.TILE_SIZE_2_5D, self.TILE_SIZE_2_5D // 2))

        mini_map_width = 200
        mini_map_height = 200
        mini_map_x = screen.get_width() - mini_map_width - 10 
        mini_map_y = screen.get_height() - mini_map_height - 10 

        # Dessiner le fond de la mini-carte
        pygame.draw.rect(screen, self.GRAY, (mini_map_x, mini_map_y, mini_map_width, mini_map_height))

        # Dessiner un contour pour la mini-carte
        pygame.draw.rect(screen, self.BLACK, (mini_map_x, mini_map_y, mini_map_width, mini_map_height), 2)

        # Dessiner la carte dans la mini-carte
        for mini_row in range(len(self.map.getMap())):
            for mini_col in range(len(self.map.getMap()[0])):
                mini_tile = self.map.getMap()[mini_row][mini_col]

                # Échelle pour la mini-carte
                mini_x = mini_col * (mini_map_width / len(self.map.getMap()[0]))
                mini_y = mini_row * (mini_map_height / len(self.map.getMap()))

                # Définir la couleur en fonction de la ressource
                if mini_tile == "W":  # Bois
                    mini_color = self.GREEN
                elif mini_tile == "G":  # Or
                    mini_color = self.YELLOW
                elif mini_tile == "T":
                    mini_color = self.GRAY
                else:
                    mini_color = self.BLACK  # Case vide

                # Dessiner le rectangle coloré pour représenter la ressource dans la mini-carte
                pygame.draw.rect(screen, mini_color, (mini_x + mini_map_x, mini_y + mini_map_y, mini_map_width / len(self.map.getMap()[0]), mini_map_height / len(self.map.getMap())))

        # Dessiner la position actuelle sur la mini-carte (représentée par un rectangle rouge)
        mini_map_scale_x = mini_map_width / len(self.map.getMap()[0]) 
        mini_map_scale_y = mini_map_height / len(self.map.getMap()) 
        current_pos_x = pos_x * mini_map_scale_x + mini_map_x
        current_pos_y = pos_y * mini_map_scale_y + mini_map_y
        rectangle_size = 50
        pygame.draw.rect(screen, (255, 0, 0), (current_pos_x, current_pos_y, rectangle_size, rectangle_size))

        pygame.display.flip()