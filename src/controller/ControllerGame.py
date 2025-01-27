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
            self.lstAI.append(AI(self.game, cplayer, lstcPlayers))

        self.stdscr = None

    def run(self):

        self.viewTerminal = ViewTerminal(self.cmap.map)
        curses.wrapper(self.run_terminal)

    def run_terminal(self, stdscr):

        self.stdscr = stdscr

        stdscr.nodelay(True)

        tab_pressed = False
        p_pressed = False

        pos_x, pos_y = 0, 0

        time_to_update = 60

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


        ''' On demande à chaque IA de choisir une stratégie au début de la partie '''
        for ai in self.lstAI:
            lsttemp = self.lstcPlayers.copy()
            lsttemp.remove(ai.cplayer)
            ai.choose_strategie(lsttemp)


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

            if key == ord('p'):
                if not p_pressed:
                    self.pause()
                else:
                    self.pause()
                p_pressed = False
            else:
                p_pressed = False

            if key == curses.KEY_F7 or key == curses.KEY_F11:
                self.uiHandler.saveGame()
            elif key == curses.KEY_F12:
                self.paused = True
                pygame.quit()
                self.uiHandler.show_menu()


            if not self.paused:

                if key == ord('z') or key == curses.KEY_UP:
                    self.viewTerminal.camera.move(0, -1, stdscr)
                elif key == ord('s') or key == curses.KEY_DOWN:
                    self.viewTerminal.camera.move(0, 1, stdscr)
                elif key == ord('q') or key == curses.KEY_LEFT:
                    self.viewTerminal.camera.move(-1, 0, stdscr)
                elif key == ord('d') or key == curses.KEY_RIGHT:
                    self.viewTerminal.camera.move(1, 0, stdscr)
                elif key == curses.KEY_F2 or key == curses.KEY_F9:
                    self.change_mode()

                if current_time - start_time > time_to_update:
                    start_time = time.time()
                    for ai in self.lstAI:
                        lsttemp = self.lstcPlayers.copy()
                        lsttemp.remove(ai.cplayer)
                        ai.choose_strategie(lsttemp)


                for ai in self.lstAI:
                        ai.update()
                        ai.verifLifeUnit()
                
                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    cplayer.update_building()
                    cplayer.updating_collect()
                    cplayer.updating_moving()
                    cplayer.updating_attack()

                self.viewTerminal.draw_map(stdscr)
        
    def change_mode(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.viewPygame = ViewPygame(self.cmap.size_map_x, self.cmap.size_map_y, self.cmap.map,self.clock,self.game)
        self.run_pygame()

    def run_pygame(self):
        frame_counter = 0
        tab_pressed = False
        p_pressed = False
        running = True
        time_to_update = 60
        
        start_time = time.time()
    
        while running:
            self.viewPygame.camera.handle_input()            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        self.stdscr.clear()
                        self.uiHandler.saveGame()
                        running = False
                        break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_k:  # Réduire HP
                        if self.lstcPlayers[0].player.buildings:
                            building = self.lstcPlayers[0].player.buildings[0]
                            building.setHp(building.getHp() - 100)
                        if self.lstcPlayers[0].player.units:
                            unit = self.lstcPlayers[0].player.units[0]
                            unit.setHp(unit.getHp() - 10)
                    elif event.key == pygame.K_F1:
                        self.viewPygame.show_player_info = not self.viewPygame.show_player_info
                        pygame.display.flip()
                    elif event.key == pygame.K_TAB and not tab_pressed:
                        tab_pressed = True
                        self.toggle_pause()
                    elif event.key == pygame.K_p and not p_pressed:
                        p_pressed = True
                        self.pause()
                    elif event.key == pygame.K_F9:
                        running = False
                        pygame.quit()
                        return
                    elif event.key == pygame.K_F12:
                        self.paused = True
                        pygame.quit()
                        self.uiHandler.show_menu()
                        return
                    elif event.key == pygame.K_F7 or event.key == pygame.K_F11:
                        self.uiHandler.saveGame()
                    elif event.key == pygame.K_m:
                        self.viewPygame.full_minimap_mode = not self.viewPygame.full_minimap_mode
                        self.viewPygame.minimap_zoom = 4.5  # Reset zoom when toggling
                        if self.viewPygame.full_minimap_mode:
                            self.viewPygame.full_minimap_offset_x = 0
                            self.viewPygame.full_minimap_offset_y = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False
                    elif event.key == pygame.K_p:
                        p_pressed = False
                        self.pause()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Minimap zoom and navigation
                    minimap_x = self.viewPygame.width - self.viewPygame.minimap_base.get_width() - 10
                    minimap_rect = pygame.Rect(minimap_x, 10, 
                                            self.viewPygame.minimap_base.get_width(), 
                                            self.viewPygame.minimap_base.get_height())
                    
                    if self.viewPygame.full_minimap_mode or minimap_rect.collidepoint(mouse_pos):
                        if event.button == 4:  # Scroll up (zoom in)
                            self.viewPygame.minimap_zoom = min(12.0, self.viewPygame.minimap_zoom * 1.1)
                        elif event.button == 5:  # Scroll down (zoom out)
                            self.viewPygame.minimap_zoom = max(4.5, self.viewPygame.minimap_zoom / 1.1)
            
            if not self.paused:
                if keys[pygame.K_ESCAPE]:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            
                self.viewPygame.draw_map_2_5D()
                pygame.display.flip()
                
                current_time = time.time()
                
                if current_time - start_time > time_to_update:
                    start_time = time.time()
                    for ai in self.lstAI:
                        lsttemp = self.lstcPlayers.copy()
                        lsttemp.remove(ai.cplayer)
                        ai.choose_strategie(lsttemp)
                
                for ai in self.lstAI:
                    ai.update()
                
                # Game update logic remains the same
                check = 0
                check2 = 0
                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    check = cplayer.update_building()
                    cplayer.updating_collect()
                    cplayer.updating_moving()
                    cplayer.updating_attack()
                    if check == 0:
                       check2 += 1

                # Mise à jour de la minimap seulement s'il y a eu une construction ou destruction
                if check2 != 0:
                    self.viewPygame.create_static_minimap()
            
            self.clock.tick(200)  # Limited to 200 FPS
        
        # Cleanup after the loop
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
    
    def pause(self):
        self.paused = not self.paused

