import pygame
import sys 
from model.Map import Map

class ViewMap():
    TILE_SIZE = 20  # Taille d'une cellule (20x20 pixels)
    GRID_WIDTH = 35  # Largeur de la grille en nombre de cellules
    GRID_HEIGHT = 35  # Hauteur de la grille en nombre de cellules
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    font = pygame.font.Font(None, 30)

    def __init__(self,map):
        self.map = map #Reference vers le modèle Map
    
    def draw_map(self):

        pygame.init()

        window_width = self.GRID_WIDTH * self.TILE_SIZE
        window_height = self.GRID_HEIGHT * self.TILE_SIZE
        screen = pygame.display.set_mode((window_width, window_height))

        screen.fill(self.WHITE)

        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x = col * self.TILE_SIZE
                y = row * self.TILE_SIZE
                pygame.draw.react(screen, self.GRAY, (x,y,self.TILE_SIZE,self.TILE_SIZE))

                if self.map[row][col] != ' ':
                    text_surface = self.font.render(self.map[row][col], True, self.BLACK)
                    screen.blit(text_surface, (x + self.TILE_SIZE // 4, y + self.TILE_SIZE // 4))
    
    def printMap():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Quitter en appuyant sur 'q'
                        pygame.quit()
                        sys.exit()
