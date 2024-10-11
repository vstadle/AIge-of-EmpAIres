import pygame
import sys 

class ViewMap():
    TILESIZE = 20  # Taille d'une cellule (20x20 pixels)
    GRID_WIDTH = 35  # Largeur de la grille en nombre de cellules
    GRID_HEIGHT = 35  # Hauteur de la grille en nombre de cellules
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    def __init__(self,TILESIZE,GRID_WIDTH,GRID_HEIGHT):
        pygame.init()
        window_width = self.GRID_WIDTH * self.TILE_SIZE
        window_height = self.GRID_HEIGHT * self.TILE_SIZE
        screen = pygame.display.set_mode((window_width, window_height))
    def map_generator(self,GRID_WIDTH,GRID_HEIGHT):
        map_data = [[' ' for i in range(self.GRID_WIDTH)] for j in range(self.GRID_HEIGHT)]
        map_data[5][5] = 'T'  # TownCenter
        map_data[10][10] = 'F'  # Farm
        map_data[15][15] = 'G'  # Gold
        map_data[20][20] = 'W'  # Wood
    
    def draw_map(self,GRID_WIDTH,GRID_HEIGHT,TILESIZE,):
        screen.fill(WHITE)  # Remplir l'écran de blanc
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                x = col * TILESIZE
                y = row * TILESIZE
                pygame.draw.rect(screen, GRAY, (x, y, TILESIZE, TILESIZE), 1)  # Dessiner la grille

