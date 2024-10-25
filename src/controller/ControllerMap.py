import pygame
import sys
from view.ViewMap import ViewMap
from model.Map import Map, MapType

class ControllerMap():
    def __init__(self):
        pygame.init()
        self.map = Map(MapType.CENTER_RESOURCES)
        self.vMap = ViewMap(self.map, self)  # Passer la référence de la carte
        self.pos_x=0
        self.pos_y=0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()  # Récupérer l'état des touches
            if keys[pygame.K_z]:  
                self.pos_y -= 1 
            if keys[pygame.K_s]: 
                self.pos_y += 1  
            if keys[pygame.K_q]:  
                self.pos_x -= 1 
            if keys[pygame.K_d]:  
                self.pos_x += 1  
            if keys[pygame.K_p]:
                pygame.quit()
                sys.exit()
            
            max_x = len(self.map.map[0]) - self.vMap.GRID_WIDTH  # Largeur maximale
            max_y = len(self.map.map) - self.vMap.GRID_HEIGHT  # Hauteur maximale

            self.pos_x = max(0, min(self.pos_x, max_x))
            self.pos_y = max(0, min(self.pos_y, max_y))

            self.vMap.draw_map(self.vMap.screen, self.pos_x,self.pos_y) 
            pygame.display.flip()
