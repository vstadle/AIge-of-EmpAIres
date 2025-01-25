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

class SliderControl:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, button_image):
        # Zone complète du slider (incluant le texte)
        self.full_height = 100  # Augmentation de la hauteur totale
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.grabbed = False
        self.handle_width = 20
        self.handle_height = height + 10
        self.button_image = button_image
        
    def get_handle_rect(self):
        value_ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + (self.rect.width - self.handle_width) * value_ratio
        handle_y = self.rect.y - 5
        return pygame.Rect(handle_x, handle_y, self.handle_width, self.handle_height)
    
    def handle_event(self, event, mouse_pos):
        handle_rect = self.get_handle_rect()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if handle_rect.collidepoint(mouse_pos):
                self.grabbed = True
            elif self.rect.collidepoint(mouse_pos):
                self.grabbed = True
                rel_x = mouse_pos[0] - self.rect.x
                ratio = max(0, min(1, rel_x / self.rect.width))
                self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
                self.value = max(self.min_val, min(self.max_val, self.value))
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False
        
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            rel_x = mouse_pos[0] - self.rect.x
            ratio = max(0, min(1, rel_x / self.rect.width))
            self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
            self.value = max(self.min_val, min(self.max_val, self.value))
    
    def draw(self, screen, font, label):
        # Calculer la zone complète du slider (texte + barre)
        button_width = 350  # Même largeur que les autres boutons
        full_rect = pygame.Rect(
            self.rect.x - (button_width - self.rect.width) // 2,  # Centrer par rapport à la barre
            self.rect.y - 60,  # Position plus haute pour inclure le texte
            button_width,  # Largeur égale aux autres boutons
            self.full_height  # Hauteur totale incluant le texte et le slider
        )
        
        # Dessiner le fond complet avec l'image du bouton
        scaled_button = pygame.transform.scale(self.button_image, (full_rect.width, full_rect.height))
        screen.blit(scaled_button, full_rect.topleft)
        
        # Dessiner la barre du slider
        pygame.draw.rect(screen, (80, 80, 80), self.rect)
        
        # Dessiner le curseur
        handle_rect = self.get_handle_rect()
        handle_color = (200, 200, 100) if self.grabbed else (160, 82, 45)
        pygame.draw.rect(screen, handle_color, handle_rect)
        
        # Afficher la valeur et le label
        value_text = font.render(f"{label}: {self.value}", True, (255, 255, 255))
        text_rect = value_text.get_rect(center=(full_rect.centerx, self.rect.y - 20))
        screen.blit(value_text, text_rect)
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
        self.font = None
        self.screen = None

    def show_menu(self):
        logo_click_count = 0
        last_click_time = 0
        click_timeout = 500 #Easter Egg
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Menu Principal")
        
        # Charger les ressources
        background = pygame.image.load("../data/img/background.png")
        button_image = pygame.image.load("../data/img/button.png")
        font = pygame.font.Font("../data/font/CinzelDecorative-Regular.ttf", 32)
        self.font = font
        logo = pygame.image.load("../data/img/logo2.png")
        buttons = [
            ("Nouvelle Partie", self.show_game_config),
            ("Charger Partie", lambda: self.show_load_game_menu()),
            ("Quitter", sys.exit)
        ]
        
        menu_active = True
        
        while menu_active:
            self.screen.fill((0, 0, 0))
            screen_width, screen_height = self.screen.get_size()
            self.screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
            
            
            logo_x = (screen_width - self.logo_size[0]) // 2
            logo_rect = pygame.Rect(logo_x, 20, self.logo_size[0], self.logo_size[1])
            self.screen.blit(pygame.transform.scale(logo, self.logo_size), (logo_x, 20))

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
                self.screen.blit(scaled_button, button_rect.topleft)
                
                # centrer le texte
                label = font.render(text, True, (255, 255, 255))
                label_rect = label.get_rect(center=button_rect.center)
                self.screen.blit(label, label_rect)
                
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
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    def show_game_config(self):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Configuration de la Partie")
        
        font = pygame.font.Font("../data/font/CinzelDecorative-Regular.ttf", 24)
        button_image = pygame.image.load("../data/img/button.png")
        background = pygame.image.load("../data/img/background.png")
        back_arrow = pygame.image.load("../data/img/back_arrow.png")
        
        config = {
            'type_game': 'LEAN',
            'map_type': 'CENTER',
            'nb_players': 2,
            'size_x': 120,
            'size_y': 120
        }
        
        game_types = ['LEAN', 'MEAN', 'MARINES']
        map_types = ['GENEROUS', 'CENTER']
        player_range = range(2, 41)
        
        slider_width = 300
        slider_x = (800 - slider_width) // 2
        
        slider_x_coord = SliderControl(slider_x, 340, slider_width, 10, 120, 3000, config['size_x'], button_image)
        slider_y_coord = SliderControl(slider_x, 440, slider_width, 10, 120, 3000, config['size_y'], button_image)
        
        selected_option = None
        config_active = True
        
        while config_active:
            screen.fill((0, 0, 0))
            screen_width, screen_height = screen.get_size()
            screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
            
            start_y = 50
            spacing = 60
            slider_spacing = 100
            current_y = start_y
            mouse_pos = pygame.mouse.get_pos()
            
            back_button_size = (50, 50)
            back_button_rect = pygame.Rect(20, 20, back_button_size[0], back_button_size[1])
            screen.blit(pygame.transform.scale(back_arrow, back_button_size), back_button_rect)
            
            def draw_config_button(text, value, y_pos, options=None, width=350, height=50):
                button_width = width
                button_height = height
                button_x = (screen_width - button_width) // 2
                
                button_rect = pygame.Rect(button_x, y_pos, button_width, button_height)
                is_hovered = button_rect.collidepoint(mouse_pos)
                
                scaled_button = pygame.transform.scale(button_image, (button_width, button_height))
                screen.blit(scaled_button, button_rect.topleft)
                
                label = font.render(f"{text}: {value}" if value else text, True, (255, 255, 255))
                label_rect = label.get_rect(center=button_rect.center)
                screen.blit(label, label_rect)
                
                return button_rect
            
            buttons = {}
            buttons['type_game'] = draw_config_button("Type de jeu", config['type_game'], current_y)
            current_y += spacing
            
            buttons['map_type'] = draw_config_button("Type de carte", config['map_type'], current_y)
            current_y += spacing
            
            buttons['nb_players'] = draw_config_button("Nombre de joueurs", config['nb_players'], current_y)
            current_y += 2 * spacing
            
            slider_x_coord.rect.y = current_y + 20
            slider_x_coord.draw(screen, font, "Largeur de la carte")
            current_y += slider_spacing
            
            slider_y_coord.rect.y = current_y + 20
            slider_y_coord.draw(screen, font, "Hauteur de la carte")
            current_y += slider_spacing - 20
            
            config['size_x'] = slider_x_coord.value
            config['size_y'] = slider_y_coord.value
            
            start_button_rect = draw_config_button("Démarrer la partie", "", current_y + 20, None, 520, 80)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config_active = False
                    pygame.quit()
                    sys.exit()
                
                # Gestion des sliders
                slider_x_coord.handle_event(event, mouse_pos)
                slider_y_coord.handle_event(event, mouse_pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button_rect.collidepoint(mouse_pos):
                        config_active = False
                        self.show_menu()
                        return
                    
                    if start_button_rect.collidepoint(mouse_pos):
                        # Réinitialisation complète du jeu
                        self.game = Game()  # Créer une nouvelle instance de Game
                        self.lstPlayers = []  # Réinitialiser la liste des joueurs
                        
                        # Initialiser la carte avec les dimensions choisies
                        self.controllerMap = ControllerMap(config['size_x'], config['size_y'])
                        
                        # Initialiser les joueurs et leurs unités
                        self.initialize(config['type_game'], config['nb_players'])
                        
                        # Configurer le type de carte et générer les ressources
                        if config['map_type'] == 'CENTER':
                            self.controllerMap.map.setMapType(MapType.CENTER_RESOURCES)
                            self.controllerMap.map.generateCenterResources()
                        else:
                            self.controllerMap.map.setMapType(MapType.GENEROUS_RESOURCES)
                            self.controllerMap.map.generateGenerousResources()
                            
                        # Générer la forêt
                        self.controllerMap.map.generateForest()

                        # Mettre à jour la map avec les joueurs
                        self.controllerMap.setLstPlayers(self.lstPlayers)
                        
                        # Mettre à jour l'objet Game avec les données initiales
                        lsttemp = []
                        for player in self.lstPlayers:
                            lsttemp.append(player.getPlayer())
                        self.game.setLstPlayer(lsttemp)
                        self.game.setMap(self.controllerMap.map)
                        
                        # Créer le contrôleur de jeu
                        self.controllerGame = ControllerGame(self.controllerMap, self.lstPlayers, self.game, self)
                        
                        config_active = False
                        pygame.quit()
                        self.start()
                    
                    for key, rect in buttons.items():
                        if rect.collidepoint(mouse_pos):
                            selected_option = key
                            if key == 'type_game':
                                current_index = game_types.index(config[key])
                                config[key] = game_types[(current_index + 1) % len(game_types)]
                            elif key == 'map_type':
                                current_index = map_types.index(config[key])
                                config[key] = map_types[(current_index + 1) % len(map_types)]
                            elif key == 'nb_players':
                                current_index = player_range.index(config[key])
                                config[key] = player_range[(current_index + 1) % len(player_range)]
    def saveGame(self):
        if not os.path.exists("../save"):
            os.makedirs("../save")
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
            
    def show_load_game_menu(self):  # ASM
        if not pygame.display.get_surface():
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))

        pygame.display.set_caption("Charger une partie")

        clock = pygame.time.Clock()
        files = [file for file in os.listdir('../save/') if file.endswith('.dat')]
        scroll_offset = 0
        scroll_speed = 20
        selected_file = None

        # Charger les images des boutons
        load_icon = pygame.image.load('../data/img/lgm_load_icon.png')
        rename_icon = pygame.image.load('../data/img/lgm_rename_icon.png')
        delete_icon = pygame.image.load('../data/img/lgm_delete_icon.png')
        back_icon = pygame.image.load('../data/img/lgm_back_icon.png')

        # Redimensionner les icônes
        icon_size = (50, 50)
        load_icon = pygame.transform.scale(load_icon, icon_size)
        rename_icon = pygame.transform.scale(rename_icon, icon_size)
        delete_icon = pygame.transform.scale(delete_icon, icon_size)
        back_icon = pygame.transform.scale(back_icon, icon_size)

        def text_input(prompt):
            """Affiche une boîte de saisie pour entrer du texte."""
            input_active = True
            user_text = ""
            font = pygame.font.Font(None, 36)

            while input_active:
                self.screen.fill((50, 50, 50))
                prompt_surface = font.render(prompt, True, (255, 255, 255))
                prompt_rect = prompt_surface.get_rect(center=(400, 200))
                self.screen.blit(prompt_surface, prompt_rect.topleft)

                # Afficher le texte saisi
                text_surface = font.render(user_text, True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(400, 300))
                self.screen.blit(text_surface, text_rect.topleft)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode

            return user_text

        load_game_active = True
        while load_game_active:
            self.screen.fill((200, 200, 200))
            mouse_pos = pygame.mouse.get_pos()

            # Afficher la liste des fichiers
            y = 100 - scroll_offset
            file_positions = []

            for file in files:
                if file == selected_file:
                    color = (0, 200, 0)  # Vert pour le fichier sélectionné
                elif pygame.Rect(100, y, 400, 30).collidepoint(mouse_pos):
                    color = (200, 200, 0)  # Doré au survol
                else:
                    color = (255, 255, 255)  # Blanc par défaut

                label = self.font.render(file, True, color)
                rect = label.get_rect(topleft=(100, y))
                self.screen.blit(label, rect.topleft)
                file_positions.append((file, rect))
                y += 40

            # Afficher les boutons
            icon_positions = {}

            # Bouton "Retour"
            back_rect = pygame.Rect(20, 20, *icon_size)
            self.screen.blit(back_icon, back_rect)
            icon_positions["Retour"] = back_rect

            # Boutons "Charger", "Renommer", "Effacer" si un fichier est sélectionné
            if selected_file:
                selected_index = files.index(selected_file)
                selected_y = 100 + selected_index * 40 - scroll_offset

                icon_positions.update({
                    "Charger": pygame.Rect(600, selected_y, *icon_size),
                    "Renommer": pygame.Rect(660, selected_y, *icon_size),
                    "Effacer": pygame.Rect(720, selected_y, *icon_size),
                })

                self.screen.blit(load_icon, icon_positions["Charger"].topleft)
                self.screen.blit(rename_icon, icon_positions["Renommer"].topleft)
                self.screen.blit(delete_icon, icon_positions["Effacer"].topleft)

            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        # Vérifie les clics sur les boutons d'action
                        for action, rect in icon_positions.items():
                            if rect.collidepoint(mouse_pos):
                                if action == "Charger" and selected_file:
                                    self.loadGame(selected_file)
                                    load_game_active = False
                                elif action == "Renommer" and selected_file:
                                    while True:
                                        new_name = text_input("Entrez un nouveau nom (sans extension) :")
                                        if not new_name:
                                            break  # Annuler le renommage si aucun nom n'est saisi

                                        new_file = f"{new_name}.dat"

                                        # Vérifier si le fichier existe déjà
                                        if os.path.exists(f"../save/{new_file}"):
                                            text_input(f"Le fichier '{new_file}' existe déjà. Appuyez sur Entrée")
                                        else:
                                            try:
                                                os.rename(f"../save/{selected_file}", f"../save/{new_file}")
                                                files = [file for file in os.listdir('../save/') if file.endswith('.dat')]
                                                selected_file = None
                                                break  # Renommage réussi
                                            except Exception as e:
                                                text_input(f"Erreur lors du renommage : {e}")
                                                break





                                elif action == "Effacer" and selected_file:
                                    confirm = text_input(f"Confirmer suppression de {selected_file} ? (o/n)")
                                    if confirm.lower() == 'o':
                                        os.remove(f"../save/{selected_file}")
                                        files = [file for file in os.listdir('../save/') if file.endswith('.dat')]
                                        selected_file = None
                                elif action == "Retour":
                                    load_game_active = False
                                    self.show_menu()

                        # Vérifie si un fichier est sélectionné
                        for file, rect in file_positions:
                            if rect.collidepoint(mouse_pos):
                                selected_file = file
                                break
                        else:
                            selected_file = None  # Aucun fichier sélectionné

                    # Gérer le défilement
                    elif event.button == 4:  # Molette haut
                        scroll_offset = max(0, scroll_offset - scroll_speed)
                    elif event.button == 5:  # Molette bas
                        scroll_offset = min(max(0, len(files) * 40 - 400), scroll_offset + scroll_speed)

                clock.tick(60)
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
            "Remerciement spécial",
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
            total_credits_height = len(credits) * 60
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
            if scroll_position < -total_credits_height:
                scroll_position = screen_height
           
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
                
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    def display_winner(self, winner_name): #ASM
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        screen.fill((0, 0, 0))  # Efface l'écran
        font = pygame.font.Font(None, 74)
        text = font.render(f"Le joueur {winner_name} a gagné !", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 300))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(5000)  # Attend 5 secondes avant de fermer