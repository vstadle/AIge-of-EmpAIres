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
        self.zoom_level = 1.0
        self.training_queue = []
        self.display_mode = "2D"  # Mode d'affichage initial


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
            self.map.addBuilding(TownCenter(), int(i[0]), int(i[1]))
            lstPlayers[cpt].addBuildingInitialize(TownCenter(), int(i[0]), int(i[1]))
            cpt += 1

    def addBuilding(self, building, x, y):
        self.map.addBuilding(building, x, y)

    def genRessources(self, map_type):
        if map_type == MapType.GENEROUS_RESOURCES:
            self.map.generateGenerousResources()
        elif map_type == MapType.CENTER_RESOURCES:
            self.map.generateCenterResources()
        self.map.generateForest()

    def addUnits(self, unit, player, building):
        start_time = time.time()
        self.training_queue.append({"unit": unit, "player": player, "start_time": start_time, "building": building})

    def update_training_units(self):
        current_time = time.time()
        for item in self.training_queue[:]:  # Itérer sur une copie de la liste
            unit = item["unit"]
            player = item["player"]
            start_time = item["start_time"]
            building = item["building"]

            if current_time - start_time >= unit.trainingTime:
                x = building.getX()
                y = building.getY()
                building_width, building_height = building.getSizeMap(), building.getSizeMap()

                placed = False
                layer = 1  # On commence par la couche directement autour du bâtiment

                while not placed:
                    # Parcours des cases autour de la couche actuelle
                    for dx in range(-layer, layer + 1):
                        for dy in range(-layer, layer + 1):
                            # Vérifier uniquement les positions aux bords de la couche
                            if abs(dx) == layer or abs(dy) == layer:
                                nx, ny = x + dx, y + dy
                                if self.map.is_free(nx, ny):
                                    self.map.addUnits(unit, nx, ny)
                                    player.addUnit(unit)
                                    placed = True
                                    break
                        if placed:
                            break
                    if not placed:
                        
                        layer += 1

                
                self.training_queue.remove(item)
    
    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        self.display_mode = "2.5D" if self.display_mode == "2D" else "2D"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  
                        self.zoom_level = round(min(1.4, self.zoom_level + 0.1), 1)
                    elif event.button == 5:  
                        self.zoom_level = round(max(0.5, self.zoom_level - 0.1), 1)
                        if self.zoom_level < 0.1:
                            self.zoom_level = 0.1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]: self.pos_y -= 1
            if keys[pygame.K_s]: self.pos_y += 1
            if keys[pygame.K_q]: self.pos_x -= 1
            if keys[pygame.K_d]: self.pos_x += 1
            if keys[pygame.K_p]: sys.exit()
            
            max_x = max(0, len(self.map.map[0]) - (self.vMap.GRID_WIDTH / self.zoom_level))
            max_y = max(0, len(self.map.map) - (self.vMap.GRID_HEIGHT / self.zoom_level))

            self.pos_x = max(0, min(self.pos_x, max_x))
            self.pos_y = max(0, min(self.pos_y, max_y))

            if self.display_mode == "2D":
                self.vMap.draw_map(self.vMap.screen, self.pos_x, self.pos_y)
            else:
                self.vMap.draw_map_2_5D(self.vMap.screen, self.pos_x, self.pos_y, self.zoom_level)

            pygame.display.flip()

            self.update_training_units()  

            clock.tick(30)

    def getMap(self):
        return self.map
    
    def is_free(self, x, y):
        return self.map.is_free(x, y)