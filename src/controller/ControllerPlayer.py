import pygame
import sys
import random

from model.Player import Player
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Camp import Camp
from model.Villager import Villager
from model.Archer import Archer
from model.Horseman import Horseman
from model.Swordsman import Swordsman

class ControllerPlayer():
    
    def __init__(self, name, f, w, g, cmap):
        self.player = Player(name, f, w, g)
        self.cmap = cmap
    
    def initializeTownCenter(self, nb):

        for i in range(nb):
            check = False
            while(not check):
                towncenter = self.player.getBuildings()[0]
                posx = towncenter.getX()
                posy = towncenter.getY()
                sizeMap = towncenter.getSizeMap()

                rx = random.randint(-5, 5)
                ry = random.randint(-5, 5)

                if rx == 0:
                    rx = rx + sizeMap + 2
                elif rx > 0:
                    rx = rx + sizeMap

                if ry == 0:
                    ry = ry - sizeMap - 2
                elif ry < 0:
                    ry = ry - sizeMap

                posx = posx + rx
                posy = posy + ry

                is_free = True
                for k in range(sizeMap):
                    for l in range(sizeMap):
                        if(not self.cmap.is_free(posx+k, posy+l)):
                            is_free = False
                            break
                    if(not is_free):
                        break
                if(is_free):
                    self.cmap.addBuilding(TownCenter(), posx, posy, self)
                    check = True

        print(self.player.name)
        for building in self.player.getBuildings():
            print(building)

    def addBuilding(self, building,x,y):
        if isinstance(building, TownCenter):
            self.player.addBuilding(building)
            building.setX(x)
            building.setY(y)

        elif self.player.canAffordBuilding(building):
            self.player.addBuilding(building)
            building.setX(x)
            building.setY(y)
            self.player.removeResourcesForBuilding(building)

    def addUnit(self,unit):
        self.player.addUnit(unit)

    def trainVillager(self, building):
        villager = Villager()
        if self.player.canAffordUnit(villager):
            self.addUnit(villager)
            self.player.removeResourcesForUnit(villager)
            self.cmap.addUnits(villager, self, building)
            return 0
        return -1
    
    def trainArcher(self, building):
        archer = Archer()
        if self.player.canAffordUnit(archer):
            self.addUnit(archer)
            self.player.removeResourcesForUnit(archer)
            self.cmap.addUnits(archer, self, building)
            return 0
        return -1

    def trainHorseman(self, building):
        horseman = Horseman()
        if self.player.canAffordUnit(horseman):
            self.addUnit(horseman)
            self.player.removeResourcesForUnit(horseman)
            self.cmap.addUnits(horseman, self, building)
            return 0
        else:
            return -1
    
    def trainSwordsman(self, building):
        swordsman = Swordsman()
        if self.player.canAffordUnit(swordsman):
            self.addUnit(swordsman)
            self.player.removeResourcesForUnit(swordsman)
            self.cmap.addUnits(swordsman, self, building)
            return 0
        else:
            return -1

    def getPlayer(self):
        return self.player