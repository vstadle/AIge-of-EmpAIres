import pygame
import sys

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer
from model.Map import MapType
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Villager import Villager

class UIHandler():
    def __init__(self):

        #Création de la map
        self.controllerMap = ControllerMap()
        self.lstPlayers = []

        self.initialize("Marines", 2)

        # Génération des ressources de la Map
        self.controllerMap.genRessources(MapType.CENTER_RESOURCES)

    def initialize(self, typeGame, nbPlayers):
        if(typeGame == "Lean"):
            
            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer("Player"+str(i), 50, 200, 50, self.controllerMap))
        
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                for j in range(3):
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[0])
                    
        elif(typeGame == "Mean"):
            
            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer(ControllerPlayer("Player"+str(i), 2000, 2000, 2000, self.controllerMap)))
            
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                for j in range(3):
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[0])

        elif(typeGame ==  "Marines"):

            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer("Player"+str(i), 20000, 20000, 20000, self.controllerMap))
            
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                cplayer.initializeTownCenter(2)
                for t in range(5):
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[0])
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[1])
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[2])
    
    def start(self):
        self.controllerMap.run()