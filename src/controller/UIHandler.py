import pygame
import sys

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer
from model.Map import MapType
from model.TownCenter import TownCenter

class UIHandler():
    def __init__(self):

        #Création de la map
        self.controllerMap = ControllerMap()
        self.lstPlayers = []
    
        # Création de 4 joueurs
        for i in range(4):
            self.lstPlayers.append(ControllerPlayer("Player"+str(i), 100, 100, 100))

        # Placement des town centers sur la map
        self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)

        # Génération des ressources de la Map
        self.controllerMap.genRessources(MapType.CENTER_RESOURCES)

        '''Test références des batiments sur la map avec prise de dégats'''
        '''self.controllerMap.getMap().addBuilding(TownCenter(), 0, 0)
        self.controllerMap.getMap().getBuildings()[0][0].setHp(300)
        print(self.controllerMap.getMap().getBuildings()[3][3].getHp())
        self.controllerMap.getMap().getBuildings()[2][1].setHp(5000)
        print(self.controllerMap.getMap().getBuildings()[3][1].getHp())'''

    def start(self):
        self.controllerMap.run()