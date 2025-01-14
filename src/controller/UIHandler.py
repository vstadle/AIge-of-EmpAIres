import pygame
import sys
import pickle
import os
import datetime

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer
from model.Map import MapType
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Villager import Villager
from model.Game import Game
from model.Player import Player
from controller.ControllerGame import ControllerGame

class UIHandler():
    def __init__(self):
        self.screen = pygame.display.set_mode((600,600))
        #Création de la map
        self.game = Game()
        self.controllerMap = ControllerMap()
        self.lstPlayers = []
        self.controllerGame = None

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
                            self.show_load_game_menu(screen, font)
                        if y > 300 and y < 330:
                            menu_active = False
                            pygame.quit()
                            sys.exit()

    def start_new_game(self):
        # Lancer une nouvelle partie
        self.controllerMap.genRessources(MapType.CENTER_RESOURCES)
        self.initialize("Marines", 4)  # Exemple : type "Marines", 4 joueurs
        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.game.setMap(self.controllerMap.map)
        for player in self.lstPlayers:
            self.game.lstPlayer.append(player.getPlayer())
        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
        pygame.quit()
        self.start()

    def saveGame(self):
        if not os.path.exists("../save"):
            os.makedirs("../save")
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Save Game")
        screen.fill((0, 0, 0))  
        pygame.display.update()
        lsttemp = []
        for players in self.lstPlayers:
            lsttemp.append(players.getPlayer())
        self.game.setLstPlayer(lsttemp)
        self.game.setMap(self.controllerMap.map)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"../save/save_{current_time}.dat"
        file = open(file_name, 'wb')
        pickle.dump(self.game, file)
        file.close()
        print("Game saved")
        
    def loadGame(self,path_file):
        path_file = "../save/" + path_file
        file = open(path_file, "rb")
        game = pickle.load(file)
        file.close()
        self.game = game
        for player in self.game.lstPlayer:
            print(f"Après désérialisation : Joueur {player.name}")
            print(f"  Units: {len(player.units)}")
            print(f"  Buildings: {len(player.buildings)}")

        self.controllerMap.reset(self.game.map)
        for player in self.game.lstPlayer:
            self.lstPlayers.append(ControllerPlayer.from_saved(player, self.controllerMap))

        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
        print(game.lstPlayer)
        print(self.controllerMap.map)
        print("Game loaded")
        pygame.quit()
        self.start()

    def initialize(self, typeGame, nbPlayers):
        if(typeGame == "Lean"):
            
            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer.from_new("Player "+str(i), 50, 200, 50, self.controllerMap))
        
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                for j in range(3):
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[0])
                    
        elif(typeGame == "Mean"):
            
            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer.from_new("Player "+str(i), 2000, 2000, 2000, self.controllerMap))
            
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                for j in range(3):
                    cplayer.trainVillager(cplayer.getPlayer().getBuildings()[0])

        elif(typeGame ==  "Marines"):

            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer.from_new("Player "+str(i), 20000, 20000, 20000, self.controllerMap))
            
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

    def show_load_game_menu(self, screen, font):
        clock = pygame.time.Clock()
        files = os.listdir('../save/')
        load_game_active = True
        while load_game_active:
            screen.fill((0, 0, 0))

            y = 100
            file_positions = []
            for file in files:
                file_text = font.render(file, True, (255, 255, 255))
                screen.blit(file_text, (100, y))
                file_positions.append((file, 100, y, 100 + file_text.get_width(), y + file_text.get_height()))
                y += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    load_game_active = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for file, x1, y1, x2, y2 in file_positions:
                        if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
                            self.loadGame(file)
                            load_game_active = False
                            

            clock.tick(200)

    def start(self):
        self.controllerGame.run()