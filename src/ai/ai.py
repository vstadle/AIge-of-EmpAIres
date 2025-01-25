import logging
import random

from logs.logger import logs
from model.TownCenter import TownCenter
from model.Camp import Camp
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.Barracks import Barracks

from model.Buildings import Buildings
from model.Units import Units

from model.Villager import Villager


from model.Gold import Gold
from model.Wood import Wood
from model.House import House
from model.Farm import Farm
from model.Swordsman import Swordsman
from model.Horseman import Horseman
from model.Archer import Archer
from model.Keep import Keep

from model.Player import Player

from controller import A_Star

class AI:

    cpt = 0

    def __init__(self, game, cplayer):
        self.game = game
        self.cplayer = cplayer

        self.lstVillagerCollect = []
        self.lstUnitAttack = []
    
        self.lstBuildingWaiting = []
        self.lstUnitWaiting = []
        
        self.RessourceCollecting = [] #ressource + case adjacente


    def villager_is_available(self):
        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager) and unit.action is None:
                #logs(self.cplayer.player.name + " : Villager found", logging.INFO)
                return unit
        return None

    def unit_is_available(self):
        for unit in self.cplayer.player.units:
            if unit.action is None:
                return unit
        return None

    def find_gold(self, villager):
        villager_x = villager.x
        villager_y = villager.y

        radius = 1  # Rayon initial de la recherche
        target = None

        max_radius = max(self.game.map.size_map_x, self.game.map.size_map_y)

        while radius <= max_radius:
            # Parcourt les points dans un carré englobant le cercle
            for x in range(villager_x - radius, villager_x + radius + 1):
                for y in range(villager_y - radius, villager_y + radius + 1):
                    # Vérifie si le point est dans le cercle
                    if (x - villager_x) ** 2 + (y - villager_y) ** 2 <= radius ** 2:
                        # Vérifie si la position est dans les limites de la carte
                        if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                            ressource = self.game.map.map_entities[x][y]
                            if ressource is not None and self.game.map.map[x][y] == "G":
                                # Vérifie les cases adjacentes libres
                                adjacent_positions = [
                                    (ressource.x - 1, ressource.y - 1),
                                    (ressource.x, ressource.y - 1),
                                    (ressource.x + 1, ressource.y - 1),
                                    (ressource.x + 1, ressource.y),
                                    (ressource.x + 1, ressource.y + 1),
                                    (ressource.x, ressource.y + 1),
                                    (ressource.x - 1, ressource.y + 1),
                                    (ressource.x - 1, ressource.y),
                                ]

                                for adj_x, adj_y in adjacent_positions:
                                    if 0 <= adj_x < self.game.map.size_map_x and 0 <= adj_y < self.game.map.size_map_y:
                                        if self.game.map.map[adj_x][adj_y] == " " and (adj_x, adj_y) not in self.RessourceCollecting:
                                            chemin = A_Star.a_star(self.game.map, (villager.x, villager.y), (adj_x, adj_y))
                                            if chemin is not None:
                                                logs(self.cplayer.player.name + " : Gold found", logging.INFO)
                                                target = ressource, adj_x, adj_y
                                                break
                                if target is not None:
                                    break
                    if target is not None:
                        break
            if target is not None:
                break
            radius += 1

        return target


    def find_deposit(self, villager, ressource):

        """
        Trouve le bâtiment de dépôt le plus proche appartenant au joueur correspondant au villageois.
        Recherche les bâtiments dans la liste des bâtiments du joueur et vérifie les cases adjacentes libres.

        Args:
            villager (Villager): Le villageois cherchant un dépôt.
            ressource (Ressources): La ressource pour laquelle on cherche un dépôt.

        Returns:
            tuple: (bâtiment, x, y) où x et y sont les coordonnées d'une case libre adjacente au bâtiment.
                Retourne None si aucun dépôt accessible n'est trouvé.
        """
        # Le joueur auquel le villageois est rattaché
        player = self.cplayer.player  # Le joueur actuellement contrôlé par l'IA
        ressource_x, ressource_y = ressource.x, ressource.y

        # Parcourt les bâtiments appartenant au joueur
        for building in player.buildings:
            # Vérifie si le bâtiment est un dépôt valide (par exemple, "C" pour Town Center, "T" pour autres dépôts)
            if isinstance(building, TownCenter) or isinstance(building, Camp):
                logs(f"Bâtiment trouvé pour dépôt : {str(building)} à ({building.x}, {building.y})", logging.INFO)

                # Récupère les coordonnées des cases adjacentes autour du bâtiment (en fonction de sa taille)
                adjacent_positions = []
                for dx in range(-1, building.sizeMap + 1):
                    adjacent_positions.append((building.x + dx, building.y - 1))  # Haut
                    adjacent_positions.append((building.x + dx, building.y + building.sizeMap))  # Bas
                for dy in range(-1, building.sizeMap + 1):
                    adjacent_positions.append((building.x - 1, building.y + dy))  # Gauche
                    adjacent_positions.append((building.x + building.sizeMap, building.y + dy))  # Droite

                # Vérifie les cases adjacentes pour trouver une case libre
                for adj_x, adj_y in adjacent_positions:
                    if (
                        0 <= adj_x < self.game.map.size_map_x and
                        0 <= adj_y < self.game.map.size_map_y and
                        self.game.map.map[adj_x][adj_y] == " "  # Vérifie que la case est libre
                    ):
                        #logs(f"Case libre trouvée pour dépôt à ({adj_x}, {adj_y})", logging.INFO)
                        chemin = A_Star.a_star(self.game.map, (villager.x, villager.y), (adj_x, adj_y))
                        if chemin is not None:
                            return (building, adj_x, adj_y, chemin)

        # Aucun dépôt accessible trouvé
        logs("Aucun bâtiment de dépôt valide trouvé pour ce joueur.", logging.WARNING)
        return None


    def collectGold(self):
        logs(self.cplayer.player.name + " :  Collect Gold stratégie", logging.INFO)

        #On cherche un villageois disponible
        villager = self.villager_is_available()

        #Si on a trouvé un villageois
        if villager is not None:
                #On cherche une ressource d'or la plus proche du villageois
                gold = self.find_gold(villager)
                #Si on a trouvé une ressource d'or
                if gold is not None:
                    # Cherche une case libre adjacente à la ressource
                    target_position = gold[1], gold[2]
                    gold = gold[0]

                    #On vérifie que la case dans laquelle on veut aller existe bien
                    if target_position:
                        target_x, target_y = target_position
                        distance_x = abs(gold.getX() - villager.x)
                        distance_y = abs(gold.getY() - villager.y)

                        self.lstVillagerCollect.append({"unit": villager, "ressource": gold, "target": target_position, "deposit" : None, "target_deposit" : None})
                        self.RessourceCollecting.append(target_position)
                        if distance_x <= 1 and distance_y <= 1:
                            self.cplayer.collectResources(villager, gold)
                        else:
                            #self.lstActionWaiting.append({"unit": villager, "action": "move", "action_target": "collect", "ressource": gold})
                            #for action in self.lstActionWaiting:
                            #    logs(self.cplayer.player.name + " :  Action waiting : " + action["action_target"], logging.INFO)
                            self.cplayer.move(villager, target_x, target_y)

    def collectWood(self):
        logs(self.cplayer.player.name + " :  Collect Wood", logging.INFO)
        
        #On chercher un villageois disponible
        villager = self.villager_is_available()

        #Si on a trouvé un villageois
        if villager is not None:
            #On cherche une ressource de bois la plus proche du villageois
            wood = self.find_wood(villager)
            #Si on a trouvé une ressource de bois
            if wood is not None:
                # Cherche une case libre adjacente à la ressource
                target_position = wood[1], wood[2]
                wood = wood[0]
                
                #On vérifie que la case dans laquelle on veut aller existe bien
                if target_position:
                    target_x, target_y = target_position
                    distance_x = abs(wood.getX() - villager.x)
                    distance_y = abs(wood.getY() - villager.y)

                    self.lstVillagerCollect.append({"unit": villager, "ressource": wood, "target": target_position, "deposit" : None, "target_deposit" : None})
                    self.RessourceCollecting.append(target_position)
                    if distance_x <= 1 and distance_y <= 1:
                        self.cplayer.collectResources(villager, wood)
                    else:
                        self.cplayer.move(villager, target_x, target_y)

    def find_wood(self, villager):
        villager_x = villager.x
        villager_y = villager.y

        radius = 1  # Rayon initial de la recherche
        target = None

        max_radius = max(self.game.map.size_map_x, self.game.map.size_map_y)

        while radius <= max_radius:
            # Parcourt les points dans un carré englobant le cercle
            for x in range(villager_x - radius, villager_x + radius + 1):
                for y in range(villager_y - radius, villager_y + radius + 1):
                    # Vérifie si le point est dans le cercle
                    if (x - villager_x) ** 2 + (y - villager_y) ** 2 <= radius ** 2:
                        # Vérifie si la position est dans les limites de la carte
                        if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                            ressource = self.game.map.map_entities[x][y]
                            if ressource is not None and self.game.map.map[x][y] == "W":
                                # Vérifie les cases adjacentes libres
                                adjacent_positions = [
                                    (ressource.x - 1, ressource.y - 1),
                                    (ressource.x, ressource.y - 1),
                                    (ressource.x + 1, ressource.y - 1),
                                    (ressource.x + 1, ressource.y),
                                    (ressource.x + 1, ressource.y + 1),
                                    (ressource.x, ressource.y + 1),
                                    (ressource.x - 1, ressource.y + 1),
                                    (ressource.x - 1, ressource.y),
                                ]

                                for adj_x, adj_y in adjacent_positions:
                                    if 0 <= adj_x < self.game.map.size_map_x and 0 <= adj_y < self.game.map.size_map_y:
                                        if self.game.map.map[adj_x][adj_y] == " " and (adj_x, adj_y) not in self.RessourceCollecting:
                                            chemin = A_Star.a_star(self.game.map, (villager.x, villager.y), (adj_x, adj_y))
                                            if chemin is not None:
                                                logs(self.cplayer.player.name + " : Wood found", logging.INFO)
                                                target = ressource, adj_x, adj_y
                                                break
                                if target is not None:
                                    break
                    if target is not None:
                        break
            if target is not None:
                break
            radius += 1

        return target

    def verifCollectVillager(self):

        for item in self.lstVillagerCollect:

            unit = item["unit"]

            if unit.action is not None:
                pass

            ressource = item["ressource"]
            target = item["target"]

            #Si le villageois n'est pas à coté de la ressource et qu'il ne transporte rien
            #Alors on le déplace
            if unit.action is None and unit.x != target[0] and unit.y != target[1] and unit.carrying == 0:
                self.cplayer.move(unit, target[0], target[1])

            #Sinon si le villageois est à coté de la ressource et qu'il ne transporte rien
            #Alors on le fait collecter la ressource
            elif unit.action is None and unit.x == target[0] and unit.y == target[1] and unit.carrying == 0:
                self.cplayer.collectResources(unit, ressource)
            
            #Sinon si le villageois ne fait rien et qu'il est plein ou que la ressource est vide
            #Alors on l'envoi au dépôt
            elif unit.action is None and (ressource.capacity == 0 or unit.carrying == 20) and unit.x == target[0] and unit.y == target[1]:
                deposit = self.find_deposit(unit, ressource)
                if deposit[0] is not None and deposit[1] is not None and deposit[2] is not None:
                    item["deposit"] = deposit[0]
                    item["target_deposit"] = deposit[1], deposit[2]
                    self.cplayer.move(unit, item["target_deposit"][0], item["target_deposit"][1])
            
            #Sinon si le villageois ne fait rien et qu'il est à coté du dépôt
            #On le fait déposer les ressources
            elif unit.action is None and item["deposit"] is not None and item["target_deposit"] is not None:
                self.cplayer.depositResources(unit, item["target_deposit"])
                if ressource.capacity == 0:
                    self.lstVillagerCollect.remove(item)
                    self.RessourceCollecting.remove(item["target"])

    def verifBuilding(self):
            for building in self.lstBuildingWaiting:
                if self.villager_is_available() is not None:
                    cpt_villager = self.count_villager_inactivity()
                    position = self.findPlaceForBuildings(building)
                    if position is not None:
                        check = self.cplayer.addBuilding(building, position[0], position[1])
                        if check == 0:
                            self.lstBuildingWaiting.remove(building)
                        break

    def verifUnit(self):
        for unit in self.lstUnitWaiting:
            if self.villager_is_available() is not None:
                if unit == "villager":
                    towncenter = self.findBuildings(TownCenter)
                    if towncenter is not None:
                        check = self.cplayer.trainVillager(towncenter)
                        if check == 0:
                            self.lstUnitWaiting.remove(unit)
                elif unit == "swordsman":
                    barracks = self.findBuildings(Barracks)
                    if barracks is not None:
                        check = self.cplayer.trainSwordsman(barracks)
                        if check == 0:
                            self.lstUnitWaiting.remove(unit)
                elif unit == "archer":
                    archery = self.findBuildings(ArcheryRange)
                    if archery is not None:
                        check = self.cplayer.trainArcher(archery)
                        if check == 0:
                            self.lstUnitWaiting.remove(unit)
                elif unit == "horseman":
                    stable = self.findBuildings(Stable)
                    if stable is not None:
                        check = self.cplayer.trainHorseman(stable)
                        if check == 0:
                            self.lstUnitWaiting.remove(unit)

    def verifUnitAttack(self):
        
        for item in self.lstUnitAttack:
            unit = item["unit"]
            
            if unit.action is not None:
                pass
        
                target = item["target"]
                target_position = item["target_position"]
                
                if unit.action is None and target is None:
                    self.lstUnitAttack.remove(item)
                    self.attackTarget()
                    
                if unit.action is None and (unit.x, unit.y == target_position) and target is not None:
                    self.cplayer.attack(unit, target)

    def find_adjacent_free_tile(self, resource):
        adjacent_positions = [
            (resource.x - 1, resource.y),
            (resource.x + 1, resource.y),
            (resource.x, resource.y - 1),
            (resource.x, resource.y + 1),
        ]
        for x, y in adjacent_positions:
            # Vérifie si la case est dans les limites de la carte et est libre
            if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                if self.game.map.map[x][y] == " ":  # Vérifie qu'aucune ressource, batiment ou unité n'occupe cette case
                    return (x, y)
        return None

    def is_gold_accessible(self, resource):
        adjacent_positions = [
            (resource.x - 1, resource.y),
            (resource.x + 1, resource.y),
            (resource.x, resource.y - 1),
            (resource.x, resource.y + 1),
        ]
        for x, y in adjacent_positions:
            # Vérifie si la case est dans les limites de la carte et est libre
            if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                if self.game.map.map_entities[x][y] is None:  # La case est libre
                    return True
        return False

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
        if len(self.cplayer.player.buildings) > 0:
            main_building = self.cplayer.player.buildings[0]  # On suppose que le premier bâtiment est le Town Center

        if main_building is not None:
            town_center_x = main_building.x
            town_center_y = main_building.y
            town_center_size = main_building.sizeMap
            building_size = building.sizeMap
            radius = 5

            while radius <= max(self.game.map.size_map_x, self.game.map.size_map_y):
                for i in range(town_center_x - radius, town_center_x + radius + 1):
                    for j in range(town_center_y - radius, town_center_y + radius + 1):
                        # Vérifie si les coordonnées sont dans les limites de la carte
                        if 0 <= i < self.game.map.size_map_x and 0 <= j < self.game.map.size_map_y:
                            # Vérifie si l'emplacement est libre pour le bâtiment
                            is_free = True
                            for k in range(-1, building_size + 1):  # Inclut une case autour du bâtiment
                                for l in range(-1, building_size + 1):
                                    check_x = i + k
                                    check_y = j + l
                                    if (
                                        0 <= check_x < self.game.map.size_map_x
                                        and 0 <= check_y < self.game.map.size_map_y
                                    ):
                                        # Vérifie qu'aucune case (y compris autour du bâtiment) n'est occupée
                                        if self.game.map.map[check_x][check_y] != " ":
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
                                            0 <= corridor_x < self.game.map.size_map_x
                                            and 0 <= corridor_y < self.game.map.size_map_y
                                            and abs(corridor_x - (i + building_size // 2)) <= 1
                                            and abs(corridor_y - (j + building_size // 2)) <= 1
                                        ):
                                            if self.game.map.map[corridor_x][corridor_y] != " ":
                                                is_free = False
                                                break
                                    if not is_free:
                                        break

                            if is_free:
                                return i, j  # Retourne les coordonnées du coin supérieur gauche

                    radius += 1

        return None  # Aucun emplacement trouvé


    def findBuildings(self, name):
        for building in self.cplayer.player.buildings:
            if isinstance(building, name):
                return building
        return None
        
    def findWaitBuildings(self, name):
        for building in self.lstBuildingWaiting:
            if isinstance(building, name):
                return building

    def start_strategie(self):
        
        townCenter = self.findBuildings(TownCenter)
        
        for i in range(0, 2):
            self.cplayer.trainVillager(townCenter)
        
            
        villager = self.villager_is_available()
        if villager is not None:
            self.collectGold()
        
        villager = self.villager_is_available()
        if villager is not None:
            self.collectWood()
        
        farm = Farm()
        position = self.findPlaceForBuildings(farm)
        if position is not None:
            self.cplayer.addBuilding(Farm(), position[0], position[1])
        
        self.lstBuildingWaiting.append(House())
        self.lstBuildingWaiting.append(House())
        self.lstBuildingWaiting.append(Barracks())
        self.lstBuildingWaiting.append(ArcheryRange())
        self.lstBuildingWaiting.append(Stable())
        self.lstBuildingWaiting.append(Camp())
        
    def count_Unit(self):
        cpt_villager = 0
        cpt_swordsman = 0
        cpt_archer = 0
        cpt_horseman = 0

        logs(self.cplayer.player.name + " :  Count unit" + str(len(self.cplayer.player.units)), logging.INFO)

        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager):
                cpt_villager += 1
            elif isinstance(unit, Swordsman):
                cpt_swordsman += 1
            elif isinstance(unit, Archer):
                cpt_archer += 1
            elif isinstance(unit, Horseman):
                cpt_horseman += 1
        
        logs(self.cplayer.player.name + " :  Villager : " + str(cpt_villager), logging.INFO)
        logs(self.cplayer.player.name + " :  Swordsman : " + str(cpt_swordsman), logging.INFO)
        logs(self.cplayer.player.name + " :  Archer : " + str(cpt_archer), logging.INFO)
        logs(self.cplayer.player.name + " :  Horseman : " + str(cpt_horseman), logging.INFO)

        return cpt_villager, cpt_swordsman, cpt_archer, cpt_horseman

    def count_villager_inactivity(self):
        cpt = 0
        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager) and unit.action is None:
                cpt += 1
        return cpt

    def build(self, typeOfBuilding):
            if typeOfBuilding == TownCenter:
                building = TownCenter()
            elif typeOfBuilding == Camp:
                building = Camp()
            elif typeOfBuilding == Barracks:
                building = Barracks()
            elif typeOfBuilding == ArcheryRange:
                building = ArcheryRange()
            elif typeOfBuilding == Stable:
                building = Stable()
            elif typeOfBuilding == House:
                building = House()
            elif typeOfBuilding == Farm:
                building = Farm()
            elif typeOfBuilding == Keep:
                building = Keep()
            else:
                return None
            position = self.findPlaceForBuildings(building)
            if position is not None:
                check = self.cplayer.addBuilding(building, position[0], position[1])
                if check == 2:
                    self.lstBuildingWaiting.append(building)

    def expansion_strategie(self):

        logs(self.cplayer.player.name + " :  Expansion strategie", logging.INFO)

        ''' Stratégie d'expansion de l'IA '''
        ''' On construit des farms et des houses pour pouvoir entrainer des unités '''
        ''' On entraine des villageois pour collecter des ressources '''
        ''' On entraine des unités pour se défendre '''

        if self.villager_is_available() is None:
            towncenter = self.findBuildings(TownCenter)
            if towncenter is not None:
                check = self.cplayer.trainVillager(towncenter)
                if check == 1:
                    self.lstUnitWaiting.append("villager")

        if self.cplayer.player.food < 300:
            for i in range (0, 2):
                farm = Farm()
                if self.cplayer.player.canAffordBuilding(farm):
                    position = self.findPlaceForBuildings(farm)
                    if position is not None:
                        check = self.cplayer.addBuilding(Farm(), position[0], position[1])
                        if check == 2:
                            self.lstBuildingWaiting.append(farm)

        nb_unit = len(self.cplayer.player.units)

        ratio_unit = nb_unit // self.cplayer.player.population

        if ratio_unit < 0.8:
            house = House()
            if self.cplayer.player.canAffordBuilding(house):
                position = self.findPlaceForBuildings(house)
                if position is not None:
                    check = self.cplayer.addBuilding(House(), position[0], position[1])
                    if check == 2:
                        self.lstBuildingWaiting.append(house)

        cpt_villager, cpt_swordsman, cpt_archer, cpt_horseman = self.count_Unit()
        ratio_villager = cpt_villager // len(self.cplayer.player.units)
        ration_sworsman = cpt_swordsman // len(self.cplayer.player.units)
        ration_archer = cpt_archer // len(self.cplayer.player.units)
        ration_horseman = cpt_horseman // len(self.cplayer.player.units)

        while ratio_villager < 0.25:
            towncenter = self.findBuildings(TownCenter)
            if towncenter is None:
                towncenter = self.findWaitBuildings(TownCenter)
                if towncenter is None:
                    self.build(TownCenter)
                    break
            elif towncenter is not None:
                check = self.cplayer.trainVillager(towncenter)
                if check == 1:
                    self.lstUnitWaiting.append("villager")
            cpt_villager += 1
            ratio_villager = cpt_villager // len(self.cplayer.player.units) + len(self.lstUnitWaiting)

        while ration_sworsman < 0.25:
            barracks = self.findBuildings(Barracks)
            if barracks is None:
                barracks = self.findWaitBuildings(Barracks)
                if barracks is None:
                    self.build(Barracks)
                    break
            elif barracks is not None:
                check = self.cplayer.trainSwordsman(barracks)
                if check == 1:
                    self.lstUnitWaiting.append("swordsman")
            cpt_swordsman += 1
            ration_sworsman = cpt_swordsman // len(self.cplayer.player.units) + len(self.lstUnitWaiting)
        
        while ration_archer < 0.25:
            archery = self.findBuildings(ArcheryRange)
            if archery is None:
                archery = self.findWaitBuildings(ArcheryRange)
                if archery is None:
                    self.build(ArcheryRange)
                    break
            elif archery is not None:
                check = self.cplayer.trainArcher(archery)
                if check == 1:
                    self.lstUnitWaiting.append("archer")
            cpt_archer += 1
            ration_archer = cpt_archer // len(self.cplayer.player.units) + len(self.lstUnitWaiting)

        while ration_horseman < 0.25:
            stable = self.findBuildings(Stable)
            if stable is None:
                stable = self.findWaitBuildings(Stable)
                if stable is None:
                    self.build(Stable)
                    break
            elif stable is not None:
                check = self.cplayer.trainHorseman(stable)
                if check == 1:
                    self.lstUnitWaiting.append("horseman")
            cpt_horseman += 1
            ration_horseman = cpt_horseman // len(self.cplayer.player.units) + len(self.lstUnitWaiting)

    def collect_strategie(self):

        logs(self.cplayer.player.name + " :  Collect strategie", logging.INFO)

        ''' Stratégie de collecte de l'IA '''
        ''' On collecte des ressources pour pouvoir construire des batiments et entrainer des unités '''
        ''' On récupère le nombre de villageois inactifs pour les faire collecter des ressources'''

        cpt_inactive_villager = self.count_villager_inactivity()
        if cpt_inactive_villager > 0:
            cpt_inactive_villager = cpt_inactive_villager // 2
            for i in range(0, cpt_inactive_villager):
                self.collectGold()
                self.collectWood()
            self.collectWood()

    def attack_strategie(self, enemy):

        logs(self.cplayer.player.name + " :  Attack strategie", logging.INFO)

        for unit in self.cplayer.player.units:
            if isinstance(unit, Swordsman) or isinstance(unit, Archer) or isinstance(unit, Horseman):
                self.attack_target(unit, enemy)

    def attack_target(self, unit, enemy):

        closest_enemy = self.find_target(unit, enemy)

        if closest_enemy is not None:
            target_position = self.find_adjacent_free_tile(closest_enemy)
            if target_position is not None:
                self.cplayer.attack(unit, closest_enemy, enemy)
                self.lstUnitAttack.append({"unit": unit, "target": closest_enemy, "target_position": target_position})

    def find_adjacent_free_tile(self, unitenemy):
        adjacent_positions = [
            (unitenemy.x - 1, unitenemy.y),
            (unitenemy.x + 1, unitenemy.y),
            (unitenemy.x, unitenemy.y - 1),
            (unitenemy.x, unitenemy.y + 1),
            (unitenemy.x - 1, unitenemy.y - 1),
            (unitenemy.x + 1, unitenemy.y + 1),
            (unitenemy.x - 1, unitenemy.y + 1),
            (unitenemy.x + 1, unitenemy.y - 1),
        ]
        for x, y in adjacent_positions:
            # Vérifie si la case est dans les limites de la carte et est libre
            if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                if self.game.map.map_entities[x][y] is None:  # La case est libre
                    return (x, y)

    def find_target(self, unit, enemy):

        closest_enemy = None
        min_distance = float('inf')

        for enemy_unit in enemy.player.units:
            distance = abs(unit.x - enemy_unit.x) + abs(unit.y - enemy_unit.y)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy_unit

        return closest_enemy

    def reforcement_strategie(self):

        logs(self.cplayer.player.name + " :  Reforcement strategie", logging.INFO)

        ''' Stratégie de renforcement de l'IA '''
        ''' On entraine beaucoup d'unités pour attaquer l'adversaire '''
        ''' On construit des batiments pour pouvoir entrainer des unités '''
        ''' On construit des batiments de défense '''

        cpt_villager, cpt_swordsman, cpt_archer, cpt_horseman = self.count_Unit()
        
        ration_sworsman = cpt_swordsman / len(self.cplayer.player.units)
        ration_archer = cpt_archer / len(self.cplayer.player.units)
        ration_horseman = cpt_horseman / len(self.cplayer.player.units)

        logs(self.cplayer.player.name + " :  Ration swordsman : " + str(ration_sworsman), logging.INFO)
        logs(self.cplayer.player.name + " :  Ration archer : " + str(ration_archer), logging.INFO)
        logs(self.cplayer.player.name + " :  Ration horseman : " + str(ration_horseman), logging.INFO)

        barracks = self.findBuildings(Barracks)
        while ration_sworsman < 0.34:
            if barracks is None:
                break
            if barracks is not None:
                check = self.cplayer.trainSwordsman(barracks)
                if check == 1:
                    self.lstUnitWaiting.append("swordsman")
            cpt_swordsman += 1
            ration_sworsman = cpt_swordsman / len(self.cplayer.player.units) + len(self.lstUnitWaiting)
        
        archery = self.findBuildings(ArcheryRange)
        while ration_archer < 0.34:
            if archery is None:
                break
            if archery is not None:
                check = self.cplayer.trainArcher(archery)
                if check == 1:
                    self.lstUnitWaiting.append("archer")
            cpt_archer += 1
            ration_archer = cpt_archer / len(self.cplayer.player.units) + len(self.lstUnitWaiting)

        stable = self.findBuildings(Stable)
        while ration_horseman < 0.34:
            if stable is None:
                break
            if stable is not None:
                check = self.cplayer.trainHorseman(stable)
                if check == 1:
                    self.lstUnitWaiting.append("horseman")
            cpt_horseman += 1
            ration_horseman = cpt_horseman + 1 / len(self.cplayer.player.units) + len(self.lstUnitWaiting)

        costGoldKeep = Keep().costG
        costWoodKeep = Keep().costW

        if self.cplayer.player.population == len(self.cplayer.player.units):
            for i in range (0, 4):
                house = House()
                if self.cplayer.player.canAffordBuilding(house):
                    position = self.findPlaceForBuildings(house)
                    if position is not None:
                        check = self.cplayer.addBuilding(house, position[0], position[1])
                        if check == 2:
                            self.lstBuildingWaiting.insert(0,house)

        cpt = 0

        while self.cplayer.player.gold > costGoldKeep and self.cplayer.player.wood > costWoodKeep and cpt < 10:
            keep = Keep()
            if self.cplayer.player.canAffordBuilding(keep):
                position = self.findPlaceForBuildings(keep)
                if position is not None:
                    check = self.cplayer.addBuilding(keep, position[0], position[1])
                    if check == 2:
                        self.lstBuildingWaiting.append(keep)
            cpt += 1

    def choose_strategie(self, lstcPlayer):

        ''' Choix de la stratégie de l'IA '''
        ''' On choisit une stratégie en fonction de la situation de l'IA '''

        if self.cplayer.player.gold < 300 and self.cplayer.player.wood < 300:
            self.collect_strategie()

        elif self.cplayer.player.food < 300 and len(self.cplayer.player.units) < 30:
            self.expansion_strategie()

        elif self.cplayer.player.food > 1000 and self.cplayer.player.gold > 1000 and self.cplayer.player.wood > 1000:
            self.reforcement_strategie()

        lstNbUnitPerPlayer = []
        minUnit = 0
        minPlayer = None
        for cPlayer in lstcPlayer:
            if cPlayer != self.cplayer:
                if minUnit < len(cPlayer.player.units):
                    minUnit = len(cPlayer.player.units)
                    minPlayer = cPlayer

        if len(self.cplayer.player.units) > minUnit:
            self.attack_strategie(minPlayer)
    
    def update(self):
        self.verifBuilding()
        self.verifCollectVillager()
        self.verifUnit()
        self.verifUnitAttack()