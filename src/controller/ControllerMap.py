import pygame
import sys
from view.ViewMap import ViewMap
from model.Map import Map

class ControllerMap():
    def __init__(self):
        pygame.init()
        self.map = Map()
        self.vMap = ViewMap(self.map, self)  # Passer la référence de la carte

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.vMap.draw_map(self.vMap.screen)  # Appeler la méthode pour dessiner la carte avec l'argument screen