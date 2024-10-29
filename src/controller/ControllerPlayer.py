import pygame
import sys
import random
from model.Player import Player
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Camp import Camp

class ControllerPlayer():
    
    def __init__(self, name, f, w, g):
        self.player = Player(name, f, w, g)
        self.player.addBuilding(TownCenter())
        self.player.addBuilding(Farm())
        self.player.addBuilding(Camp())
    
    def addBuilding(self, building,x,y):
        if self.player.canAffordBuilding(building):
            self.player.addBuilding(building,x,y)
            self.player.removeResourcesForBuilding(building)

    def addUnit(self,unit):
        if self.player.canAffordUnit(unit):
            self.player.addUnit(unit)
            self.player.removeResourcesForUnit(unit)

        self.player.addUnit(unit)

    def getPlayer(self):
        return self.player