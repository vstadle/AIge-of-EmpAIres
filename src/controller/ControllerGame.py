import curses
import pygame
import sys
import webbrowser
import os
import logging  
import time

from logs.logger import logs
from web.generate_html import generateHtml

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer

from view.ViewTerminal import ViewTerminal
from view.ViewPygame import ViewPygame

from model.Game import Game
from view.Camera import Camera

from model.Gold import Gold
from model.TownCenter import TownCenter
from model.Farm import Farm

from ai.ai import AI

class ControllerGame():

    log_win = None

    def __init__(self, cmap, lstcPlayers, game , uiHandler):
        
        self.cmap = cmap
        self.lstcPlayers = lstcPlayers
        
        self.game = Game()
        self.game.setMap(self.cmap.map)
        for cplayer in lstcPlayers:
            self.game.addPlayer(cplayer.player)

        self.uiHandler = uiHandler
    
        self.viewTerminal = None
        self.viewPygame = None

        self.mode = "terminal"
        self.paused = False
        self.zoom_level = 1.0

        self.lstAI = []
        for cplayer in lstcPlayers:
            self.lstAI.append(AI(self.game, cplayer))

        self.stdscr = None

    def run(self):

        self.viewTerminal = ViewTerminal(self.cmap.map)
        curses.wrapper(self.run_terminal)

    def run_terminal(self, stdscr):

        self.stdscr = stdscr

        stdscr.nodelay(True)

        tab_pressed = False

        pos_x, pos_y = 0, 0

        time_to_update = 0.5

        start_time = time.time()

        #Test Collecte des ressources avec un villageois
        '''
        self.cmap.map.mapRessources[0][0] = Gold()
        self.cmap.map.mapRessources[0][0].setXY(0, 0)
        self.cmap.map.map[0][0] = "G"
        self.cmap.map.map[0][1] = "v"
        self.lstcPlayers[0].collectResources(self.lstcPlayers[0].player.units[0], self.cmap.map.mapRessources[0][0], 2, 2)
        '''

        '''
        logs(self.lstcPlayers[0].__str__(), level=logging.INFO)
        for unit in self.lstcPlayers[0].player.units:
            logs(unit.__str__(), level=logging.INFO)
        '''

        logs("List player in the game :")
        for cplayer in self.lstcPlayers:
            logs(cplayer.player.__repr__(), level=logging.INFO)

        logs("Size of the map: " + str(len(self.cmap.map.map)) + "x" + str(len(self.cmap.map.map[0])), level=logging.INFO)

        logs("Game started", level=logging.INFO)
    
        #self.lstcPlayers[0].addBuilding(TownCenter(), 10, 10)
        
        #self.lstcPlayers[0].player.gold = 50

        logs("Nb d'IA : " + str(len(self.lstAI)), level=logging.INFO)


        #self.lstcPlayers[0].addBuilding(Farm(), 10, 10)

        #self.lstcPlayers[0].move(self.lstcPlayers[0].player.units[0], 119, 1)

        for ai in self.lstAI:
            ai.start_strategie()

        while True:
            #stdscr.refresh()
            current_time = time.time()
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
                    self.viewTerminal.camera.move(-1, 0, stdscr)
                elif key == ord('s'):
                    self.viewTerminal.camera.move(1, 0, stdscr)
                elif key == ord('q'):
                    self.viewTerminal.camera.move(0, -1, stdscr)
                elif key == ord('d'):
                    self.viewTerminal.camera.move(0, 1, stdscr)
                elif key == ord('p'):
                    self.uiHandler.saveGame()
                    stdscr.clear()
                    sys.exit()
                elif key == ord('v'):
                    self.change_mode()

                if current_time - start_time > time_to_update:
                    start_time = current_time
                    for ai in self.lstAI:
                        ai.choose_strategie()
                
                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    cplayer.update_building()
                    cplayer.updating_collect()
                    cplayer.updating_moving()

                self.viewTerminal.draw_map(stdscr)
        
    def change_mode(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.viewPygame = ViewPygame(119, 119, self.cmap.map,self.clock,self.game)
        self.run_pygame()

    def run_pygame(self):
        frame_counter = 0
        tab_pressed = False
        pos_x, pos_y = 0, 0
        running = True
        
        while running:
            self.viewPygame.camera.handle_input()            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.stdscr.clear()
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
                    
            if not self.paused:
                
                if keys[pygame.K_ESCAPE]:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                
                self.viewPygame.draw_map_2_5D()
                pygame.display.flip()
                check = 0
                check2 = 0
                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    check = cplayer.update_building()
                    cplayer.updating_collect()
                    cplayer.updating_moving()
                    if(check==0):
                        check2+=1
                if check2!=0:
                    self.viewPygame.create_static_minimap()

                    
    
            self.clock.tick(200)  # Limité à 150 FPS
        # Cleanup après la boucle
        pygame.quit()
        sys.exit()
        
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            logs("GAME PAUSED", level=logging.INFO)
            generateHtml(self.lstcPlayers)
            current_path = "file://" + os.getcwd() + "/web/index.html"
            webbrowser.open(current_path)
        else:
            logs("GAME UNPAUSED", level=logging.INFO)
