from model.TownCenter import TownCenter 
from model.Farm import Farm
from model.Keep import Keep
from model.Barracks import Barracks
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.House import House
from model.Camp import Camp
from model.Ressources import Ressources
from model.Units import Units
from model.Gold import Gold
from model.Food import Food
from model.Wood import Wood
from logs.logger import logs
from model.Villager import Villager
import numpy as np

import random
import curses
import pygame
import logging

class MapType():
    GENEROUS_RESOURCES = 1
    CENTER_RESOURCES = 2
class Map():
    def __init__(self, size_map_x, size_map_y):

        #Matrice de 120x120 qui va contenir les batiments
        #self.mapBuildings = [[None for x in range(size_map_y)] for y in range(size_map_x)]

        #Matrice de 120x120 qui va contenir les ressources
        #self.mapRessources = [[None for x in range(size_map_y)] for y in range(size_map_x)]

        #Matrice de 120x120 qui va contenir les unités
        #self.mapUnits = [[None for x in range(size_map_y)] for y in range(size_map_x)]

        #Listes des couleurs
        '''self.lstColor= [[None for x in range(size_map_y)] for y in range(size_map_x)]

        self.map = [[" " for x in range(size_map_y)] for y in range(size_map_x)]
        self.map[0][0] = 'R'

        self.map_entities = [[None for x in range(size_map_y)] for y in range(size_map_x)]

        self.map[size_map_x-1][size_map_y-1] = 'R'
        '''
    
        self.size_map_x = size_map_x
        self.size_map_y = size_map_y
        self.map = np.full((size_map_x, size_map_y), ' ', dtype='<U1')
        self.map[0][0] = 's'
        self.map_entities = np.full((size_map_x, size_map_y), None)
        self.map_entities[0][0] = Units
        self.mapType = None
        
    
    def generateGenerousResources(self):
        max_percentage_gold = 0.01
        total_cells = self.size_map_x * self.size_map_y
        max_gold_blocks = int(max_percentage_gold * total_cells / 4)
        gold_blocks_planted = 0

        while gold_blocks_planted < max_gold_blocks:
            x = random.randint(0, self.size_map_x - 2)  # Ajustement pour s'assurer que le bloc 2x2 ne dépasse pas la map
            y = random.randint(0, self.size_map_y - 2)

            # Vérifier si le bloc 2x2 est libre
            if (self.map[x][y] == " " and
                self.map[x+1][y] == " " and
                self.map[x][y+1] == " " and
                self.map[x+1][y+1] == " "):
                
                self.addRessources(Gold(), x, y)
                self.addRessources(Gold(), x+1, y)
                self.addRessources(Gold(), x, y+1)
                self.addRessources(Gold(), x+1, y+1)
                
                gold_blocks_planted += 1


    def generateCenterResources(self):
        center_x, center_y = self.size_map_x//2, self.size_map_y//2 
        width = random.randint(3, 7)  
        height = random.randint(3, 7)  

        start_x = center_x - width // 2
        start_y = center_y - height // 2
        for dx in range(width): 
            for dy in range(height):
                x = start_x + dx
                y = start_y + dy
                if 0 <= x < self.size_map_x and 0 <= y < self.size_map_y:
                    self.addRessources(Gold(), x, y)


    def generateSizeRessources(self, r, x, y):
        
        r_x = random.randint(1, 5)
        r_y = random.randint(1,5)
        for i in range(r_x):
            for j in range(r_y):
                self.addRessources(r, x + i, y+j)

    def addRessources(self, Ressources, x,y):
        self.map_entities[x][y] = Ressources
        #self.mapRessources[x][y] = Ressources
        self.map[x][y] = Ressources.letter
        Ressources.setXY(x, y)

    def addBuilding(self, building, x, y, player):
        building.setX(x)
        building.setY(y)
        building.color = player.getColor()
        building.player = player
        building.is_constructing = False
        for i in range(building.sizeMap):
            for j in range(building.sizeMap):
                self.map_entities[x + i][y + j] = building
                self.map[x + i][y + j] = building.letter
        
        if isinstance(building, Keep):
            player.lstKeep.append(building)


        if isinstance(building, TownCenter) or isinstance(building, House):
            player.population += building.population
            
    def addBuildingTemp(self, building, x, y):
        building.setX(x)
        building.setY(y)
        building.is_constructing = True  # Nouveau : marquer comme en construction
        for i in range(building.sizeMap):
            for j in range(building.sizeMap):
                self.map[x + i][y + j] = building.letter

    def addUnits(self, units, x, y, player):
        units.color = player.getColor()
        self.map_entities[x][y] = units
        self.map[x][y] = units.letter
        units.setPosition(x, y)
        units.player = player

    
    def generateForest(self):
        max_percentage_wood = 0.05
        total_cells = self.size_map_x * self.size_map_y
        max_trees = int(total_cells * max_percentage_wood)
        total_trees_planted = 0

        while total_trees_planted < max_trees:
            # Use a more irregular shape generation
            forest_shape = self._generate_forest_mask()
            
            # Find a valid placement for the forest
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(0, self.size_map_x - len(forest_shape))
                y = random.randint(0, self.size_map_y - len(forest_shape[0]))
                
                # Check if the forest can be placed
                if self._can_place_forest(forest_shape, x, y):
                    # Place the forest
                    trees_planted = self._place_forest(forest_shape, x, y)
                    total_trees_planted += trees_planted
                    placed = True
                
                attempts += 1
            
            if not placed:
                break

    def _generate_forest_mask(self):
        # Generate an irregular forest shape
        size = random.randint(5, 15)
        forest_mask = [[False] * size for _ in range(size)]
        
        # Use a randomized cellular automata-like approach
        for i in range(size):
            for j in range(size):
                # Randomly decide to add a tree with decreasing probability towards edges
                prob = 0.7 - (abs(i - size//2) + abs(j - size//2)) * 0.05
                if random.random() < prob:
                    forest_mask[i][j] = True
        
        return forest_mask

    def _can_place_forest(self, forest_shape, start_x, start_y):
        for i in range(len(forest_shape)):
            for j in range(len(forest_shape[0])):
                if forest_shape[i][j]:
                    # Check if this cell can accommodate a tree
                    if (start_x + i >= self.size_map_x or 
                        start_y + j >= self.size_map_y or 
                        self.map[start_x + i][start_y + j] != " "):
                        return False
        return True

    def _place_forest(self, forest_shape, start_x, start_y):
        trees_planted = 0
        for i in range(len(forest_shape)):
            for j in range(len(forest_shape[0])):
                if forest_shape[i][j]:
                    self.addRessources(Wood(), start_x + i, start_y + j)
                    trees_planted += 1
        return trees_planted

    '''def addTownCenter(self, towncenter): 
        center_x, center_y = self.size_map_x//2, self.size_map_y//2
        distance_from_center = random.randint(40,55)
        angle = random.uniform(0, 2 * 3.14159)
        pos1_x = int(center_x + distance_from_center * random.uniform(-1, 1))
        pos1_y = int(center_y + distance_from_center * random.uniform(-1, 1))
        pos2_x = center_x - (pos1_x - center_x)
        pos2_y = center_y - (pos1_y - center_y)
        self.addBuilding(towncenter, pos1_x, pos1_y)
        self.addBuilding(towncenter, pos2_x, pos2_y)'''
    
    def getMap(self):
        return self.map
    
    def getBuildings(self):
        return self.mapBuildings
    
    def getRessources(self):
        return self.mapRessources
    
    def is_free(self, x, y):
        
        return (
            0 <= x < len(self.map_entities) and 
            0 <= y < len(self.map_entities[0]) and
            self.map_entities[x][y] is None
        )
    

    def rmUnit(self, unit):
        self.map_entities[unit.getX()][unit.getY()] = None
        #self.mapUnits[unit.getX()][unit.getY()] = None
        self.map[unit.getX()][unit.getY()] = " "
    
    def rmBuilding(self, building):
        for i in range(building.sizeMap):
            for j in range(building.sizeMap):
                self.map_entities[building.getX() + i][building.getY() + j] = None
                #self.mapBuildings[building.getX() + i][building.getY() + j] = None
                self.map[building.getX() + i][building.getY() + j] = " "
    
    def rmRessource(self, ressource):
        self.map_entities[ressource.getX()][ressource.getY()] = None
        #self.mapRessources[ressource.getX()][ressource.getY()] = None
        self.map[ressource.getX()][ressource.getY()] = " "

    def moveUnit(self, unit, x, y, player):
        pos = unit.getPosition()
        self.map_entities[pos[0]][pos[1]] = None
        self.map[pos[0]][pos[1]] = " "
        
        self.map_entities[x][y] = unit
        unit.setPosition(x, y)
        self.map[x][y] = unit.letter

    def setMapType(self, type):
        self.mapType = type

    def get_map_entities(self):
        return self.map_entities
    def getColor(self, x, y):
        entity = self.map_entities[x][y]
        if entity:
            if hasattr(entity, 'is_constructing') and entity.is_constructing:
                return curses.COLOR_WHITE
            return entity.color if hasattr(entity, 'color') else None
        return None