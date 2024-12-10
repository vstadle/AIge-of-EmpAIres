import pygame
import sys
from model.Farm import Farm
from model.Keep import Keep
from model.Barracks import Barracks
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.House import House
from model.Camp import Camp
from model.TownCenter import TownCenter
class ViewMap():
    def __init__(self, map, cmap):
        self.map = map
        self.cmap = cmap
        
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 30
        
        display_info = pygame.display.Info()
        screen_width = int(display_info.current_w * 0.8)
        screen_height = int(display_info.current_h * 0.8)
        
        self.TILE_SIZE = min(screen_width // self.GRID_WIDTH, screen_height // self.GRID_HEIGHT)
        
        self.ISO_ANGLE = 30 
        
        self.map_width = 120
        self.map_height = 120
        iso_factor = 0.5  
        self.iso_tile_width = self.TILE_SIZE
        self.iso_tile_height = self.TILE_SIZE * iso_factor
        self.total_iso_width = (self.map_width + self.map_height) * self.iso_tile_width // 2
        self.total_iso_height = (self.map_width + self.map_height) * self.iso_tile_height // 2

        self.MINIMAP_SIZE = 180  
        self.MINIMAP_SIZE2 = 120
        self.MINIMAP_PADDING = 20
        self.MINIMAP_TILE_SIZE = self.MINIMAP_SIZE // max(self.map_width, self.map_height) *1.5
        
        window_width = self.GRID_WIDTH * self.TILE_SIZE
        window_height = self.GRID_HEIGHT * self.TILE_SIZE
        self.screen = pygame.display.set_mode((window_width, window_height))
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN_LIGHT = (34, 139, 34)
        self.GREEN_DARK = (0, 70, 0)
        self.YELLOW = (255, 215, 0)
        self.BROWN = (127, 42, 42)
        self.BLUE = (135, 206, 250)
        self.RED = (255, 0, 0)
        
        self.font = pygame.font.Font(None, 30)

    def draw_map(self, screen, pos_x, pos_y):
        screen.fill(self.WHITE)
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x = col * self.TILE_SIZE
                y = row * self.TILE_SIZE
                pygame.draw.rect(screen, self.GRAY, (x, y, self.TILE_SIZE, self.TILE_SIZE))
                map_row = pos_y + row
                map_col = pos_x + col
                if 0 <= map_row < len(self.map.getMap()) and 0 <= map_col < len(self.map.getMap()[0]):
                    if self.map.getMap()[map_row][map_col] != ' ':
                        text_surface = self.font.render(self.map.getMap()[map_row][map_col], True, self.BLACK)
                        screen.blit(text_surface, (x + self.TILE_SIZE // 4, y + self.TILE_SIZE // 4))
        pygame.display.flip()
    def draw_minimap(self, screen, view_x, view_y, zoom_level):
        minimap_surface = pygame.Surface((self.MINIMAP_SIZE, self.MINIMAP_SIZE2))
        minimap_surface.fill(self.BLACK) 

        iso_minimap_tile_width = self.MINIMAP_TILE_SIZE
        iso_minimap_tile_height = self.MINIMAP_TILE_SIZE * 2/3

        minimap_center_x = self.MINIMAP_SIZE // 2
        minimap_center_y = self.MINIMAP_SIZE2 // 2

        for row in range(self.map_height):
            for col in range(self.map_width):
                iso_x = (col - row) * iso_minimap_tile_width // 2 + minimap_center_x
                iso_y = (col + row) * iso_minimap_tile_height // 2 + minimap_center_y - (self.map_height * iso_minimap_tile_height // 2)

                cell_content = self.map.getMap()[row][col]
                color = self.get_tile_color(cell_content)

                points = [
                    (iso_x, iso_y),
                    (iso_x + iso_minimap_tile_width // 2, iso_y + iso_minimap_tile_height // 2),
                    (iso_x, iso_y + iso_minimap_tile_height),
                    (iso_x - iso_minimap_tile_width // 2, iso_y + iso_minimap_tile_height // 2),
                ]
                pygame.draw.polygon(minimap_surface, color, points)

        total_map_width = self.map_width
        total_map_height = self.map_height

        minimap_tile_height_ratio = 1.34 # 4/3 = ratio longueur/hauteur ??

        viewport_width = (self.GRID_WIDTH / total_map_width) * self.MINIMAP_SIZE / zoom_level
        viewport_height = minimap_tile_height_ratio * (self.GRID_HEIGHT / total_map_height) * self.MINIMAP_SIZE / zoom_level
        
        viewport_x = (view_x / (total_map_width * self.iso_tile_width)) * self.MINIMAP_SIZE
        viewport_y = (view_y / (total_map_height * self.iso_tile_height)) * self.MINIMAP_SIZE2

        viewport_x = max(0, min((view_x / total_map_width) * self.MINIMAP_SIZE, self.MINIMAP_SIZE - viewport_width))
        viewport_y = max(0, min((view_y / total_map_height) * self.MINIMAP_SIZE, self.MINIMAP_SIZE2 - viewport_height))

        pygame.draw.rect(
            minimap_surface,
            self.RED,
            (viewport_x, viewport_y, viewport_width, viewport_height),
            2,
        )

        minimap_x = screen.get_width() - self.MINIMAP_SIZE - self.MINIMAP_PADDING
        minimap_y = screen.get_height() - self.MINIMAP_SIZE2 - self.MINIMAP_PADDING
        screen.blit(minimap_surface, (minimap_x, minimap_y))
    def draw_map_2_5D(self, screen, pos_x, pos_y, zoom_level):
        
        screen.fill(self.BLACK)
        map_surface_width = (self.map_width + self.map_height) * self.iso_tile_width // 2 * zoom_level
        map_surface_height = (self.map_width + self.map_height) * self.iso_tile_height // 2 * zoom_level
        iso_surface = pygame.Surface((map_surface_width, map_surface_height))
        iso_surface.fill(self.BLACK)
        diamond_left = self.map_height * self.iso_tile_width // 2 * zoom_level
        diamond_top = 0
        diamond_width = self.map_width * self.iso_tile_width // 2 * zoom_level
        diamond_height = (self.map_width + self.map_height) * self.iso_tile_height // 2 * zoom_level
        start_x = diamond_left
        start_y = 0
        
        for row in range(self.map_height):
            for col in range(self.map_width):
                iso_x = start_x + (col - row) * self.iso_tile_width // 2 * zoom_level
                iso_y = start_y + (col + row) * self.iso_tile_height // 2 * zoom_level
                
                if (iso_x >= diamond_left - diamond_width and 
                    iso_x <= diamond_left + diamond_width and
                    iso_y >= diamond_top and 
                    iso_y <= diamond_height):
                    
                    points = [
                        (iso_x, iso_y),  
                        (iso_x + self.iso_tile_width // 2 * zoom_level , iso_y + self.iso_tile_height // 2 * zoom_level),  
                        (iso_x, iso_y + self.iso_tile_height * zoom_level),  
                        (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y + self.iso_tile_height // 2 * zoom_level) 
                    ]
                    
                    cell_content = self.map.getMap()[row][col]
                    color = self.get_tile_color(cell_content)
                    
                    pygame.draw.polygon(iso_surface, color, points)
                    '''
                    pygame.draw.polygon(iso_surface, self.BLACK, points, 1)
                    '''
        
        max_scroll_x = map_surface_width - screen.get_width() + (self.iso_tile_width * zoom_level)
        max_scroll_y = map_surface_height - screen.get_height() + (self.iso_tile_height * zoom_level)
    
        view_x = max(0, min(pos_x * self.iso_tile_width * zoom_level, max_scroll_x))
        view_y = max(0, min(pos_y * self.iso_tile_height * zoom_level, max_scroll_y))
        
        screen.blit(iso_surface, (0, 0), 
                   (view_x, view_y, 
                    screen.get_width(), 
                    screen.get_height()))
        
        self.draw_minimap(screen, view_x, view_y, zoom_level)    
        pygame.display.flip()

    def get_tile_color(self, content):
        if content == ' ':
            return self.GREEN_LIGHT
        elif content == 'W':
            return self.GREEN_DARK
        elif content == 'G':
            return self.YELLOW
        elif content == 'A':
            return self.BLUE
        elif content == 'T':
            return self.WHITE
        elif content == 'B':
            return self.BROWN
        else:
            return self.GRAY