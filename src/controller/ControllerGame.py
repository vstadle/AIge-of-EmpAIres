import curses
import pygame
import sys
import webbrowser
import os
import logging  

from logs.logger import logs
from web.generate_html import generateHtml

from controller.ControllerMap import ControllerMap
from controller.ControllerPlayer import ControllerPlayer

from view.ViewTerminal import ViewTerminal
from view.ViewPygame import ViewPygame

from model.Game import Game
from model.Gold import Gold

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

    def run(self):

        self.viewTerminal = ViewTerminal(self.cmap.map)
        curses.wrapper(self.run_terminal)

    def run_terminal(self, stdscr):

        stdscr.nodelay(True)

        tab_pressed = False

        pos_x, pos_y = 0, 0

        #Test Collecte des ressources avec un villageois
        '''
        self.cmap.map.mapRessources[0][0] = Gold()
        self.cmap.map.mapRessources[0][0].setXY(0, 0)
        self.cmap.map.map[0][0] = "G"
        self.cmap.map.map[0][1] = "v"
        self.lstcPlayers[0].collectResources(self.lstcPlayers[0].player.units[0], self.cmap.map.mapRessources[0][0], 2, 2)
        '''
        logs(self.lstcPlayers[0].__str__(), level=logging.INFO)
        for unit in self.lstcPlayers[0].player.units:
            logs(unit.__str__(), level=logging.INFO)

        logs("Size of the map: " + str(len(self.cmap.map.map)) + "x" + str(len(self.cmap.map.map[0])), level=logging.INFO)
        logs(self.lstcPlayers[0].player.__repr__(), level=logging.INFO)

        self.lstcPlayers[0].move(self.lstcPlayers[0].player.units[0], 119, 1)
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
                    cplayer.updating_collect()
                    cplayer.updating_moving()

                self.viewTerminal.draw_map(stdscr, pos_x, pos_y)
        
    def change_mode(self):
        pygame.init()
        self.viewPygame = ViewPygame(self.cmap.map)
        self.run_pygame()

    def run_pygame(self):
        frame_counter = 0
        tab_pressed = False
        pos_x, pos_y = 0, 0
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.uiHandler.saveGame()
                        sys.exit()
                    if event.key == pygame.K_v:
                        pygame.quit()
                        return
                    if event.key == pygame.K_TAB and not tab_pressed:
                        tab_pressed = True
                        self.toggle_pause()
        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab_pressed = False
                    
                if not self.paused:

                    key = pygame.key.get_pressed()
                    if key[pygame.K_z]:
                        pos_y -= 1
                    if key[pygame.K_s]:
                        pos_y += 1
                    if key[pygame.K_q]:
                        pos_x -= 1
                    if key[pygame.K_d]:
                        pos_x += 1
                    if key[pygame.K_ESCAPE]: webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    
                    self.viewPygame.draw_map_2_5D(pos_x, pos_y)
                    pygame.display.flip()
                    
                    for cplayer in self.lstcPlayers:
                        cplayer.update_training()
                        cplayer.update_building()
                        cplayer.updating_collect()
                        cplayer.updating_moving()
                    
                    clock.tick(60)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            logs("Paused", level=logging.INFO)
            generateHtml(self.lstcPlayers)
            current_path = "file://" + os.getcwd() + "/web/index.html"
            webbrowser.open(current_path)
        else:
            logs("Unpaused", level=logging.INFO)
