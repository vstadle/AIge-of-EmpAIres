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


import random
import curses
import pygame
class MapType():
    GENEROUS_RESOURCES = 1
    CENTER_RESOURCES = 2
class Map():
    def __init__(self,map_type):

        #Matrice de 120x120 qui va contenir les batiments
        self.mapBuildings = [[None for x in range(120)] for y in range(120)]

        #Matrice de 120x120 qui va contenir les ressources
        self.mapRessources = [[None for x in range(120)] for y in range(120)]

        #Matrice de 120x120 qui va contenir les unités
        self.mapUnits = [[None for x in range(120)] for y in range(120)]

        #Listes des couleurs
        self.lstColor= [[None for x in range(120)] for y in range(120)]

        self.map = [[" " for x in range(120)] for y in range(120)]
        self.map[0][0] = 'R'
        self.map[119][119] = 'R'
        
    
    def generateGenerousResources(self):
        max_percentage_gold = 0.01
        max_percentage_food = 0.01
        total_cells = 120*120
        max_gold = max_percentage_gold * total_cells
        max_food = max_percentage_food * total_cells
        food_planted = 0
        gold_planted = 0
        while (gold_planted < max_gold):
            x = random.randint(0,119)
            y = random.randint(0,119)
            if(self.map[x][y]== " "):
                self.addRessources(Gold(), x, y)
                gold_planted+=1
        while (food_planted < max_food):
            x = random.randint(0,119)
            y = random.randint(0,119)
            if(self.map[x][y]== " "):
                self.addRessources(Food(), x, y)
                food_planted+=1




    def generateCenterResources(self):
        center_x, center_y = 60, 60 
        width = random.randint(3, 7)  
        height = random.randint(3, 7)  

        start_x = center_x - width // 2
        start_y = center_y - height // 2
        for dx in range(width): 
            for dy in range(height):
                x = start_x + dx
                y = start_y + dy
                if 0 <= x < 120 and 0 <= y < 120:
                    self.addRessources(Gold(), x, y)


    def generateSizeRessources(self, r, x, y):
        
        r_x = random.randint(1, 5)
        r_y = random.randint(1,5)
        for i in range(r_x):
            for j in range(r_y):
                self.addRessources(r, x + i, y+j)

    def draw_map(self, win,pos_x,pos_y):

        for i in range(20):  # Limite pour le nombre de lignes à dessiner
            for j in range(20):  # Limite pour le nombre de colonnes à dessiner
                # Supposons que self.map contient des caractères pour représenter la carte
                tile = self.map.map[(pos_y + i) % self.map.height][(pos_x + j) % self.map.width]
                # Dessiner le tile sur l'écran
                # Utilisez pygame.draw ou autre méthode selon votre implémentation

        pygame.display.flip()  # Met à jour l'affichage
        #win.getch()

    def addRessources(self, Ressources, x,y):
        self.mapRessources[x][y] = Ressources
        self.map[x][y] = Ressources.letter

    def addBuilding(self, building, x, y, player):
        building.setX(x)
        building.setY(y)
        cpt = 0
        for i in range(building.sizeMap):
            cpt += 1
            for j in range(building.sizeMap):
                self.mapBuildings[x + i][y + j] = building
                self.map[x + i][y + j] = building.letter
                self.lstColor[x + i][y + j] = player.getColor()


    def addUnits(self, units, x, y, player):
        self.mapUnits[x][y] = units
        self.map[x][y] = units.letter
        self.lstColor[x][y] = player.getColor()
        print(self.lstColor[x][y])

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

    def addTownCenter(self, towncenter): 
        center_x, center_y = 60, 60
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
        return self.map[x][y] == " "
    
    def getColor(self, x, y):
        return self.lstColor[x][y]
