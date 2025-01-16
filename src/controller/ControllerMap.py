import pygame
import sys
import random
import math
import time
import webbrowser
import os

from model.Map import Map, MapType
from model.Player import Player
from model.TownCenter import TownCenter
from model.Villager import Villager
from model.Archer import Archer
from model.Horseman import Horseman
from model.Swordsman import Swordsman
from web.generate_html import generateHtml

class ControllerMap():
    def __init__(self, size_map_x, size_map_y):
        self.size_map_x = size_map_x
        self.size_map_y = size_map_y
        self.map = Map(self.size_map_x, self.size_map_y)
        self.pos_x = 0
        self.pos_y = 0
        self.training_queue = []
        self.lstPlayers = []
        self.paused = False
        self.tab_pressed = False
        

    def reset(self, map):
        self.map = map
        self.pos_x = 0
        self.pos_y = 0
        self.training_queue = []
        self.lstPlayers = []
        self.size_map_x = map.size_map_x
        self.size_map_y = map.size_map_y

    def reset_map_size(self, size_x, size_y):
       self.map = Map(size_x, size_y)
       self.size_map_x = size_x
       self.size_map_y = size_y

    def setLstPlayers(self, lstPlayers):
        self.lstPlayers = lstPlayers

    def placementTownCenter(self, nbPlayer, lstPlayers):
        position = []
        center_x, center_y = self.map.size_map_x//2, self.map.size_map_y//2
        
        radius = 40
        k = random.uniform(0, 1) * 2 * math.pi 
        for i in range(nbPlayer):
            x = radius * math.cos(2 * math.pi * i / nbPlayer)
            y = radius * math.sin(2 * math.pi * i / nbPlayer)
            position.append((x * math.cos(k) - y * math.sin(k) + center_x, 
                             x * math.sin(k) + y * math.cos(k) + center_y))

        cpt = 0
        for i in position:
            self.map.addBuilding(TownCenter(), int(i[0]), int(i[1]), lstPlayers[cpt].getPlayer())
            lstPlayers[cpt].addBuildingInitialize(TownCenter(), int(i[0]), int(i[1]))
            cpt += 1

    def genRessources(self, map_type):
        if map_type == MapType.GENEROUS_RESOURCES:
            self.map.generateGenerousResources()
        elif map_type == MapType.CENTER_RESOURCES:
            self.map.generateCenterResources()
        self.map.generateForest()

    def getMap(self):
        return self.map
    
    def is_free(self, x, y):
        return self.map.is_free(x, y)
    
    def rmUnit(self, unit):
        self.map.rmUnit(unit)
    
    def rmBuilding(self, building):
        self.map.rmBuilding(building)
    
    def rmRessource(self, ressource):
        self.map.rmRessource(ressource)