import curses
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

    def generateSizeRessources(self, r, x, y):
        
        r_x = random.randint(1, 5)
        r_y = random.randint(1,5)
        for i in range(r_x):
            for j in range(r_y):
                self.addRessources(r, x + i, y+j)


    def addPlayer(self, player):
        self.players.append(player)

    def printMap(self):
        self.map[0][0] = 'R'
        for i in range(35, 70):
            for j in range(35, 70):
                print(self.map[i][j], end=' ')
            print()

    def draw_map(self, win):

        win.clear()

        for i in range(37):
                win.addch(0,i,'-')
        
        for j in range(37):
            win.addch(37,j,'-')

        for i in range(1, 37):
            win.addch(i, 0, '|')
            win.addch(i, 36, '|')
        '''
        for i in range(35, 70):
            for j in range(35, 70):
                win.addch(i - 35, j - 35, self.map[i][j])
        '''
        
        win.refresh()

        #win.getch()

    def addRessources(self, Ressources, x,y):
        letter = 'P'
        if(isinstance(Ressources,Food)):
            letter = 'F'
        elif(isinstance(Ressources,Wood)):
            letter = 'W'
        elif(isinstance(Ressources,Gold)):
            letter = 'G'
        self.map[x][y] = letter 

    def addBuilding(self, building, x, y):
        letter = 'P'
        if(isinstance(building, Farm)):
            letter = 'F'
        elif(isinstance(building, TownCenter)):
            letter = 'T'
        elif(isinstance(building, Barracks)):
            letter = 'B'
        elif(isinstance(building, ArcheryRange)):
            letter = 'A'
        elif(isinstance(building, Stable)):
            letter = 'S'
        elif(isinstance(building, House)):
            letter = 'H'
        elif(isinstance(building, Keep)):
            letter = 'K'
        elif(isinstance(building, Camp)):
            letter = 'C'
        
        self.buildings.append(building)
        for i in range (building.sizeMap):
            for j in range (building.sizeMap):
                self.map[x+i][y+j] = letter
    def generateForest(self):
        max_percentage_wood = 0.1 
        total_cells = 120 * 120
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

            x = random.randint(0, 120 - height)
            y = random.randint(0, 120 - width)

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
