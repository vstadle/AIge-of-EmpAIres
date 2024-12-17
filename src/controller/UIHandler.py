import pygame
import sys
import pickle
import os
import datetime
import logging

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer
from model.Map import MapType
from model.TownCenter import TownCenter
from model.Farm import Farm
from model.Villager import Villager
from model.Game import Game
from model.Player import Player
from controller.ControllerGame import ControllerGame
from logs.logger import logs

class UIHandler():
    def __init__(self):

        #Création de la map
        self.game = Game()
        self.controllerMap = ControllerMap(120,120)
        self.lstPlayers = []
        self.controllerGame = None

    def show_menu(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Menu Principal")

        font = pygame.font.Font(None, 36)

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

        pygame.quit()

        '''Demande des paramètres pour une nouvelle partie'''
        while(True):
            typeGame = input("Type de partie (Lean, Mean, Marines) : ")
            if typeGame in ["Lean", "Mean", "Marines"]:
                break
            else:
                print("Type de partie invalide")
        
        while(True):
            nbPlayers = input("Nombre de joueurs : ")
            if nbPlayers.isdigit():
                nbPlayers = int(nbPlayers)
                break
            else:
                print("Nombre de joueurs invalide")

        while(True):
            typeMap = input("Type de carte (Generous, Center) : ")
            if typeMap in ["Generous", "Center"]:
                if typeMap == "Generous":
                    typeRessource = MapType.GENEROUS_RESOURCES
                    break
                elif typeMap == "Center":
                    typeRessource = MapType.CENTER_RESOURCES
                    break
            else:
                print("Type de carte invalide")

        while(True):
            size_x = input("Taille de la carte (x) : ")
            if size_x.isdigit():
                size_x = int(size_x)
                if size_x > 0:
                    break
            print("Taille invalide")
            
        while(True):
            size_y = input("Taille de la carte (y) : ")
            if size_y.isdigit():
                size_y = int(size_y)
                if size_y > 0:
                    break
            print("Taille invalide")
        '''Initialisation de la partie'''

        print("Création de la partie...")

        # Lancer une nouvelle partie
        self.controllerMap = ControllerMap(size_x, size_y)
        self.controllerMap.genRessources(typeRessource)
        self.initialize(typeGame, nbPlayers)  # Exemple : type "Marines", 6 joueurs
        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.game.setMap(self.controllerMap.map)
        for player in self.lstPlayers:
            self.game.lstPlayer.append(player.getPlayer())
        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
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
        logs("Gave Saved", level=logging.INFO)
        
    def loadGame(self,path_file):
        logs("Loading Game", level=logging.INFO)
        path_file = "../save/" + path_file
        file = open(path_file, "rb")
        game = pickle.load(file)
        file.close()
        self.game = game
        for player in self.game.lstPlayer:
            logs(f"Après désérialisation : Joueur {player.name}", level=logging.INFO)
            logs(f"  Units: {len(player.units)}", level=logging.INFO)
            logs(f"  Buildings: {len(player.buildings)}", level=logging.INFO)

        self.controllerMap.reset(self.game.map)
        for player in self.game.lstPlayer:
            self.lstPlayers.append(ControllerPlayer.from_saved(player, self.controllerMap))

        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
        logs(game.lstPlayer.__str__())
        logs(self.controllerMap.map.__str__())
        logs("Game loaded")
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
                            

            clock.tick(60)

    def start(self):
        self.controllerGame.run()