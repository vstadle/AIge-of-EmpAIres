import pygame
import sys
import pickle
import os
import datetime
import logging
import tkinter as tk #ASM

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
from controller.SaveMenu import SaveMenu #ASM
from tkinter import messagebox #ASM


class UIHandler():
    def __init__(self):

        #Création de la map
        self.game = Game()
        self.controllerMap = ControllerMap(120,120)
        self.lstPlayers = []
        self.controllerGame = None

        self.isSaved = False
        self.nameFile = ""

    def show_menu(self):
        pygame.init()
        
        # Définir la taille initiale de la fenêtre
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Menu Principal")
        
        # Charger les ressources
        background = pygame.image.load(f"../data/img/menu_background.png")  # Remplacez par une image de style médiéval
        button_image = pygame.image.load(f"../data/img/button.png")  # Remplacez par une texture de bouton médiéval
        font = pygame.font.Font(f"../data/font/CinzelDecorative-Regular.ttf", 36)  # Remplacez par une police médiévale
        
        buttons = [
            ("Nouvelle Partie", self.start_new_game),
            ("Sauvegardes", lambda: self.manage_saves(screen, font)), #ASM
            ("Quitter", sys.exit)
        ]
        
        menu_active = True
        
        while menu_active:
            screen.fill((0, 0, 0))
            
            # Ajuster l'image de fond à la taille de l'écran
            screen.blit(pygame.transform.scale(background, screen.get_size()), (0, 0))
            
            # Obtenir la taille actuelle de l'écran
            screen_width, screen_height = screen.get_size()
            
            # Centrer dynamiquement les boutons
            mouse_pos = pygame.mouse.get_pos()
            for i, (text, action) in enumerate(buttons):
                button_width, button_height = 300, 50
                x = (screen_width - button_width) // 2
                y = (screen_height - (len(buttons) * (button_height + 20))) // 2 + i * (button_height + 20)
                
                # Définir le rectangle du bouton
                button_rect = pygame.Rect(x, y, button_width, button_height)
                
                # Vérifier si la souris est au-dessus du bouton
                is_hovered = button_rect.collidepoint(mouse_pos)
                button_color = (200, 200, 100) if is_hovered else (160, 82, 45)  # Or couleur en fonction du thème
                
                # Dessiner le bouton
                pygame.draw.rect(screen, button_color, button_rect)
                screen.blit(pygame.transform.scale(button_image, button_rect.size), button_rect.topleft)
                
                # Ajouter le texte centré sur le bouton
                label = font.render(text, True, (255, 255, 255))
                label_rect = label.get_rect(center=button_rect.center)
                screen.blit(label, label_rect.topleft)
            
            # Rafraîchir l'écran
            pygame.display.flip()
            
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                    for i, (text, action) in enumerate(buttons):
                        button_width, button_height = 300, 50
                        x = (screen_width - button_width) // 2
                        y = (screen_height - (len(buttons) * (button_height + 20))) // 2 + i * (button_height + 20)
                        button_rect = pygame.Rect(x, y, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            menu_active = False
                            action()
                elif event.type == pygame.VIDEORESIZE:
                    # Ajuster l'écran à la nouvelle taille
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    def start_new_game(self):

        pygame.quit()

        '''Demande des paramètres pour une nouvelle partie'''
        while(True):
            typeGame = input("Type de partie (Lean, Mean, Marines) : ")
            typeGame = typeGame.upper()
            if typeGame in ["LEAN", "MEAN", "MARINES"]:
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
            typeMap = typeMap.upper()
            if typeMap in ["GENEROUS", "CENTER"]:
                if typeMap == "GENEROUS":
                    typeRessource = MapType.GENEROUS_RESOURCES
                    break
                elif typeMap == "CENTER":
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
        self.controllerMap.map.mapType = typeRessource
        self.controllerMap.genRessources(typeRessource)
        self.initialize(typeGame, nbPlayers)  # Exemple : type "Marines", 6 joueurs
        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.game.setMap(self.controllerMap.map)
        for player in self.lstPlayers:
            self.game.lstPlayer.append(player.getPlayer())
        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
        self.start()

    def saveGameOld(self): #ASM
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

        if self.isSaved:
            file_name_temp = f"../save/{self.nameFile}"
            os.remove(file_name_temp)

        file_name = f"../save/save_{current_time}.dat"
        file = open(file_name, 'wb')
        pickle.dump(self.game, file)
        file.close()
        logs("Game Saved", level=logging.INFO) 
        

    def saveGame(self): #ASM

        # Initialiser tkinter sans fenêtre principale
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale de tkinter

        if not os.path.exists("../save"):
            os.makedirs("../save")

        # Effectuer la sauvegarde
        lsttemp = []
        for players in self.lstPlayers:
            lsttemp.append(players.getPlayer())
        self.game.setLstPlayer(lsttemp)
        self.game.setMap(self.controllerMap.map)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if self.isSaved:
            file_name_temp = f"../save/{self.nameFile}"
            os.remove(file_name_temp)

        file_name = f"../save/save_{current_time}.dat"
        with open(file_name, 'wb') as file:
            pickle.dump(self.game, file)

        logs("Game Saved", level=logging.INFO)

        # Afficher une boîte de dialogue de confirmation
        messagebox.showinfo("Sauvegarde", "Sauvegarde effectuée avec succès !")

        # Revenir au menu principal
        self.show_menu()




    def loadGameOld(self,path_file): #ASM
        self.isSaved = True
        self.nameFile = path_file
        logs("Loading Game", level=logging.INFO)
        path_file = "../save/" + path_file
        file = open(path_file, "rb")
        game = pickle.load(file)
        file.close()
        self.game = game

        '''
        for player in self.game.lstPlayer:
            logs(f"Après désérialisation : Joueur {player.name}", level=logging.INFO)
            logs(f"  Units: {len(player.units)}", level=logging.INFO)
            logs(f"  Buildings: {len(player.buildings)}", level=logging.INFO)
        '''
            
        self.controllerMap.reset(self.game.map)
        for player in self.game.lstPlayer:
            self.lstPlayers.append(ControllerPlayer.from_saved(player, self.controllerMap))

        self.controllerMap.setLstPlayers(self.lstPlayers)
        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
        #logs(game.lstPlayer.__str__())
        #logs(self.controllerMap.map.__str__())
        logs("Game loaded")
        pygame.quit()
        self.start()


    def loadGame(self, path_file): #ASM
        try:
            self.isSaved = True
            self.nameFile = path_file
            logs("Loading Game", level=logging.INFO)

            # Chargement du fichier de sauvegarde
            path_file = "../save/" + path_file
            with open(path_file, "rb") as file:
                self.game = pickle.load(file)

            # Réinitialiser la carte et les joueurs
            self.controllerMap.reset(self.game.map)
            self.lstPlayers = [
                ControllerPlayer.from_saved(player, self.controllerMap) for player in self.game.lstPlayer
            ]
            self.controllerMap.setLstPlayers(self.lstPlayers)
            self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)

            logs("Game loaded successfully")
            print(f"Partie {path_file} chargée avec succès.")
        except Exception as e:
            logs(f"Erreur lors du chargement de la partie : {e}", level=logging.ERROR)
            print(f"Erreur lors du chargement de la partie : {e}")
        finally:
            # Retour propre au menu principal
            self.show_menu()



    def initialize(self, typeGame, nbPlayers):
        if(typeGame == "LEAN"):
            
            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer.from_new("Player "+str(i), 50, 200, 50, self.controllerMap))
        
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                for j in range(3):
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[0])
                    
        elif(typeGame == "MEAN"):
            
            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer.from_new("Player "+str(i), 2000, 2000, 2000, self.controllerMap))
            
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                for j in range(3):
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[0])

        elif(typeGame ==  "MARINES"):

            for i in range(nbPlayers):
                self.lstPlayers.append(ControllerPlayer.from_new("Player "+str(i), 20000, 20000, 20000, self.controllerMap))
            
            self.controllerMap.placementTownCenter(len(self.lstPlayers), self.lstPlayers)
            
            for cplayer in self.lstPlayers:
                cplayer.initializeTownCenter(2)
                for t in range(5):
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[0])
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[1])
                    cplayer.addUnitInitialize(Villager(), cplayer.getPlayer().getBuildings()[2])
    
            '''
            self.lstPlayers[0].addBuilding(Farm(), 10, 10)
            self.lstPlayers[0].trainArcher(self.lstPlayers[0].getPlayer().getBuildings()[7])
            self.lstPlayers[0].trainHorseman(self.lstPlayers[0].getPlayer().getBuildings()[6])
            self.lstPlayers[0].trainVillager(self.lstPlayers[0].getPlayer().getBuildings()[0])
            self.lstPlayers[0].trainSwordsman(self.lstPlayers[0].getPlayer().getBuildings()[4])
            self.lstPlayers[0].trainVillager(self.lstPlayers[0].getPlayer().getBuildings()[0])
            self.lstPlayers[0].trainVillager(self.lstPlayers[0].getPlayer().getBuildings()[0])
            '''
            
    def show_load_game_menuOld(self, screen, font): #ASM

        clock = pygame.time.Clock()
        files = os.listdir('../save/')
        scroll_offset = 0
        scroll_speed = 20  # Nombre de pixels par défilement

        load_game_active = True
        while load_game_active:
            screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()

            y = 100 - scroll_offset
            file_positions = []

            for file in files:
                label = font.render(file, True, (255, 255, 255))
                rect = label.get_rect(topleft=(100, y))
                color = (200, 200, 0) if rect.collidepoint(mouse_pos) else (255, 255, 255)
                label = font.render(file, True, color)
                screen.blit(label, rect.topleft)
                file_positions.append((file, rect))
                y += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    load_game_active = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        for file, rect in file_positions:
                            if rect.collidepoint(mouse_pos):
                                self.loadGame(file)
                                load_game_active = False
                    elif event.button == 4:  # Molette haut
                        scroll_offset = max(0, scroll_offset - scroll_speed)
                    elif event.button == 5:  # Molette bas
                        scroll_offset = min(max(0, len(files) * 40 - 400), scroll_offset + scroll_speed)

            clock.tick(60)

    def show_load_game_menu(self, screen, font): #ASM
        import os
        import pygame

        # Répertoire des sauvegardes
        save_dir = "../save/"

        # Vérifier que le répertoire de sauvegarde existe
        if not os.path.exists(save_dir):
            print(f"Le répertoire {save_dir} est introuvable.")
            return

        # Charger la liste des fichiers
        files = os.listdir(save_dir)
        if not files:
            print("Aucune sauvegarde disponible.")
            return

        clock = pygame.time.Clock()
        scroll_offset = 0
        scroll_speed = 20  # Nombre de pixels par défilement
        load_game_active = True

        while load_game_active:
            screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            screen_width, screen_height = screen.get_size()

            # Dessiner les fichiers de sauvegarde
            y = 100 - scroll_offset
            file_positions = []
            for file in files:
                label = font.render(file, True, (255, 255, 255))
                rect = label.get_rect(topleft=(100, y))
                color = (200, 200, 0) if rect.collidepoint(mouse_pos) else (255, 255, 255)
                label = font.render(file, True, color)
                screen.blit(label, rect.topleft)
                file_positions.append((file, rect))
                y += 40

            # Bouton Retour
            button_width, button_height = 200, 50
            button_rect = pygame.Rect((screen_width - button_width) // 2, screen_height - 100, button_width, button_height)
            pygame.draw.rect(screen, (255, 0, 0), button_rect)
            label = font.render("Retour", True, (255, 255, 255))
            label_rect = label.get_rect(center=button_rect.center)
            screen.blit(label, label_rect)

            pygame.display.flip()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        # Vérifier si un fichier a été cliqué
                        for file, rect in file_positions:
                            if rect.collidepoint(mouse_pos):
                                try:
                                    self.loadGame(file)
                                    print(f"Partie {file} chargée avec succès !")
                                    load_game_active = False
                                except Exception as e:
                                    print(f"Erreur lors du chargement : {e}")
                                    load_game_active = False
                                    return
                        # Vérifier si le bouton Retour a été cliqué
                        if button_rect.collidepoint(mouse_pos):
                            load_game_active = False

                    elif event.button == 4:  # Molette haut
                        scroll_offset = max(0, scroll_offset - scroll_speed)
                    elif event.button == 5:  # Molette bas
                        scroll_offset = min(max(0, len(files) * 40 - 400), scroll_offset + scroll_speed)

            clock.tick(60)

    def start(self):
        self.controllerGame.run()

    def manage_saves(self, screen, font): #ASM
        save_menu = SaveMenu(self)
        save_menu.display(screen, font)