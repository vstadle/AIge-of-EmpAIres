import pygame
import sys
import pickle
import datetime

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer
from model.Map import MapType
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Villager import Villager
from model.Game import Game
import os

class UIHandler():
    def __init__(self):

        #Création de la map
        self.game = Game()
        self.controllerMap = ControllerMap(self)
        self.lstPlayers = []

    def show_menu(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Menu Principal")

        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        menu_active = True
        while menu_active:
            screen.fill((0, 0, 0))

            new_game = font.render("Nouvelle Partie", True, (255, 255, 255))
            load_game = font.render("Charger Partie", True, (255, 255, 255))
            quit_game = font.render("Quitter", True, (255, 255, 255))

            screen.blit(new_game, (300, 200))
            screen.blit(load_game, (300, 250))
            screen.blit(quit_game, (300, 300))
    
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_active = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x > 300 and x < 500:
                        if y > 200 and y < 230:
                            menu_active = False
                            self.start_new_game()
                        if y > 250 and y < 280:
                            menu_active = False
                            self.loadGame()
                        if y > 300 and y < 330:
                            menu_active = False
                            pygame.quit()
                            sys.exit()

    def start_new_game(self):
        # Lancer une nouvelle partie
        self.controllerMap.genRessources(MapType.CENTER_RESOURCES)
        self.initialize("Marines", 6)  # Exemple : type "Marines", 6 joueurs
        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.start()

    def saveGame(self):
        if not os.path.exists("../sauv"):
            os.makedirs("../sauv")
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Save Game")
        screen.fill((0, 0, 0))  # Fill the screen with a background color
        pygame.display.update()
        # Charger une partie sauvegardée
        lsttemp = []
        for players in self.lstPlayers:
            lsttemp.append(players.getPlayer())
        print(lsttemp)
        print(self.controllerMap.map)
        self.game.setLstPlayer(lsttemp)
        self.game.setMap(self.controllerMap.map)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"../sauv/Save_{current_time}.dat"
        print(file_name)
        file = open(file_name, 'wb')
        pickle.dump(self.game, file)
        file.close()
        print("Game saved")
        
    def loadGame(self):
        # Set the window size and title for the load game menu
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Load Game")
        pygame.display.update()
        # Charger une partie sauvegardée
        file_name = "../sauv/save.txt"  # Update this to the correct file name if needed
        file = open(file_name, "rb")
        game = pickle.load(file)
        file.close()
        self.game = game
        self.controllerMap.reset(self.game.map)
        for player in game.lstPlayer:
            self.lstPlayers.append(ControllerPlayer.from_saved(player, self.controllerMap))
        self.controllerMap.setLstPlayers(self.lstPlayers)
        print(self.controllerMap.map)
        print("Game loaded")
        self.start()

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