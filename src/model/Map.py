from model.TownCenter import TownCenter 
from model.Farm import Farm
from model.Keep import Keep
from model.Barracks import Barracks
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.House import House
from model.Camp import Camp
from model.Ressources import Ressources
from model.Gold import Gold
from model.Food import Food
from model.Wood import Wood
from logs.logger import logs


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
        self.lstColor= [[None for x in range(size_map_y)] for y in range(size_map_x)]

        self.map = [[" " for x in range(size_map_y)] for y in range(size_map_x)]
        self.map[0][0] = 'R'

        self.map_entities = [[None for x in range(size_map_y)] for y in range(size_map_x)]

        self.map[size_map_x-1][size_map_y-1] = 'R'

        self.size_map_x = size_map_x
        self.size_map_y = size_map_y

        self.mapType = None
        
    
    def generateGenerousResources(self):
        max_percentage_gold = 0.01
        total_cells = self.size_map_x*self.size_map_y
        max_gold = max_percentage_gold * total_cells
        gold_planted = 0
        while (gold_planted < max_gold):
            x = random.randint(0,self.size_map_x-1)
            y = random.randint(0,self.size_map_y-1)
            if(self.map[x][y]== " "):
                self.addRessources(Gold(), x, y)
                gold_planted+=1



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
        cpt = 0
        for i in range(building.sizeMap):
            cpt += 1
            for j in range(building.sizeMap):
                self.map_entities[x + i][y + j] = building
                #self.mapBuildings[x + i][y + j] = building
                self.map[x + i][y + j] = building.letter
                self.lstColor[x + i][y + j] = player.getColor()
        if isinstance(building, TownCenter) or isinstance(building, House):
            player.population += building.population

    def addBuildingTemp(self, building, x, y):
        building.setX(x)
        building.setY(y)
        for i in range(building.sizeMap):
            for j in range(building.sizeMap):
                self.map[x + i][y + j] = building.letter
                self.lstColor[x + i][y + j] = curses.COLOR_WHITE

    def addUnits(self, units, x, y, player):
        self.map_entities[x][y] = units
        #self.mapUnits[x][y] = units
        self.map[x][y] = units.letter
        self.lstColor[x][y] = player.getColor()
        units.setPosition(x, y)

    def generateForest(self):
        max_percentage_wood = 0.1 
        total_cells = self.size_map_x * self.size_map_y
        max_trees = int(total_cells * max_percentage_wood) 

        num_forests = random.randint(3, 8) 
        total_trees_planted = 0 

        while total_trees_planted < max_trees:
            width = random.randint(3, 10)

            height = random.randint(3, 10)
            num_trees_in_forest = width * height

            if total_trees_planted + num_trees_in_forest > max_trees:
                remaining_trees = max_trees - total_trees_planted
                width = min(width, remaining_trees // height)

            x = random.randint(0, self.size_map_x - height)
            y = random.randint(0, self.size_map_y - width)

            trees_planted_in_this_forest = 0
            for i in range(height):
                if width < 1: 
                    continue
                num_trees_in_row = random.randint(max(1,width - 3), width)
                positions_in_row = random.sample(range(width), num_trees_in_row)
                for j in positions_in_row:
                    if self.map[x + i][y + j] == " ":
                        self.addRessources(Wood(), x + i, y + j)
                        trees_planted_in_this_forest += 1

            total_trees_planted += trees_planted_in_this_forest
            if trees_planted_in_this_forest == 0:
                break

    def addTownCenter(self, towncenter): 
        center_x, center_y = self.size_map_x//2, self.size_map_y//2
        distance_from_center = random.randint(40,55)
        angle = random.uniform(0, 2 * 3.14159)
        pos1_x = int(center_x + distance_from_center * random.uniform(-1, 1))
        pos1_y = int(center_y + distance_from_center * random.uniform(-1, 1))
        pos2_x = center_x - (pos1_x - center_x)
        pos2_y = center_y - (pos1_y - center_y)
        self.addBuilding(towncenter, pos1_x, pos1_y)
        self.addBuilding(towncenter, pos2_x, pos2_y)
    
    def getMap(self):
        return self.map
    
    def getBuildings(self):
        return self.mapBuildings
    
    def getRessources(self):
        return self.mapRessources
    
    def is_free(self, x, y):
        return self.map_entities[x][y] is None
        return self.mapBuildings[x][y] is None and self.mapUnits[x][y] is None and self.mapRessources[x][y] is None
    
    def getColor(self, x, y):
        return self.lstColor[x][y]

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
        #self.mapUnits[pos[0]][pos[1]] = None
        self.map[pos[0]][pos[1]] = " "
        self.map_entities[x][y] = unit
        #self.mapUnits[x][y] = unit
        unit.setPosition(x, y)
        self.map[x][y] = "v"
        self.lstColor[x][y] = player.getColor()

    def setMapType(self, type):
        self.mapType = type

    def get_map_entities(self):
        return self.map_entities