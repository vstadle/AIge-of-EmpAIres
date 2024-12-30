import logging

from logs.logger import logs
from model.TownCenter import TownCenter
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.Barracks import Barracks

from model.Villager import Villager

from model.Gold import Gold

class AI:

    cpt = 0

    def __init__(self, game, cplayer):
        self.game = game
        self.cplayer = cplayer

        self.lstActionWaiting = []
        self.lstVillagerCollecting = []
    
    def build(self, building_name, position):
        self.cplayer.addBuilding(building_name, position[0], position[1])

    def train(self, unit_name):
        unit_name = unit_name.lower()

        if unit_name == "villager":
            
            towncenter = None
            for building in self.cplayer.player.buildings:
                if isinstance(building, TownCenter):
                    towncenter = building
                    break
            if towncenter is not None:
                self.cplayer.trainVillager(towncenter)
                return 0
            else:
                logs(self.cplayer.player.name + " : No town center found, impossible to train villager", logging.ERROR)
                return -1
            
        elif unit_name == "archer":
            
            archeryrange = None
            for building in self.cplayer.buildings:
                if isinstance(building, ArcheryRange):
                    archeryrange = building
                    break
            if archeryrange is not None:
                self.cplayer.trainArcher(archeryrange)
                return 0
            else:
                logs(self.cplayer.player.name + " : No archery range found, impossible to train archer", logging.ERROR)
                return -1
        
        elif unit_name == "horseman":
            
            stable = None
            for building in self.cplayer.buildings:
                if isinstance(building, Stable):
                    stable = building
                    break
            if stable is not None:
                self.cplayer.trainHorseman(stable)
                return 0
            else:
                logs(self.cplayer.player.name + " : No stable found, impossible to train horseman", logging.ERROR)
                return -1
        
        elif unit_name == "swordsman":
            
            barracks = None
            for building in self.cplayer.buildings:
                if isinstance(building, Barracks):
                    barracks = building
                    break
            if barracks is not None:
                self.cplayer.trainSwordsman(barracks)
                return 0
            else:
                logs(self.cplayer.player.name + " : No barracks found, impossible to train swordsman", logging.ERROR)
                return -1
        
        else:
            logs(self.cplayer.player.name + " : Unknown unit type", logging.ERROR)
            return -1
    
    def villager_is_available(self):
        for unit in self.cplayer.player.units:
            if isinstance(unit, Villager) and unit.action is None:
                logs(self.cplayer.player.name + " : Villager found", logging.INFO)
                return unit
        return None

    def find_gold(self, villager):
        villager_x = villager.x
        villager_y = villager.y
        radius = 1  # Commence avec un rayon de recherche de 1

        while radius <= max(self.game.map.size_map_x, self.game.map.size_map_y):
            for x in range(villager_x - radius, villager_x + radius + 1):
                for y in range(villager_y - radius, villager_y + radius + 1):
                    # Vérifie si (x, y) est dans les limites de la carte
                    if 0 <= x < self.game.map.size_map_x and 0 <= y < self.game.map.size_map_y:
                        resource = self.game.map.mapRessources[x][y]
                        if resource is not None and isinstance(resource, Gold):
                            # Vérifie si au moins une case adjacente est libre
                            if self.is_gold_accessible(resource):
                                return resource
            radius += 1  # Augmente le rayon de recherche

        return None  # Retourne None si aucun or accessible n'est trouvé

             
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
                if self.game.map.mapUnits[x][y] is None:  # Vérifie qu'aucune unité n'occupe cette case
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


    def choose_strategie(self):

        '''On regarde si l'IA a des actions en attente
        Ex: un villageois qui doit se déplacer pour collecter une ressource'''
        for action in self.lstActionWaiting:
            unit = action["unit"]
            action_target = action["action_target"]
            #logs(self.cplayer.player.name + " :  Acton unit " + str(unit.action) + " Action waiting : " + action_target, logging.INFO)
            '''Si l'action en attente est de collecter une ressource et que l'unité n'a pas d'action en cours
            alors elle est arrivée à destination et peut commencer à collecter la ressource'''
            if action_target == "collect" and unit.action is None:
                logs(self.cplayer.player.name + " :  Collect ressource after moving", logging.INFO)
                self.lstActionWaiting.remove(action)
                '''On ajout le villageois à la liste des villageois qui collectent des ressources et on le fait collecter la ressource'''
                self.lstVillagerCollecting.append({"unit": unit, "ressource": action["ressource"]})
                self.cplayer.collectResources(unit, action["ressource"])

        '''On regarde si les villageois qui collectent des ressources ont fini de collecter la ressource
        Si oui alors on les déplace pour aller déposer les ressources'''
        for villager in self.lstVillagerCollecting:
            if villager["unit"].action is None and(villager["ressource"].capacity == 0 or villager["unit"].carrying == 20):
                logs(self.cplayer.player.name + " : villager return to town center", logging.INFO)
                
                #Test de déplacement du villageois vers le centre-ville
                #On devra trouver le town center ou le camp le plus proche pour déposer la ressource
                self.cplayer.move(villager["unit"], 10, 10)
                self.lstVillagerCollecting.remove(villager)
        
        # --- TEST ---
        #Test pour ne pas répéter la stratégie
        if AI.cpt < 2:

            gold = self.cplayer.player.gold
            wood = self.cplayer.player.wood
            food = self.cplayer.player.food
            population = self.cplayer.player.population

            logs (self.cplayer.player.name + " :  Gold : " + str(gold), logging.INFO)
            logs (self.cplayer.player.name + " :  Choose strategie", logging.INFO)

            if gold <= 100:
                logs(self.cplayer.player.name + " :  Collect Gold stratégie", logging.INFO)
                villager = self.villager_is_available()
                if villager is not None:
                    gold = self.find_gold(villager)
                    if gold is not None:
                        # Cherche une case libre adjacente à la ressource
                        target_position = self.find_adjacent_free_tile(gold)
                        if target_position:
                            target_x, target_y = target_position
                            distance_x = abs(gold.getX() - villager.x)
                            distance_y = abs(gold.getY() - villager.y)
                            if distance_x <= 1 and distance_y <= 1:
                                self.lstVillagerCollecting.append(villager)
                                self.cplayer.collectResources(villager, gold)
                            else:
                                self.lstActionWaiting.append({"unit": villager, "action": "move", "action_target": "collect", "ressource": gold})
                                for action in self.lstActionWaiting:
                                    logs(self.cplayer.player.name + " :  Action waiting : " + action["action_target"], logging.INFO)
                                self.cplayer.move(villager, target_x, target_y)
            
        AI.cpt += 1

        return 0