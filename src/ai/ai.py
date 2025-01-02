import logging
import random

from logs.logger import logs
from model.TownCenter import TownCenter
from model.Camp import Camp
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.Barracks import Barracks

from model.Villager import Villager

from model.Gold import Gold
from model.Wood import Wood
from model.House import House
from model.Farm import Farm
from model.Swordsman import Swordsman
from model.Horseman import Horseman
from model.Archer import Archer
from model.Keep import Keep

from controller import A_Star

class AI:

    cpt = 0

    def __init__(self, game, cplayer):
        self.game = game
        self.cplayer = cplayer

        self.lstActionWaiting = []
        self.lstVillagerCollecting = []
        self.lstVillagerCollect = []
    
        self.lstBuildingWaiting = []
    
    def villager_is_available(self):
        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager) and unit.action is None:
                #logs(self.cplayer.player.name + " : Villager found", logging.INFO)
                return unit
        return None

    def find_gold(self, villager):
        villager_x = villager.x
        villager_y = villager.y

        radius = 1

        target = None

        while radius <= max(self.game.map.size_map_x, self.game.map.size_map_y):
            for x in range(villager_x - radius, villager_y + radius + 1):
                for y in range(villager_y - radius, villager_y + radius + 1):
                    if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                        ressource = self.game.map.mapRessources[x][y]
                        if ressource is not None and self.game.map.map[x][y] == "G":
                            
                            adjacent_positions = [
                                (ressource.x - 1, ressource.y),
                                (ressource.x + 1, ressource.y),
                                (ressource.x, ressource.y - 1),
                                (ressource.x, ressource.y + 1),
                            ]

                            for x, y in adjacent_positions:
                                if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                                    if self.game.map.map[x][y] == " ":
                                        logs(self.cplayer.player.name + " :  Gold found", logging.INFO)
                                        target = ressource, x, y
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
        villager = self.villager_is_available()

        if villager is not None:
                gold = self.find_gold(villager)
                if gold is not None:
                    # Cherche une case libre adjacente à la ressource
                    target_position = gold[1], gold[2]
                    gold = gold[0]
                    if target_position:
                        target_x, target_y = target_position
                        distance_x = abs(gold.getX() - villager.x)
                        distance_y = abs(gold.getY() - villager.y)

                        deposit = self.find_deposit(villager, gold)
                        if deposit is None:
                            logs(self.cplayer.player.name + " : No deposit found", logging.ERROR)
                            return -1

                        temp_x = deposit[1]
                        temp_y = deposit[2]

                        target_deposit = temp_x, temp_y

                        self.lstVillagerCollect.append({"unit": villager, "ressource": gold, "target": target_position, "deposit": deposit[0], "target_deposit": target_deposit})
                        if distance_x <= 1 and distance_y <= 1:
                            self.cplayer.collectResources(villager, gold)
                        else:
                            #self.lstActionWaiting.append({"unit": villager, "action": "move", "action_target": "collect", "ressource": gold})
                            #for action in self.lstActionWaiting:
                            #    logs(self.cplayer.player.name + " :  Action waiting : " + action["action_target"], logging.INFO)
                            self.cplayer.move(villager, target_x, target_y)

    def collectWood(self):
        logs(self.cplayer.player.name + " :  Collect Wood", logging.INFO)
        villager = self.villager_is_available()

        if villager is not None:
            wood = self.find_wood(villager)
            if wood is not None:
                target_position = wood[1], wood[2]
                wood = wood[0]
                
                distance_x = abs(wood.x - villager.x)
                distance_y = abs(wood.y - villager.y)
                
                deposit = self.find_deposit(villager, wood)
                if deposit is None:
                    logs(self.cplayer.player.name + " : No deposit found", logging.ERROR)
                    return -1

                temp_x = deposit[1]
                temp_y = deposit[2]

                target_deposit = temp_x, temp_y

                self.lstVillagerCollect.append({"unit": villager, "ressource": wood, "target": target_position, "deposit": deposit[0], "target_deposit": target_deposit})
                if distance_x <= 1 and distance_y <= 1:
                    self.cplayer.collectResources(villager, wood)
                else:
                    self.cplayer.move(villager, target_position[0], target_position[1])

        return 0

    def find_wood(self, villager):
        villager_x = villager.x
        villager_y = villager.y

        radius = 1

        target = None

        while radius <= max(self.game.map.size_map_x, self.game.map.size_map_y):
            for x in range(villager_x - radius, villager_y + radius + 1):
                for y in range(villager_y - radius, villager_y + radius + 1):
                    if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                        ressource = self.game.map.mapRessources[x][y]
                        if ressource is not None and self.game.map.map[x][y] == "W":
                            
                            adjacent_positions = [
                                (ressource.x - 1, ressource.y),
                                (ressource.x + 1, ressource.y),
                                (ressource.x, ressource.y - 1),
                                (ressource.x, ressource.y + 1),
                            ]

                            for x, y in adjacent_positions:
                                if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                                    if self.game.map.map[x][y] == " ":
                                        logs(self.cplayer.player.name + " :  Wood found", logging.INFO)
                                        target = ressource, x, y
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
            deposit = item["deposit"]
            target_deposit = item["target_deposit"]

            if unit.action is None and unit.x == target_deposit[0] and unit.y == target_deposit[1]:
                self.cplayer.depositResources(unit, target_deposit)
                self.cplayer.move(unit, target[0], target[1])
            elif unit.action is None and (ressource.capacity == 0 or unit.carrying == 20):
                logs(self.cplayer.player.name + " : villager return to town center", logging.INFO)
                self.cplayer.move(unit, target_deposit[0], target_deposit[1])
                if ressource.capacity == 0:
                    self.lstVillagerCollect.remove(item)
            elif unit.action is None and unit.x == target[0] and unit.y == target[1]:
                self.cplayer.collectResources(unit, ressource)
            
            elif unit.action is None and unit.x != target[0] and unit.y != target[1]:
                if ressource.capacity != 0:
                    deposit_temp = self.find_deposit(unit, ressource)
                    self.cplayer.move(unit, deposit_temp[1], deposit_temp[2])
                else:
                    self.lstVillagerCollect.remove(item)

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
                if self.game.map.mapUnits[x][y] is None:  # La case est libre
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

        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager):
                cpt_villager += 1
            elif isinstance(unit, Swordsman):
                cpt_swordsman += 1
            elif isinstance(unit, Archer):
                cpt_archer += 1
            elif isinstance(unit, Horseman):
                cpt_horseman += 1
        
        return cpt_villager, cpt_swordsman, cpt_archer, cpt_horseman

    def count_villager_inactivity(self):
        cpt = 0
        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager) and unit.action is None:
                cpt += 1
        return cpt

    def choose_strategie(self):

        ''' On vérifier les villageois qui collectent des ressources '''
        self.verifCollectVillager()

        '''Vérification constructions des batiments'''
        '''for building in self.lstBuildingWaiting:
            if self.villager_is_available() is not None:
                cpt_villager = self.count_villager_inactivity()
                position = self.findPlaceForBuildings(building)
                if position is not None:
                    check = self.cplayer.addBuilding(building, position[0], position[1])
                    if check == 0:
                        self.lstBuildingWaiting.remove(building)
                    break'''

        if self.cplayer.player.food < 200:
            farm = Farm()
            if self.cplayer.player.canAffordBuilding(farm):
                position = self.findPlaceForBuildings(farm)
                if position is not None:
                    check = self.cplayer.addBuilding(Farm(), position[0], position[1])
                    if check == -1:
                        self.lstBuildingWaiting.append(farm)
        
        
        if ((len(self.cplayer.player.units) + len(self.cplayer.player.training_queue))) == self.cplayer.player.population:
            #logs(self.cplayer.player.name + " :  Population is full (AI Information)", logging.INFO)
            house = House()
            if self.cplayer.player.canAffordBuilding(house):
                self.lstBuildingWaiting = [house] + self.lstBuildingWaiting
        
                    
        else:
            '''Vérification entrainement des unités'''
            cpt_villager, cpt_swordsman, cpt_archer, cpt_horseman = self.count_Unit()
            ratio_villager = cpt_villager // len(self.cplayer.player.units)
            ration_sworsman = cpt_swordsman // len(self.cplayer.player.units)
            ration_archer = cpt_archer // len(self.cplayer.player.units)
            ration_horseman = cpt_horseman // len(self.cplayer.player.units)

            if ratio_villager < 0.5:
                towncenter = self.findBuildings(TownCenter)
                if towncenter is not None:
                    check = self.cplayer.trainVillager(towncenter)
                    if check == 1:
                        self.lstBuildingWaiting.append(Farm())
                    elif check == -1:
                        self.lstBuildingWaiting.append(House())

            if ration_sworsman < 0.5:
                barracks = self.findBuildings(Barracks)
                if barracks is not None:
                    check = self.cplayer.trainSwordsman(barracks)
                    if check == 1:
                        self.lstBuildingWaiting.append(Farm())
                    elif check == -1:
                        self.lstBuildingWaiting.append(House())
            
            if ration_archer < 0.5:
                archery = self.findBuildings(ArcheryRange)
                if archery is not None:
                    check = self.cplayer.trainArcher(archery)
                    if check == 1:
                        self.lstBuildingWaiting.append(Farm())
                    elif check == -1:
                        self.lstBuildingWaiting.append(House())
            
            if ration_horseman < 0.5:
                stable = self.findBuildings(Stable)
                if stable is not None:
                    check = self.cplayer.trainHorseman(stable)
                    if check == 1:
                        self.lstBuildingWaiting.append(Farm())
                    elif check == -1:
                        self.lstBuildingWaiting.append(House())
            
            if self.cplayer.player.gold > 1000 and self.cplayer.player.wood > 1000:
                self.lstBuildingWaiting.append(Camp())
                self.lstBuildingWaiting.append(Barracks())
                self.lstBuildingWaiting.append(ArcheryRange())
                self.lstBuildingWaiting.append(Stable())
                self.lstBuildingWaiting.append(Keep())
                self.lstBuildingWaiting.append(TownCenter())
            else:
                cpt_villager = self.count_villager_inactivity()
                if cpt_villager > 0:
                    for i in range(0, cpt_villager//4):
                        self.collectGold()
                        self.collectWood()