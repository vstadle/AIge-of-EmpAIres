import pygame
import sys
import random
import math
import time

from view.ViewMap import ViewMap
from model.Map import Map, MapType
from model.Player import Player
from model.TownCenter import TownCenter
from model.Villager import Villager
from model.Archer import Archer
from model.Horseman import Horseman
from model.Swordsman import Swordsman

class ControllerMap():
    def __init__(self):
        pygame.init()
        self.map = Map(MapType.GENEROUS_RESOURCES)
        self.vMap = ViewMap(self.map, self)  # Passer la référence de la carte
        self.pos_x = 0
        self.pos_y = 0
        self.training_queue = []
        self.lstPlayers = []

    def setLstPlayers(self, lstPlayers):
        self.lstPlayers = lstPlayers

    def placementTownCenter(self, nbPlayer, lstPlayers):
        position = []
        center_x, center_y = 60, 60
        
        radius = 40
        k = random.uniform(0, 1) * 2 * math.pi 
        for i in range(nbPlayer):
            x = radius * math.cos(2 * math.pi * i / nbPlayer)
            y = radius * math.sin(2 * math.pi * i / nbPlayer)
            position.append((x * math.cos(k) - y * math.sin(k) + center_x, 
                             x * math.sin(k) + y * math.cos(k) + center_y))

        cpt = 0
        for i in position:
            self.map.addBuilding(TownCenter(), int(i[0]), int(i[1]), lstPlayers[cpt])
            lstPlayers[cpt].addBuildingInitialize(TownCenter(), int(i[0]), int(i[1]))
            cpt += 1

    def genRessources(self, map_type):
        if map_type == MapType.GENEROUS_RESOURCES:
            self.map.generateGenerousResources()
        elif map_type == MapType.CENTER_RESOURCES:
            self.map.generateCenterResources()
        self.map.generateForest()
    
    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]: self.pos_y -= 1
            if keys[pygame.K_s]: self.pos_y += 1
            if keys[pygame.K_q]: self.pos_x -= 1
            if keys[pygame.K_d]: self.pos_x += 1
            if keys[pygame.K_p]: sys.exit()

            max_x = len(self.map.map[0]) - self.vMap.GRID_WIDTH
            max_y = len(self.map.map) - self.vMap.GRID_HEIGHT
            self.pos_x = max(0, min(self.pos_x, max_x))
            self.pos_y = max(0, min(self.pos_y, max_y))

            self.vMap.draw_map(self.vMap.screen, self.pos_x, self.pos_y)
            pygame.display.flip()

            #self.update_training_units()  # Mettre à jour les unités en entraînement

            for player in self.lstPlayers:
                player.update_training()
                player.update_building()

            clock.tick(30)

    def getMap(self):
        return self.map
    
    def is_free(self, x, y):
        return self.map.is_free(x, y)