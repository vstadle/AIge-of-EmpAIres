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
from model.Buildings import Buildings
from model.House import House

from model.Units import Units

class ControllerPlayer():
    
    def __init__(self, player, cmap):
        self.player = player
        self.cmap = cmap
        self.queueCollect = []
        self.queueMoving = []
        self.queueAttack = []
    
    @classmethod
    def from_saved(cls,player,cmap):
        return cls(player, cmap)
    
    @classmethod
    def from_new(cls, name, f, w, g ,cmap):
        return cls(Player(name, f, w, g), cmap)

    def initializeTownCenter(self, nb):

        for i in range(nb):
            #Placement du TownCenter
            position = self.findPlaceForBuildings(TownCenter())
            if position is not None:
                self.addBuildingInitialize(TownCenter(), position[0], position[1])

        position = None

        #Placement des Barracks
        for i in range(nb):
            position = self.findPlaceForBuildings(Barracks())
            if position is not None:
                self.addBuildingInitialize(Barracks(), position[0], position[1])


        #Placement des Stable
        for i in range(nb):
            position = self.findPlaceForBuildings(Stable())
            if position is not None:
                self.addBuildingInitialize(Stable(), position[0], position[1])
        
        #Placement des ArcheryRange
        for i in range(nb):
            position = self.findPlaceForBuildings(ArcheryRange())
            if position is not None:
                self.addBuildingInitialize(ArcheryRange(), position[0], position[1])

        '''
        logs(self.player.name, level=logging.INFO)
        for building in self.player.getBuildings():
            logs(building.__str__(), level=logging.INFO)
        '''

    def findPlaceForBuildings(self, building):
        """
        Trouve une position libre pour placer un nouveau bâtiment avec une case d'écart minimum
        de chaque côté par rapport aux autres bâtiments et en laissant un couloir autour du Town Center.

        Args:
            building (Building): Le bâtiment à placer.

        Returns:
            tuple: (x, y) coordonnées du coin supérieur gauche où placer le bâtiment,
                ou None si aucun emplacement n'est trouvé.
        """
        main_building = None
        if len(self.player.buildings) > 0:
            main_building = self.player.buildings[0]  # On suppose que le premier bâtiment est le Town Center

        if main_building is not None:
            town_center_x = main_building.x
            town_center_y = main_building.y
            town_center_size = main_building.sizeMap
            building_size = building.sizeMap
            radius = 5

            while radius <= max(self.cmap.map.size_map_x, self.cmap.map.size_map_y):
                for i in range(town_center_x - radius, town_center_x + radius + 1):
                    for j in range(town_center_y - radius, town_center_y + radius + 1):
                        # Vérifie si les coordonnées sont dans les limites de la carte
                        if 0 <= i < self.cmap.map.size_map_x and 0 <= j < self.cmap.map.size_map_y:
                            # Vérifie si l'emplacement est libre pour le bâtiment
                            is_free = True
                            for k in range(-1, building_size + 1):  # Inclut une case autour du bâtiment
                                for l in range(-1, building_size + 1):
                                    check_x = i + k
                                    check_y = j + l
                                    if (
                                        0 <= check_x < self.cmap.map.size_map_x
                                        and 0 <= check_y < self.cmap.map.size_map_y
                                    ):
                                        # Vérifie qu'aucune case (y compris autour du bâtiment) n'est occupée
                                        if self.cmap.map.map[check_x][check_y] != " ":
                                            is_free = False
                                            break
                                    else:
                                        is_free = False  # Si hors limites, emplacement invalide
                                        break
                                if not is_free:
                                    break
                            
                            # Vérifie que le couloir autour du Town Center est respecté
                            if is_free:
                                for k in range(-1, town_center_size + 1):
                                    for l in range(-1, town_center_size + 1):
                                        # Vérifie les cases autour du Town Center
                                        corridor_x = town_center_x + k
                                        corridor_y = town_center_y + l
                                        if (
                                            0 <= corridor_x < self.cmap.map.size_map_x
                                            and 0 <= corridor_y < self.cmap.map.size_map_y
                                            and abs(corridor_x - (i + building_size // 2)) <= 1
                                            and abs(corridor_y - (j + building_size // 2)) <= 1
                                        ):
                                            if self.cmap.map.map[corridor_x][corridor_y] != " ":
                                                is_free = False
                                                break
                                    if not is_free:
                                        break

                            if is_free:
                                return i, j  # Retourne les coordonnées du coin supérieur gauche

                    radius += 1

        return None  # Aucun emplacement trouvé

    def addBuildingInitialize(self, building, x, y):
        self.player.addBuilding(building)
        self.cmap.map.addBuilding(building, x, y, self.player)
        building.setX(x)
        building.setY(y)


    '''Fonction pour contruire un batiment
    Paramètres : le batiment à construire, les coordonnées x et y
    Renvoie : 
            0 si le batiment est construit
            1 si le joueur n'a pas assez de ressources
            -1 si le batiment est trop grand
            2 si le joueur n'a pas de villageois disponibles'''
    
    def addBuilding(self, building,x,y):

        if self.player.canAffordBuilding(building):
            is_free = True
            if x + building.getSizeMap() < self.cmap.map.size_map_x or y + building.getSizeMap() < self.cmap.map.size_map_y:
                for i in range (building.getSizeMap()):
                    for j in range (building.getSizeMap()):
                        if not self.cmap.is_free(x+i, y+j):
                            is_free = False
                            break
                    if not is_free:
                        break
                if is_free:

                    cpt = 0
                    lstVillager = []
                    for villager in self.player.units:
                        if isinstance(villager, Villager) and villager.action is None and villager.carrying == 0:
                            cpt += 1
                            lstVillager.append(villager)

                    #logs(self.player.name + " : " + str(cpt) + " villagers available", level=logging.INFO)

                    if cpt == 0:
                        #logs(self.player.name + " : No villager available", level=logging.INFO)
                        return 2
                    
                    # Determine available tiles around the building
                    available_tiles = []
                    for dx in range(-1, building.getSizeMap() + 1):
                        for dy in range(-1, building.getSizeMap() + 1):
                            nx, ny = x + dx, y + dy
                            if self.cmap.is_free(nx, ny):
                                available_tiles.append((nx, ny))

                    #logs(self.player.name + " : Available tiles around the building : " + available_tiles.__str__(), level=logging.INFO)

                    taille = min(len(lstVillager), len(available_tiles))

                    tempLstVillager = []

                    for i in range(taille):
                        villager = lstVillager[i]
                        check = self.move(villager, available_tiles[i][0], available_tiles[i][1])
                        if check != -1:
                            tempLstVillager.append(villager)
                            villager.action = "build"

                    if len(tempLstVillager) == 0:
                        #logs(self.player.name + " : No villager can move", level=logging.INFO)
                        return 2

                    if len(tempLstVillager) == 1:
                        buildingTime = building.getBuildingTime()
                    
                    elif len(tempLstVillager) > 1:
                        buildingTime = (3*building.getBuildingTime()) / (cpt + 2)

                    logs(self.player.name + " : " + building.__str__() + " add to building queue buildingTime = " + str(buildingTime) + " with " + str(len(tempLstVillager)) + " villagers", level=logging.INFO)
                    self.player.removeResourcesForBuilding(building)
                    self.cmap.map.addBuildingTemp(building, x, y)
                    self.player.getBuildingQueue().append({"building": building, "player": self.player, "start_time": time.time(), "buildingTime": buildingTime, 'lstVillagers': tempLstVillager, "x": x, "y": y})

                    return 0
            else:
                logs(self.player.name + " : Building is too big", level=logging.INFO)
                return -1    
        else:
            return 1

    def update_building(self):
        current_time = time.time()
        
        for item in self.player.getBuildingQueue()[:]:
            building = item["building"]
            player = item["player"]
            start_time = item["start_time"]
            buildingTime = item["buildingTime"]
            lstVillagers = item["lstVillagers"]
            building = item["building"]
            x = item["x"]
            y = item["y"]

            if current_time - start_time >= buildingTime:

                is_free = True
                for i in range(building.getSizeMap()):
                    for j in range(building.getSizeMap()):
                        if(not self.cmap.is_free(x+i, y+j)):
                            s = f"{x+i} {y+j}"
                            logs(s, level=logging.ERROR)
                            logs(self.player.name + " : Error  with building placement : "+ building.__str__(), level=logging.ERROR)
                            is_free = False
                            break
                    if(not is_free):
                        break

                if(is_free):
                    if isinstance(building, Farm):
                        player.food += building.food
                        logs(self.player.name + " : Farm build, add " + str(building.food) + " to food player", level=logging.INFO)
                    player.addBuilding(building)
                    self.cmap.map.addBuilding(building, x, y, player)
                    building.setX(x)
                    building.setY(y)
                    self.player.getBuildingQueue().remove(item)
                    logs(self.player.name + " : " + building.__str__() + " is placed", level=logging.INFO)
                    for villager in lstVillagers:
                        for item in self.queueMoving[:]:
                            if item["unit"] == villager:
                                self.queueMoving.remove(item)
                        villager.action = None

                    return 0
                else:
                    print()
                    #print("Erreur de placement du batiment" , building, player)
        return -1
                
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
        logs(self.player.name + " : " + unit.__str__() + " add to training queue", level=logging.INFO)
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
                                if self.cmap.map.is_free(nx,ny) and self.cmap.map.map[nx][ny] == " ":
                                    self.cmap.map.addUnits(unit, nx, ny, player)
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
        if self.player.population < 200 and (len(self.player.units)+len(self.player.training_queue)) < self.player.population:
            if self.player.canAffordUnit(villager):
                self.player.removeResourcesForUnit(villager)
                self.addUnit(villager, building)
                return 0
            else :
                return 1
        else:
            #logs(self.player.name + " : Population is full", level=logging.INFO)
            return -1
    
    def trainArcher(self, building):
        archer = Archer()
        if self.player.population < 200 and (len(self.player.units)+len(self.player.training_queue)) < self.player.population:
            if self.player.canAffordUnit(archer):
                self.addUnit(archer, building)
                self.player.removeResourcesForUnit(archer)
                return 0
            else:
                return 1
        else:
            #logs(self.player.name + " : Population is full", level=logging.INFO)
            return -1

    def trainHorseman(self, building):
        horseman = Horseman()
        if self.player.population < 200 and (len(self.player.units)+len(self.player.training_queue)) < self.player.population:
            if self.player.canAffordUnit(horseman):
                self.addUnit(horseman, building)
                self.player.removeResourcesForUnit(horseman)
                return 0
            else :
                return 1
        else:
            #logs(self.player.name + " : Population is full", level=logging.INFO)
            return -1
    
    def trainSwordsman(self, building):
        swordsman = Swordsman()
        if self.player.population < 200 and (len(self.player.units)+len(self.player.training_queue)) < self.player.population:
            if self.player.canAffordUnit(swordsman):
                self.addUnit(swordsman, building)
                self.player.removeResourcesForUnit(swordsman)
                return 0
            else :
                return 1
        else:
            #logs(self.player.name + " : Population is full", level=logging.INFO)
            return -1

    def collectResources(self, villager, ressource):
        unit_x = villager.x
        unit_y = villager.y
        can_collect = False

        # Calcul des distances en X et Y
        distance_x = abs(ressource.getX() - unit_x)
        distance_y = abs(ressource.getY() - unit_y)

        if distance_x <= 1.25 and distance_y <= 1.25:
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
                logs(self.player.name + " : Villager is collecting resources", level=logging.INFO)
                start_time = time.time()
                villager.action = "collect"
                self.queueCollect.append({"villager": villager, "start_time": start_time, "ressource": ressource})
                #logs(self.player.name + " : Villager is collecting resources", level=logging.INFO)
        else:
            logs(self.player.name + " : Villager is too far to collect resources", level=logging.INFO)
    
    def updating_collect(self):
        current_time = time.time()
        #print(current_time)
        for item in self.queueCollect[:]:
            villager = item["villager"]
            start_time = item["start_time"]
            ressource = item["ressource"]
            if current_time - start_time >= villager.collectPerSecond:
                #logs(self.player.name + " : villager can collect ressources", level=logging.INFO)
                if(villager.canCollectRessources() and ressource.capacity > 0):
                    villager.collect(ressource)
                    #logs(self.player.name + " : villager collect ressources", level=logging.INFO)
                    #logs(villager.carrying.__str__(), level=logging.INFO)
                    self.queueCollect.remove(item)
                    start_time = time.time()
                    if(ressource.capacity <= 0):
                        logs(self.player.name + " : Ressource is empty", level=logging.INFO)

                        self.cmap.map.map_entities[ressource.getX()][ressource.getY()] = None
                        #self.cmap.map.mapRessources[ressource.getX()][ressource.getY()] = None
                        self.cmap.map.map[ressource.getX()][ressource.getY()] = " "
                        villager.action = None
                    else:
                        self.queueCollect.append({"villager": villager, "start_time": start_time, "ressource": ressource})
                else:
                    logs(self.player.name + " : Villagers can't collect ressources", level=logging.INFO)
                    villager.action = None
                    self.queueCollect.remove(item)
                    return 3

    def moveWithChemin(self, unit, chemin):
        if chemin is not None:
            start = unit.getPosition()
            end = chemin[len(chemin)-1]
            
            #logs(self.player.name + " : " + str(unit) + " is moving", level=logging.INFO)
            if unit.action is None:
                unit.action = "move"
            start_time = time.time()
            self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})
            return 0
        else:
            #logs(self.player.name + " : " + str(unit) + " No path found", level=logging.INFO)
            if unit.action != "build":
                unit.action = None
            return -1

    def move(self, unit, x, y):
        start = unit.getPosition()
        end = (x,y)
        #logs(self.player.name + " : " + str(unit) + " is moving", level=logging.INFO)
        chemin = A_Star.a_star(self.cmap.map, start, end)
        if unit.action is None:
            unit.action = "move"
        if chemin is None:
            #logs(self.player.name + " : " + str(unit) + " No path found", level=logging.INFO)
            if unit.action != "build":
                unit.action = None
            return -1
        else:
            chemin.pop(0)
            #logs("Chemin : " + chemin.__str__(), level=logging.INFO)
            start_time = time.time()
            self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})
            return 0


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
                if self.cmap.map.is_free(x,y) and self.cmap.map.map[x][y] == " ":
                    self.queueMoving.remove(item)
                    self.cmap.map.moveUnit(unit, x, y, self.player)
                    chemin.pop(0)
                    start_time = time.time()
                    if len(chemin) > 0:
                        self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})
                    else:
                        #logs(self.player.name + " : " + str(unit) + " is arrived", level=logging.INFO)
                        if unit.action != "build":
                            unit.action = None
                else:
                    #logs("Case :" + self.cmap.map.map[x][y], level=logging.INFO)
                    #logs("Unit position :" + str(unit.getPosition()), level=logging.INFO)
                    #logs("Unit can't move", level=logging.INFO)
                    #logs("Path : " + chemin.__str__(), level=logging.INFO)
                    self.queueMoving.remove(item)
                    chemin = A_Star.a_star(self.cmap.map, (unit.getPosition()), chemin[len(chemin)-1])
                    if chemin is None:
                        #logs(self.player.name + " : " + str(unit) + " No path found", level=logging.ERROR)
                        if unit.action != "build":
                            unit.action = None
                        return -1
                    else:
                        chemin.pop(0)
                        #logs("New path : " + chemin.__str__(), level=logging.INFO)
                        start_time = time.time()
                        if len(chemin) > 0:
                            case = chemin[0]
                            x = case[0]
                            y = case[1]
                            if len(chemin) == 1:
                                #logs(self.player.name + " : " + str(unit) + " is block", level=logging.ERROR)
                                unit.action = None
                            else:
                                if self.cmap.map.is_free(x,y) and self.cmap.map.map[x][y] == " ":
                                    self.cmap.map.moveUnit(unit, x, y, self.player)
                                    chemin.pop(0)
                                    if len(chemin) > 0:
                                        self.queueMoving.append({"unit": unit, "start_time": start_time, "chemin": chemin})
                                    else:
                                        #logs(self.player.name + " : " + str(unit) + " is arrived", level=logging.INFO)
                                        if unit.action != "build":
                                            unit.action = None
                        else:
                            #logs(self.player.name + " : " + str(unit) + " is arrived", level=logging.INFO)
                            if unit.action != "build":
                                unit.action = None

    def depositResources(self, villager, target_deposit):

        villager_position = villager.getPosition()

        distance_x = abs(target_deposit[0] - villager.x)
        distance_y = abs(target_deposit[1] - villager.y)
        if distance_x <= 1 and distance_y <= 1:
            if villager.carryingType == 'Gold':
                self.player.addGold(villager.carrying)
                villager.carrying = 0
                villager.carryingType = None
                logs(self.player.name + " : Villager deposit gold : " + str(self.player), level=logging.INFO)
            elif villager.carryingType == 'Wood':
                self.player.addWood(villager.carrying)
                villager.carrying = 0
                villager.carryingType = None
                logs(self.player.name + " : Villager deposit wood : " + str(self.player), level=logging.INFO)
            villager.action = None
        
        else :
            logs(self.player.name + " : Villager is too far to deposit resources", level=logging.INFO)

    def getPlayer(self):
        return self.player
    
    def attack(self, unit, enemy, playerenemy):
        
        #Vérification de la distance entre l'unité et l'ennemi
        if isinstance(enemy, Buildings):
            distance_x = abs(enemy.x - unit.x) - enemy.sizeMap // 2
            distance_y = abs(enemy.y - unit.y) - enemy.sizeMap // 2
        else:
            distance_x = abs(enemy.x - unit.x)
            distance_y = abs(enemy.y - unit.y)
        
        if distance_x <= unit.range and distance_y <= unit.range:
            logs(self.player.name + " : " + str(unit) + " is attacking", level=logging.INFO)
            unit.action = "attack"
            start_time = time.time()
            self.queueAttack.append({"unit": unit, "start_time": start_time, "enemy": enemy, "playerenemy": playerenemy})
            return 0
        else:
            return -1
                
    def updating_attack(self):
        
        current_time = time.time()
        
        for item in self.queueAttack[:]:
            unit = item["unit"]
            start_time = item["start_time"]
            enemy = item["enemy"]
            playerenemy = item["playerenemy"]
            
            if current_time - start_time >= unit.speedAtack:
                #vérification de la distance entre l'unité et l'ennemi
                if isinstance(enemy, Buildings):
                    distance_x = abs(enemy.x - unit.x) - enemy.sizeMap // 2
                    distance_y = abs(enemy.y - unit.y) - enemy.sizeMap // 2
                else:
                    distance_x = abs(enemy.x - unit.x)
                    distance_y = abs(enemy.y - unit.y)
                
                #Si l'ennemi est à portée d'attaque, l'unité attaque
                if distance_x <= unit.range and distance_y <= unit.range:
                    
                    #logs(self.player.name + " : " + str(unit) + " is attacking", level=logging.INFO)
                    enemy.health -= unit.attack
                    item["start_time"] = time.time()
                    if enemy.health == 0:
                        self.cmap.map.map_entities[enemy.x][enemy.y] = None
                        self.cmap.map.map[enemy.x][enemy.y] = " "
                        if isinstance(enemy, Buildings):
                            for x in range(enemy.sizeMap):
                                for y in range(enemy.sizeMap):
                                    self.cmap.map.map_entities[enemy.x + x][enemy.y + y] = None
                                    self.cmap.map.map[enemy.x + x][enemy.y + y] = " "
                            if enemy in playerenemy.player.buildings:
                                playerenemy.player.buildings.remove(enemy)
                            logs(playerenemy.name + " : " + str(enemy) + " is destroyed", level=logging.INFO)
                        elif isinstance(enemy, Units):
                            if enemy in playerenemy.player.units:
                                playerenemy.player.units.remove(enemy) 
                            logs(playerenemy.player.name + " : " + str(enemy) + " is dead", level=logging.INFO)
                        self.queueAttack.remove(item)
                        unit.action = None
                #Si l'ennemi est trop loin, l'unité arrête d'attaquer
                else:
                    self.queueAttack.remove(item)
                    unit.action = None