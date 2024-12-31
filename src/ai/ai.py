import logging

from logs.logger import logs
from model.TownCenter import TownCenter
from model.Camp import Camp
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
        self.lstVillagerCollect = []
    
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
                        logs(f"Case libre trouvée pour dépôt à ({adj_x}, {adj_y})", logging.INFO)
                        return (building, adj_x, adj_y)

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
                    target_position = self.find_adjacent_free_tile(gold)
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
                    self.lstVillagerCollect.remove(unit)
            elif unit.action is None and unit.x == target[0] and unit.y == target[1]:
                self.cplayer.collectResources(unit, ressource)

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


    def choose_strategie(self):

        ''' On vérifier les villageois qui collectent des ressources '''
        self.verifCollectVillager()
        
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
                self.collectGold()

        AI.cpt += 1

        return 0