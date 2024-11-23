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

        self.controllerMap.genRessources(MapType.CENTER_RESOURCES)

        # Initialisation de la partie
        # La fonction initialize prend en paramètre le mode de jeu de la partie et le nombre de joueurs de la partie
        self.initialize("Marines", 6)

        self.controllerMap.setLstPlayers(self.lstPlayers)
        # Génération des ressources de la Map
        #self.controllerMap.genRessources(MapType.CENTER_RESOURCES)

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
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[0])
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[1])
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[2])
    
            self.lstPlayers[0].addBuilding(Farm(), 10, 10)
            
            self.lstPlayers[0].trainArcher(self.lstPlayers[0].getPlayer().getBuildings()[7])
            self.lstPlayers[0].trainHorseman(self.lstPlayers[0].getPlayer().getBuildings()[6])
            self.lstPlayers[0].trainVillager(self.lstPlayers[0].getPlayer().getBuildings()[0])
            self.lstPlayers[0].trainSwordsman(self.lstPlayers[0].getPlayer().getBuildings()[4])

    def start(self):
        self.controllerMap.run()