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
        self.screen = pygame.display.set_mode((800, 600))
        self.game = Game()
        self.controllerMap = ControllerMap(120, 120)
        self.lstPlayers = []
        self.controllerGame = None
        self.isSaved = False
        self.nameFile = ""
        self.logo_size = (200, 200)  # Taille réduite pour mieux s'intégrer en haut

    def show_menu(self):
        logo_click_count = 0
        last_click_time = 0
        click_timeout = 500 #Easter Egg
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Menu Principal")
        
        # Charger les ressources
        background = pygame.image.load("../data/img/background.png")
        button_image = pygame.image.load("../data/img/button.png")
        font = pygame.font.Font("../data/font/CinzelDecorative-Regular.ttf", 32)
        logo = pygame.image.load("../data/img/logo2.png")
        buttons = [
            ("Nouvelle Partie", self.show_game_config),
            ("Charger Partie", lambda: self.show_load_game_menu(screen, font)),
            ("Quitter", sys.exit)
        ]
        
        menu_active = True
        
        while menu_active:
            screen.fill((0, 0, 0))
            screen_width, screen_height = screen.get_size()
            screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
            
            
            logo_x = (screen_width - self.logo_size[0]) // 2
            logo_rect = pygame.Rect(logo_x, 20, self.logo_size[0], self.logo_size[1])
            screen.blit(pygame.transform.scale(logo, self.logo_size), (logo_x, 20))

            mouse_pos = pygame.mouse.get_pos()
            button_height = 60 
            spacing = 30  # espace entre les boutons
            total_height = len(buttons) * (button_height + spacing)
            
            current_y = (screen_height - total_height) // 2
            
            for text, action in buttons:
                button_width = 350 
                button_rect = pygame.Rect((screen_width - button_width) // 2, current_y, button_width, button_height)
                
                is_hovered = button_rect.collidepoint(mouse_pos)
                button_color = (200, 200, 100) if is_hovered else (160, 82, 45)
                
                # dessin bouton
                scaled_button = pygame.transform.scale(button_image, (button_width, button_height))
                screen.blit(scaled_button, button_rect.topleft)
                
                # centrer le texte
                label = font.render(text, True, (255, 255, 255))
                label_rect = label.get_rect(center=button_rect.center)
                screen.blit(label, label_rect)
                
                current_y += button_height + spacing
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    current_time = pygame.time.get_ticks()
                
                    if logo_rect.collidepoint(mouse_pos):
                        if current_time - last_click_time < click_timeout:
                            logo_click_count += 1
                        else:
                            logo_click_count = 1
                        
                        last_click_time = current_time
                        
                        if logo_click_count >= 5:  # Après 5 clics rapides
                            menu_active = False
                            self.show_credits()
                            return
                    for i, (text, action) in enumerate(buttons):
                        button_rect = pygame.Rect(
                            (screen_width - 350) // 2,
                            (screen_height - total_height) // 2 + i * (button_height + spacing),
                            350,
                            button_height
                        )
                        if button_rect.collidepoint(mouse_pos):
                            action()
                            menu_active = False
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    def show_game_config(self):
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Configuration de la Partie")
        
        font = pygame.font.Font("../data/font/CinzelDecorative-Regular.ttf", 24)
        button_image = pygame.image.load("../data/img/button.png")
        background = pygame.image.load("../data/img/background.png")
        logo = pygame.image.load("../data/img/logo2.png")
        back_arrow = pygame.image.load("../data/img/back_arrow.png")
        # Configuration par défaut
        config = {
            'type_game': 'LEAN',
            'map_type': 'GENEROUS',
            'nb_players': 2,
            'size_x': 120,
            'size_y': 120
        }
        
        # Options disponibles
        game_types = ['LEAN', 'MEAN', 'MARINES']
        map_types = ['GENEROUS', 'CENTER']
        player_range = range(2, 9)
        size_range = range(120, 241, 20)
        
        selected_option = None
        config_active = True
        
        while config_active:
            screen.fill((0, 0, 0))
            screen_width, screen_height = screen.get_size()
            screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
            logo_x = (screen_width - self.logo_size[0]) // 2
            screen.blit(pygame.transform.scale(logo, self.logo_size), (logo_x, 20))
            # Position de départ pour les options
            start_y = 200
            spacing = 60
            current_y = start_y
            mouse_pos = pygame.mouse.get_pos()
            back_button_size = (50, 50)
            back_button_rect = pygame.Rect(20, 20, back_button_size[0], back_button_size[1])
            screen.blit(pygame.transform.scale(back_arrow, back_button_size), back_button_rect)
            def draw_config_button(text, value, y_pos, options=None):
                button_width = 350
                button_height = 50
                button_x = (screen_width - button_width) // 2
                
                button_rect = pygame.Rect(button_x, y_pos, button_width, button_height)
                is_hovered = button_rect.collidepoint(mouse_pos)
                
                scaled_button = pygame.transform.scale(button_image, (button_width, button_height))
                screen.blit(scaled_button, button_rect.topleft)
                
                label = font.render(f"{text}: {value}", True, (255, 255, 255))
                label_rect = label.get_rect(center=button_rect.center)
                screen.blit(label, label_rect)
                
                return button_rect
            
            # Dessiner les options
            buttons = {}
            buttons['type_game'] = draw_config_button("Type de jeu", config['type_game'], current_y)
            current_y += spacing
            
            buttons['map_type'] = draw_config_button("Type de carte", config['map_type'], current_y)
            current_y += spacing
            
            buttons['nb_players'] = draw_config_button("Nombre de joueurs", config['nb_players'], current_y)
            current_y += spacing
            
            buttons['size_x'] = draw_config_button("Largeur de la carte", config['size_x'], current_y)
            current_y += spacing
            
            buttons['size_y'] = draw_config_button("Hauteur de la carte", config['size_y'], current_y)
            current_y += spacing
            
            # Bouton de démarrage
            start_button_rect = draw_config_button("Démarrer la partie", "", current_y + 20)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config_active = False
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for key, rect in buttons.items():
                        if back_button_rect.collidepoint(mouse_pos):
                            config_active = False
                            self.show_menu()
                            return
                        if rect.collidepoint(mouse_pos):
                            selected_option = key
                            if key == 'type_game':
                                current_index = game_types.index(config[key])
                                config[key] = game_types[(current_index + 1) % len(game_types)]
                            elif key == 'map_type':
                                current_index = map_types.index(config[key])
                                config[key] = map_types[(current_index + 1) % len(map_types)]
                            elif key == 'nb_players':
                                current_index = list(player_range).index(config[key])
                                config[key] = list(player_range)[(current_index + 1) % len(player_range)]
                            elif key in ['size_x', 'size_y']:
                                current_index = list(size_range).index(config[key])
                                config[key] = list(size_range)[(current_index + 1) % len(size_range)]
                    
                    if start_button_rect.collidepoint(mouse_pos):
                        # Convertir le type de carte en MapType
                        pygame.quit()
                        type_ressource = MapType.GENEROUS_RESOURCES if config['map_type'] == 'GENEROUS' else MapType.CENTER_RESOURCES
                        
                        # Initialiser la nouvelle partie avec les configurations choisies
                        self.controllerMap = ControllerMap(config['size_x'], config['size_y'])
                        self.controllerMap.map.mapType = type_ressource
                        self.controllerMap.genRessources(type_ressource)
                        self.initialize(config['type_game'], config['nb_players'])
                        self.controllerMap.setLstPlayers(self.lstPlayers)
                        self.game.setMap(self.controllerMap.map)
                        for player in self.lstPlayers:
                            self.game.lstPlayer.append(player.getPlayer())
                        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
                        config_active = False
                        self.start()
                
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

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

        if self.isSaved:
            file_name_temp = f"../save/{self.nameFile}"
            os.remove(file_name_temp)

        file_name = f"../save/save_{current_time}.dat"
        file = open(file_name, 'wb')
        pickle.dump(self.game, file)
        file.close()
        logs("Gave Saved", level=logging.INFO)
        
    def loadGame(self,path_file):
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
            
    def show_load_game_menu(self, screen, font):
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

            clock.tick(200)

    def start(self):
        self.controllerGame.run()

    def show_credits(self):
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Crédits")
        
        font_title = pygame.font.Font("../data/font/CinzelDecorative-Regular.ttf", 40)
        font_text = pygame.font.Font("../data/font/CinzelDecorative-Regular.ttf", 24)
        button_image = pygame.image.load("../data/img/button.png")
        background = pygame.image.load("../data/img/background.png")
        
        credits = [
            "Développeurs",
            "Valentin STADLER",
            "Goran VALIDZIC",
            "Nora MASSOT",
            "Amélie Sauvan-Magnet",
            "Gabriel SCAVONE",
            "Melvin MINVIELLE",
            "",
            "Game Design",
            "Goran VALIDZIC",
            "Gabriel SCAVONE",
            "",
            "Remerciements spéciaux",
            "à Monsieur HUGOT"
        ]
        
        credits_active = True
        scroll_position = screen.get_height()
        scroll_speed = 1
        
        while credits_active:
            screen.fill((0, 0, 0))
            screen_width, screen_height = screen.get_size()
            screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
            list = [0,8,12,13]
            # Affichage des crédits avec défilement
            current_y = scroll_position
            for i, line in enumerate(credits):
                if i in list:  # Pour les titres de sections
                    text = font_title.render(line, True, (255, 215, 0))  # Or pour les titres
                else:
                    text = font_text.render(line, True, (255, 255, 255))  # Blanc pour le texte
                
                text_rect = text.get_rect(center=(screen_width/2, current_y))
                screen.blit(text, text_rect)
                current_y += 60
            
            scroll_position -= scroll_speed
            
            # Réinitialiser le défilement quand tous les crédits sont passés
            if scroll_position < -current_y + screen_height/2:
                scroll_position = screen.get_height()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    credits_active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        credits_active = False
                        self.show_menu()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    credits_active = False
                    self.show_menu()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)