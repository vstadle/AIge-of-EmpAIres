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

class ControllerGame():

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
        self.viewPygame = ViewPygame(self.cmap.map)
        self.run_pygame()

    def run_pygame(self):
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
                    
                    clock.tick(30)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            print("Paused")
            generateHtml(self.lstcPlayers)
            current_path = "file://" + os.getcwd() + "/web/index.html"
            webbrowser.open(current_path)
        else:
            print("Unpaused")
