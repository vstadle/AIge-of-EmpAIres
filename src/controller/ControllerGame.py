import curses
import pygame
import sys

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


    def run(self):

        self.viewTerminal = ViewTerminal(self.cmap.map)
        self.viewPygame = ViewPygame(self.cmap.map)

        curses.wrapper(self.run_terminal)

    def run_terminal(self, stdscr):

        stdscr.nodelay(True)

        paused = False
        tab_pressed = False

        pos_x, pos_y = 0, 0

        while True:
            #stdscr.refresh()

            key = stdscr.getch()

            if key == 9 and not tab_pressed:
                paused = True
                print("Paused")
            elif key == 9 and tab_pressed:
                paused = False
                print("Unpaused")

            if not paused:

                if key == ord('z'):
                    pos_x += 1
                elif key == ord('s'):
                    pos_x -= 1
                elif key == ord('q'):
                    pos_y += 1
                elif key == ord('d'):
                    pos_y -= 1
                elif key == ord('p'):
                    self.uiHandler.saveGame()
                    sys.exit()
                elif key == ord('v'):
                    self.change_mode()

                for cplayer in self.lstcPlayers:
                    cplayer.update_training()
                    cplayer.update_building()

                self.viewTerminal.draw_map(stdscr, pos_x, pos_y)
        
    def change_mode(self):
        self.run_pygame()

    def run_pygame(self):
        pygame.init()
        paused = False
        pos_x, pos_y = 0, 0
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
                    if event.key == pygame.K_z:
                        paused = True
                        print("Tab pressed")
                    
                if not paused:

                    key = pygame.key.get_pressed()
                    if key[pygame.K_z]:
                        pos_y -= 1
                    if key[pygame.K_s]:
                        pos_y += 1
                    if key[pygame.K_q]:
                        pos_x -= 1
                    if key[pygame.K_d]:
                        pos_x += 1
                    
                    self.viewPygame.draw_map_2_5D(pos_x, pos_y)
                
