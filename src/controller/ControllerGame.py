import curses
import pygame
import sys
import webbrowser
import os

from web.generate_html import generateHtml

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer

from view.ViewTerminal import ViewTerminal
from view.ViewPygame import ViewPygame

from model.Game import Game
from view.Camera import Camera

class ControllerGame():
    def __init__(self, cmap, lstcPlayers, game, uiHandler, screen):
        self.curses_screen = screen  # Renommé pour clarté
        self.cmap = cmap
        self.lstcPlayers = lstcPlayers
        # Définir une taille par défaut pour la fenêtre Pygame
        self.width = 1550
        self.height = 865
        self.game = Game()
        self.game.setMap(self.cmap.map)
        for cplayer in lstcPlayers:
            self.game.addPlayer(cplayer.player)

        self.uiHandler = uiHandler
    
        self.viewTerminal = None
        self.viewPygame = None
        self.pygame_screen = None  # Sera initialisé plus tard

        self.mode = "terminal"
        self.paused = False
        self.zoom_level = 1.0
        self.camera = Camera(self.width, self.height,119,119)

    def run(self):

        self.viewTerminal = ViewTerminal(self.cmap.map)
        curses.wrapper(self.run_terminal)

    def run_terminal(self, stdscr):

        stdscr.nodelay(True)

        tab_pressed = False

        pos_x, pos_y = 0, 0

        while True:
            #stdscr.refresh()

            key = stdscr.getch()

            if key == 9:  # Si la touche "Tab" est pressée
                if not tab_pressed:
                    if self.paused:
                        self.toggle_pause()
                    else:
                        self.toggle_pause()
                    tab_pressed = True  # Empêcher de basculer l'état à chaque pression
            else:
                tab_pressed = False

            if not self.paused:

                if key == ord('z'):
                    pos_x -= 1
                elif key == ord('s'):
                    pos_x += 1
                elif key == ord('q'):
                    pos_y -= 1
                elif key == ord('d'):
                    pos_y += 1
                elif key == ord('p'):
                    self.uiHandler.saveGame()
                    stdscr.clear()
                    sys.exit()
                elif key == ord('v'):
                    self.change_mode()

                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    cplayer.update_building()

                self.viewTerminal.draw_map(stdscr, pos_x, pos_y)
        
    def change_mode(self):
        pygame.init()
        self.pygame_screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.viewPygame = ViewPygame(119, 119, self.width, self.height, self.pygame_screen,self.cmap.map,self.clock,self.game)
        self.run_pygame()

    def run_pygame(self):
        tab_pressed = False
        pos_x, pos_y = 0, 0
        running = True
        
        while running:
            self.camera.handle_input()            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.uiHandler.saveGame()
                        running = False
                        break
                    if event.key == pygame.K_v:
                        running = False
                        pygame.quit()
                        self.run()  # Retour à la vue curses
                        return 
                   
                    if event.key == pygame.K_F1:
                        self.viewPygame.show_player_info = not self.viewPygame.show_player_info
                        pygame.display.flip()
                    if event.key == pygame.K_TAB and not tab_pressed:
                        tab_pressed = True
                        self.toggle_pause()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  
                        self.zoom_level = round(min(3, self.zoom_level + 0.1), 1)
                    elif event.button == 5:  
                        self.zoom_level = round(max(0.5, self.zoom_level - 0.1), 1)
                        if self.zoom_level < 0.1:
                            self.zoom_level = 0.1
       

            if not running:
                break

            if not self.paused:
                if keys[pygame.K_z]:
                    pos_y -= 1
                if keys[pygame.K_s]:
                    pos_y += 1
                if keys[pygame.K_q]:
                    pos_x -= 1
                if keys[pygame.K_d]:
                    pos_x += 1
                if keys[pygame.K_ESCAPE]:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                
                self.viewPygame.draw_map_2_5D()
                pygame.display.flip()
                
                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    cplayer.update_building()
    
            self.clock.tick(200)  # Limité à 150 FPS
        # Cleanup après la boucle
        pygame.quit()
        sys.exit()
        
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            print("Paused")
            generateHtml(self.lstcPlayers)
            current_path = "file://" + os.getcwd() + "/web/index.html"
            webbrowser.open(current_path)
        else:
            print("Unpaused")
