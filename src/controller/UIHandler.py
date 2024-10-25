import pygame
import sys

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer
from model.Map import MapType

class UIHandler():
    def __init__(self):

        #Création de la map
        self.controllerMap = ControllerMap()
        self.lstPlayers = []
    
        # Création de 4 joueurs
        for i in range(5):
            self.lstPlayers.append(ControllerPlayer("Player"+str(i), 100, 100, 100))

        # Placement des town centers sur la map
        self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)

        # Génération des ressources de la Map
        self.controllerMap.genRessources(MapType.CENTER_RESOURCES)

    def start(self):
        self.controllerMap.run()