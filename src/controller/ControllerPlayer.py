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
    
    def addBuilding(self, building):
        self.player.addBuilding(building)

    def addUnit(self,unit):
        self.player.addUnit(unit)

    def getPlayer(self):
        return self.player