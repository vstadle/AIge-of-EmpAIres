from TownCenter import TownCenter 
from Farm import Farm
from Keep import Keep
from Barracks import Barracks
from ArcheryRange import ArcheryRange
from Stable import Stable
from House import House
from Camp import Camp



class Map():

    def __init__(self):
        self.map = [[" " for x in range(120)] for y in range(120)]
        self.players = []
        self.buildings = []

    def addPlayer(self, player):
        self.players.append(player)

    def printMap(self):
        i = 35
        j = 35
        for i in range(50):
            for j in range(50):
                print(self.map[i][j], end=" ")
            print()

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
