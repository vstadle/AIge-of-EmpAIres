from TownCenter import TownCenter 
from Farm import Farm
from Keep import Keep
from Barracks import Barracks
from ArcheryRange import ArcheryRange
from Stable import Stable
from House import House
from Camp import Camp
from Ressources import Ressources
from Gold import Gold
from Food import Food
from Wood import Wood

import random

class Map():

    def __init__(self):
        self.map = [[" " for x in range(120)] for y in range(120)]
        self.players = []
        self.buildings = []

    def generateSizeRessources(self, r):
        
        x = 40
        y = 40

        r_x = random.randint(1, 4)
        r_y = random.randint(1,3)
        for i in range(r_x):
            for j in range(r_y):
                self.addRessources(r, x + i, y+j)


    def addPlayer(self, player):
        self.players.append(player)

    def printMap(self):
        self.map[0][0] = "R"
        for i in range(35, 70):
            for j in range(35, 70):
                print(self.map[i][j], end=" ")
            print()

    def addRessources(self, Ressources, x,y):
        letter = "P"
        if(isinstance(Ressources,Food)):
            letter = "F"
        elif(isinstance(Ressources,Wood)):
            letter = "W"
        elif(isinstance(Ressources,Gold)):
            letter = "G"
        self.map[x][y] = letter 

    def addBuilding(self, building, x, y):
        letter = "P"
        if(isinstance(building, Farm)):
            letter = "F"
        elif(isinstance(building, TownCenter)):
            letter = "T"
        elif(isinstance(building, Barracks)):
            letter = "B"
        elif(isinstance(building, ArcheryRange)):
            letter = "A"
        elif(isinstance(building, Stable)):
            letter = "S"
        elif(isinstance(building, House)):
            letter = "H"
        elif(isinstance(building, Keep)):
            letter = "K"
        elif(isinstance(building, Camp)):
            letter = "C"
        
        self.buildings.append(building)
        for i in range (building.sizeMap):
            for j in range (building.sizeMap):
                self.map[x+i][y+j] = letter
