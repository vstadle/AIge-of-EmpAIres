import pygame
import sys
import random
import time

from model.Player import Player
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Camp import Camp
from model.Villager import Villager
from model.Archer import Archer
from model.Horseman import Horseman
from model.Swordsman import Swordsman
from model.Barracks import Barracks
from model.Stable import Stable
from model.ArcheryRange import ArcheryRange

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
                    self.addBuildingInitialize(TownCenter(), posx, posy)
                    check = True

        #Placement des Barracks
        for i in range(nb):
            check = False
            while(not check):
                
                posx = towncenter.getX()
                posy = towncenter.getY()
                sizeMap = towncenter.getSizeMap()

                rx1 = random.randint(-8, 0)
                rx2 = random.randint(0, 8)
                rx = random.choice([rx1, rx2])

                ry1 = random.randint(-8, 0)
                ry2 = random.randint(0, 8)
                ry = random.choice([ry1, ry2])

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
                farm = Barracks()
                sizeMap = farm.getSizeMap()
                if(posx + sizeMap) > 120 or (posy + sizeMap) > 120:
                    continue
                for k in range(sizeMap):
                    for l in range(sizeMap):
                        if(not self.cmap.is_free(posx+k, posy+l)):
                            is_free = False
                            break
                    if(not is_free):
                        break
                if(is_free):
                    self.addBuildingInitialize(farm, posx, posy)
                    check = True

        #Placement des Stable
        for i in range(nb):
            check = False
            while(not check):
                
                posx = towncenter.getX()
                posy = towncenter.getY()
                sizeMap = towncenter.getSizeMap()

                rx1 = random.randint(-8, 0)
                rx2 = random.randint(0, 8)
                rx = random.choice([rx1, rx2])

                ry1 = random.randint(-8, 0)
                ry2 = random.randint(0, 8)
                ry = random.choice([ry1, ry2])

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
                stable = Stable()
                sizeMap = farm.getSizeMap()
                if(posx + sizeMap) > 120 or (posy + sizeMap) > 120:
                    continue
                for k in range(sizeMap):
                    for l in range(sizeMap):
                        if(not self.cmap.is_free(posx+k, posy+l)):
                            is_free = False
                            break
                    if(not is_free):
                        break
                if(is_free):
                    self.addBuildingInitialize(stable, posx, posy)
                    check = True
        
        #Placement des ArcheryRange
        for i in range(nb):
            check = False
            while(not check):
                
                posx = towncenter.getX()
                posy = towncenter.getY()
                sizeMap = towncenter.getSizeMap()

                rx1 = random.randint(-8, 0)
                rx2 = random.randint(0, 8)
                rx = random.choice([rx1, rx2])

                ry1 = random.randint(-8, 0)
                ry2 = random.randint(0, 8)
                ry = random.choice([ry1, ry2])

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
                archeryrange = ArcheryRange()
                sizeMap = farm.getSizeMap()
                if(posx + sizeMap) > 120 or (posy + sizeMap) > 120:
                    continue
                for k in range(sizeMap):
                    for l in range(sizeMap):
                        if(not self.cmap.is_free(posx+k, posy+l)):
                            is_free = False
                            break
                    if(not is_free):
                        break
                if(is_free):
                    self.addBuildingInitialize(archeryrange, posx, posy)
                    check = True

        print(self.player.name)
        for building in self.player.getBuildings():
            print(building)

    def addBuildingInitialize(self, building, x, y):
        self.player.addBuilding(building)
        self.cmap.map.addBuilding(building, x, y)
        building.setX(x)
        building.setY(y)

    def addBuilding(self, building,x,y):
        if self.player.canAffordBuilding(building):
            print("Le joueur peut construire le batiment")
            self.player.removeResourcesForBuilding(building)
            self.player.getBuildingQueue().append({"building": building, "player": self.player, "start_time": time.time(), "x": x, "y": y})

    def update_building(self):
        current_time = time.time()
        
        for item in self.player.getBuildingQueue()[:]:
            building = item["building"]
            player = item["player"]
            start_time = item["start_time"]
            building = item["building"]
            x = item["x"]
            y = item["y"]

            if current_time - start_time >= building.getBuildingTime():

                is_free = True
                for i in range(building.getSizeMap()):
                    for j in range(building.getSizeMap()):
                        if(not self.cmap.is_free(x+i, y+j)):
                            print(x+i, y+j)
                            print("Erreur de placement du batiment" , building, player)
                            is_free = False
                            break
                    if(not is_free):
                        break

                if(is_free):
                    self.player.addBuilding(building)
                    self.cmap.map.addBuilding(building, x, y)
                    building.setX(x)
                    building.setY(y)
                    self.player.getBuildingQueue().remove(item)
                    print("Le batiment est placé")
                else:
                    print()
                    #print("Erreur de placement du batiment" , building, player)
                
    def addUnitInitialize(self, unit):
        self.player.addUnit(unit)
        self.cmap.addUnits(unit, self, self.player.getBuildings()[0])

    def addUnit(self,unit, player, building):
        start_time = time.time()
        print("Ajout d'une unité à la file d'attente")
        self.player.getTrainingQueue().append({"unit": unit, "player": player, "start_time": start_time, "building": building})

    def update_training(self):
        current_time = time.time()
        #print(current_time)
        for item in self.player.getTrainingQueue()[:]:
            unit = item["unit"]
            player = item["player"]
            start_time = item["start_time"]
            building = item["building"]

            if current_time - start_time >= unit.trainingTime:
                x = building.getX()
                y = building.getY()
                building_width, building_height = building.getSizeMap(), building.getSizeMap()

                placed = False
                layer = 1

                while not placed :

                    for dx in range(-layer, layer, + 1):
                        for dy in range(-layer, layer, + 1):
                            if abs(dx) == layer or abs(dy) == layer:
                                nx, ny = x + dx, y + dy
                                if self.cmap.map.is_free(nx,ny):
                                    print("Le villageois est placé")
                                    self.cmap.map.addUnits(unit, nx, ny)
                                    self.player.addUnit(unit)
                                    placed = True
                                    break
                        if placed:
                            break
                    if not placed:
                        layer += 1

                self.player.getTrainingQueue().remove(item)


    def trainVillager(self, building):
        villager = Villager()
        if self.player.canAffordUnit(villager):
            print("Le joueur peut entrainer un villageois")
            self.player.removeResourcesForUnit(villager)
            self.addUnit(villager, self.player, building)
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