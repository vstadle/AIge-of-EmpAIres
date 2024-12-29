import pygame
import sys
import random
import time
import logging

from controller import A_Star
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
from model.Gold import Gold
from model.Wood import Wood
from logs.logger import logs

class ControllerPlayer():
    
    def __init__(self, player, cmap):
        self.player = player
        self.cmap = cmap
        self.queueCollect = []
        self.queueMoving = []
        self.queueConstruct = []
    
    @classmethod
    def from_saved(cls,player,cmap):
        return cls(player, cmap)
    
    @classmethod
    def from_new(cls, name, f, w, g ,cmap):
        return cls(Player(name, f, w, g), cmap)

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

        logs(self.player.name, level=logging.INFO)
        for building in self.player.getBuildings():
            logs(building.__str__(), level=logging.INFO)

    def addBuildingInitialize(self, building, x, y):
        self.player.addBuilding(building)
        self.cmap.map.addBuilding(building, x, y, self.player)
        building.setX(x)
        building.setY(y)

    def addBuilding(self, building,x,y):

        if self.player.canAffordBuilding(building):
            is_free = True
            if x + building.getSizeMap() < 120 or y + building.getSizeMap() < 120:
                for i in range (building.getSizeMap()):
                    for j in range (building.getSizeMap()):
                        if not self.cmap.is_free(x+i, y+j):
                            is_free = False
                            break
                    if not is_free:
                        break
                if is_free:
                    logs(building.__str__() + " add to building queue", level=logging.INFO)
                    self.player.removeResourcesForBuilding(building)
                    self.player.getBuildingQueue().append({"nbVillager": 0, "building": building, "player": self.player, "start_time": time.time(), "x": x, "y": y})

    def update_building(self):
        current_time = time.time()
        
        for item in self.player.getBuildingQueue()[:]:

            building = item["building"]
            nbVillager = item["nbVillager"]
            player = item["player"]
            start_time = item["start_time"]
            building = item["building"]
            x = item["x"]
            y = item["y"]

            qConstruct = self.queueConstruct[:]
            bTime = building.getBuildingTime()
            
            #calcul du building time par rapport au nombre de villageois
            bTime = (3*bTime)/(nbVillager + 2)

            if current_time - start_time >= bTime:

                is_free = True
                for i in range(building.getSizeMap()):
                    for j in range(building.getSizeMap()):
                        if(not self.cmap.is_free(x+i, y+j)):
                            s = f"{x+i} {y+j}"
                            logs(s, level=logging.ERROR)
                            logs("Error  with building placement : "+ building.__str__(), level=logging.ERROR)
                            is_free = False
                            break
                    if(not is_free):
                        break

                if(is_free):
                    player.addBuilding(building)
                    self.cmap.map.addBuilding(building, x, y, player)
                    building.setX(x)
                    building.setY(y)
                    self.player.getBuildingQueue().remove(item)

                    #enleve chaque element de queueConstruct qui a construit le batment
                    for element in qConstruct:
                        if element["building"] == building:
                            element["Villager"].action = None
                            self.queueConstruct.remove(element)

                    logs(building.__str__() + " is placed", level=logging.INFO)
                else:
                    print()
                    #print("Erreur de placement du batiment" , building, player)
                
    def addUnitInitialize(self, unit, building):
        x = building.getX()
        y = building.getY()

        placed = False
        layer = 1

        while not placed :

            for dx in range(-layer, layer, + 1):
                for dy in range(-layer, layer, + 1):
                    if abs(dx) == layer or abs(dy) == layer:
                        nx, ny = x + dx, y + dy
                        if self.cmap.map.is_free(nx,ny):
                            self.cmap.map.addUnits(unit, nx, ny, self.player)
                            self.player.addUnit(unit)
                            placed = True
                            break
                if placed:
                    break
            if not placed:
                layer += 1

    def addUnit(self,unit, building):
        start_time = time.time()
        logs(unit.__str__() + " add to training queue", level=logging.INFO)
        self.player.getTrainingQueue().append({"unit": unit, "player": self.player, "start_time": start_time, "building": building})

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
                                    self.cmap.map.addUnits(unit, nx, ny, player)
                                    self.player.addUnit(unit)
                                    placed = True
                                    logs(unit.__str__() + " is placed", level=logging.INFO)
                                    break
                        if placed:
                            break
                    if not placed:
                        layer += 1

                self.player.getTrainingQueue().remove(item)


    def trainVillager(self, building):
        villager = Villager()
        if self.player.canAffordUnit(villager):
            self.player.removeResourcesForUnit(villager)
            self.addUnit(villager, building)
            return 0
        return -1
    
    def trainArcher(self, building):
        archer = Archer()
        if self.player.canAffordUnit(archer):
            self.addUnit(archer, building)
            self.player.removeResourcesForUnit(archer)
            return 0
        return -1

    def trainHorseman(self, building):
        horseman = Horseman()
        if self.player.canAffordUnit(horseman):
            self.addUnit(horseman, building)
            self.player.removeResourcesForUnit(horseman)
            return 0
        else:
            return -1
    
    def trainSwordsman(self, building):
        swordsman = Swordsman()
        if self.player.canAffordUnit(swordsman):
            self.addUnit(swordsman, building)
            self.player.removeResourcesForUnit(swordsman)
            return 0
        else:
            return -1

    def collectResources(self, villager, ressource, unit_x, unit_y):
        can_collect = False

        # Calcul des distances en X et Y
        distance_x = abs(ressource.getX() - unit_x)
        distance_y = abs(ressource.getY() - unit_y)

        if distance_x <= 1 and distance_y <= 1:
            if villager.carryingType == None:
                if isinstance(ressource, Gold):
                    villager.carryingType = "Gold"
                    can_collect = True
                elif isinstance(ressource, Wood):
                    villager.carryingType = "Wood"
                    can_collect = True
            elif isinstance(ressource, Gold) and villager.carryingType == "Gold":
                can_collect = True
            elif isinstance(ressource, Wood) and villager.carryingType == "Wood":
                can_collect = True
            
            if can_collect:
                #Le villageois est à la bonne distance pour collecter des ressources
                logs("Villager is collecting resources", level=logging.INFO)
                start_time = time.time()
                villager.action = "collect"
                self.queueCollect.append({"villager": villager, "start_time": start_time, "ressource": ressource})
                logs("Villager is collecting resources", level=logging.INFO)
        else:
            logs("Villager is too far to collect resources", level=logging.INFO)
    
    def updating_collect(self):
        current_time = time.time()
        #print(current_time)
        for item in self.queueCollect[:]:
            villager = item["villager"]
            start_time = item["start_time"]
            ressource = item["ressource"]
            if current_time - start_time >= villager.collectPerSecond:
                logs("Le villageois peut collecter des ressources", level=logging.INFO)
                if(villager.canCollectRessources() and ressource.capacity > 0):
                    villager.collect(ressource)
                    logs("Villageois collecte des ressources", level=logging.INFO)
                    logs(villager.carrying.__str__(), level=logging.INFO)
                    self.queueCollect.remove(item)
                    start_time = time.time()
                    if(ressource.capacity <= 0):
                        logs("Ressource is empty", level=logging.INFO)
                        self.cmap.map.mapRessources[ressource.getX()][ressource.getY()] = None
                        self.cmap.map.map[ressource.getX()][ressource.getY()] = " "
                    else:
                        self.queueCollect.append({"villager": villager, "start_time": start_time, "ressource": ressource})
                else:
                    logs("Villageois ne peut pas collecter de ressources", level=logging.INFO)
                    self.queueCollect.remove(item)

    def villagerConstructBuilding(self, villager, building, unit_x, unit_y):

        building_queue = self.player.getBuildingQueue()
        #trouver le batiment dans la buildingQueue
        item = next((item for item in building_queue if item["Building"] == building), None)

        #si le batiment choisi est dans buildingQueue
        if item is not None:

            building_x = building.getX()
            building_y = building.getY()
            building_size = building.getSizeMap()

            #verification de la distance entre le villageois et le batiment
            is_near_building = False
            for i in range(building_size):
                for j in range(building_size):
                    distance_x = abs((building_x + i) - unit_x)
                    distance_y = abs((building_y + j) - unit_y)
                    if (distance_x == 1 and distance_y == 0) or (distance_x == 0 and distance_y == 1):
                        is_near_building = True
                        break
                if is_near_building:
                    break
            
            #ajout du villageois dans queueConstruct
            #et +1 dans "nbVillager" dans l'item qui contient le batiment dans buildingQueue 
            if is_near_building:
                villager.action = "build"
                self.queueConstruct.append({"villager": villager,  "building": building})
                item["nbVillager"] += 1 
                logs("Villager is building", level=logging.INFO)
            else:
                logs("Villager is too far to build", level=logging.INFO)
        else:
            logs("Building is not in the Building queue", level=logging.INFO)
            




    def move(self, unit, x, y):
        start = unit.getPosition()
        end = (x,y)
        logs("Unit is moving", level=logging.INFO)
        chemin = A_Star.a_star(self.cmap.map, start, end)
        if chemin is None:
            logs("No path found", level=logging.INFO)
        else:
            chemin.pop(0)
            logs("Chemin : " + chemin.__str__(), level=logging.INFO)
            start_time = time.time()
            self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})

    def updating_moving(self):
        current_time = time.time()
        for item in self.queueMoving[:]:
            unit = item["unit"]
            start_time = item["start_time"]
            chemin = item["chemin"]
            if current_time - start_time >= unit.speed:
                #logs("Unit is moving", level=logging.INFO)
                case = chemin[0]
                x = case[0]
                y = case[1]
                pos = unit.getPosition()
                #logs("Position : " + pos.__str__(), level=logging.INFO)
                #logs("Next_position : " + case.__str__(), level=logging.INFO)
                #logs("Next_position : " + self.cmap.map.map[x][y], level=logging.INFO)
                #logs("Current Position : " + self.cmap.map.map[pos[0]][pos[1]], level=logging.INFO)
                if self.cmap.map.is_free(x,y):
                    self.queueMoving.remove(item)
                    self.cmap.map.moveUnit(unit, x, y, self.player)
                    chemin.pop(0)
                    start_time = time.time()
                    if len(chemin) > 0:
                        self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})
                else:
                    #logs("Unit can't move", level=logging.INFO)
                    self.queueMoving.remove(item)
                    chemin = A_Star.a_star(self.cmap.map, (unit.getPosition()), chemin[len(chemin)-1])
                    start_time = time.time()
                    self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})



    def getPlayer(self):
        return self.player