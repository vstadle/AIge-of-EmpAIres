import pygame
import sys
import os
import random
from model.Farm import Farm
from model.Keep import Keep
from model.Barracks import Barracks
from model.ArcheryRange import ArcheryRange
from model.Stable import Stable
from model.House import House
from model.Camp import Camp
from model.TownCenter import TownCenter



class ViewPygame():
    def __init__(self, map):
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.map = map
        self.update_window_size()
        pygame.event.set_allowed([pygame.QUIT,pygame.VIDEORESIZE ,pygame.KEYDOWN, pygame.KEYUP,pygame.MOUSEBUTTONDOWN])
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.mapBuildings = self.map.get_map_buildings()
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1080)
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
        
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN_LIGHT = (34, 139, 34)
        self.GREEN_DARK = (0, 70, 0)
        self.YELLOW = (255, 215, 0)
        self.BROWN = (127, 42, 42)
        self.BLUE = (135, 206, 250)
        self.RED = (255, 0, 0)
        self.load_sprite()
        self.load_tree_sprites()
        self.load_gold_sprites()
        self.barracks_sprite = self.load_barracks_sprite()
        self.towncenterleft_sprite = self.load_towncenterleft_sprite()
        self.towncenterright_sprite = self.load_towncenterright_sprite()
        self.towncentermiddle_sprite = self.load_towncentermiddle_sprite()
        self.tree_positions = {}
        self.gold_positions = {}
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def load_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        sprite_path = os.path.join(project_root, "Sprite_aoe", "miscellaneous","grass2.png")
        
        self.ground_sprite = pygame.image.load(sprite_path).convert_alpha()
        self.ground_sprite = pygame.transform.scale(self.ground_sprite,
                                                  (int(self.iso_tile_width),
                                                   int(self.iso_tile_height)))
        self.tower_sprite = pygame.image.load(os.path.join(project_root, "Sprite_aoe", "buildings", "towers.png")).convert_alpha()
        self.tower_sprite = pygame.transform.scale(self.tower_sprite,
                                                  (int(self.iso_tile_width),
                                                   int(self.iso_tile_height)))
    def load_gold_sprites(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        gold_path = os.path.join(project_root, "Sprite_aoe", "gold")
        self.gold_sprites = []
        
        for filename in os.listdir(gold_path):
            if filename.endswith(".bmp"):
                sprite_path = os.path.join(gold_path, filename)
                sprite = pygame.image.load(sprite_path).convert()
                sprite.set_colorkey((255, 0, 255))
                self.gold_sprites.append(sprite)
    def load_towncenterleft_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        towncenterleft_path = os.path.join(project_root, "Sprite_aoe", "towncenter","Towncenterleft14.bmp")
        towncenterleft = pygame.image.load(towncenterleft_path).convert()
        towncenterleft.set_colorkey((255,0,255))
        return self.scale_sprite(towncenterleft)

    def load_towncenterright_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        towncenterright_path = os.path.join(project_root, "Sprite_aoe", "towncenter","Towncenterright14.bmp")
        towncenterright = pygame.image.load(towncenterright_path).convert()
        towncenterright.set_colorkey((255,0,255))
        return self.scale_sprite(towncenterright)
    def load_towncentermiddle_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        towncentermiddle_path = os.path.join(project_root, "Sprite_aoe", "towncenter","Towncentermiddle14.bmp")
        towncentermiddle = pygame.image.load(towncentermiddle_path).convert()
        towncentermiddle.set_colorkey((255,0,255))
        return self.scale_sprite(towncentermiddle)
    

        
    def load_tree_sprites(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        trees_path = os.path.join(project_root, "Sprite_aoe", "trees")
        self.tree_sprites = []
        
        for filename in os.listdir(trees_path):
            if filename.endswith(".bmp"):
                sprite_path = os.path.join(trees_path, filename)
                sprite = pygame.image.load(sprite_path).convert()
                sprite.set_colorkey((255, 0, 255))
                self.tree_sprites.append(sprite)
    '''    
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
    '''

    def update_window_size(self):
        display_info = pygame.display.Info()
        self.screen_width = int(display_info.current_w * 0.8)
        self.screen_height = int(display_info.current_h * 0.8)
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 30
        self.TILE_SIZE = min(self.screen_width // self.GRID_WIDTH, self.screen_height // self.GRID_HEIGHT)
        
        self.ISO_ANGLE = 30
        self.map_width = 120 
        self.map_height = 120
        
        # Mettre à jour les dimensions isométriques
        iso_factor = 0.5
        self.iso_tile_width = self.TILE_SIZE
        self.iso_tile_height = self.TILE_SIZE * iso_factor
        
        # Recalculer les dimensions de la minimap
        self.MINIMAP_SIZE = int(self.screen_width * 0.15)  # 15% de la largeur
        self.MINIMAP_SIZE2 = int(self.screen_height * 0.15) # 15% de la hauteur
        self.MINIMAP_PADDING = 20
        self.MINIMAP_TILE_SIZE = self.MINIMAP_SIZE // max(self.map_width, self.map_height) * 1.5

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
        self.display_fps(screen)
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
        self.clock.tick(self.FPS)
        
        for event in pygame.event.get(pygame.VIDEORESIZE):
            self.screen_width = event.w
            self.screen_height = event.h
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            self.update_window_size()
        
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
                        (iso_x + self.iso_tile_width // 2 * zoom_level, iso_y + self.iso_tile_height // 2 * zoom_level),  
                        (iso_x, iso_y + self.iso_tile_height * zoom_level),  
                        (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y + self.iso_tile_height // 2 * zoom_level)
                    ]

                    cell_content = self.map.getMap()[row][col]
                    color = self.get_tile_color(cell_content)

                    if cell_content == ' ':
                        scaled_sprite = pygame.transform.scale(
                            self.ground_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                    elif cell_content == 'W':
                        scaled_sprite = pygame.transform.scale(
                            self.ground_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                        
                        if (row, col) not in self.tree_positions:
                            self.tree_positions[(row, col)] = random.choice(self.tree_sprites)

                        tree_sprite = self.tree_positions[(row, col)]
                        scaled_tree_sprite = pygame.transform.scale(
                            tree_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_tree_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                    elif cell_content == 'T':
                        scaled_sprite = pygame.transform.scale(
                            self.ground_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                    elif cell_content == 'G':
                        scaled_sprite = pygame.transform.scale(
                            self.ground_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                        
                        if (row, col) not in self.gold_positions:
                            self.gold_positions[(row, col)] = random.choice(self.gold_sprites)

                        gold_sprite = self.gold_positions[(row, col)]
                        scaled_gold_sprite = pygame.transform.scale(
                            gold_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_gold_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                    elif cell_content == 'B':
                        scaled_sprite = pygame.transform.scale(
                            self.ground_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                    else:
                        pygame.draw.polygon(iso_surface, color, points)

                    building = self.mapBuildings[row][col]
                    if building is not None:
                        if isinstance(building, Barracks):
                            building_x, building_y = self.get_building_top_left(building)

                            if self.is_main_tile(building_x, building_y, row, col):
                                scaled_grass = pygame.transform.scale(self.ground_sprite,(int(self.iso_tile_width * zoom_level),int(self.iso_tile_height * zoom_level)))
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                                sprite = self.barracks_sprite

                                scaled_sprite = pygame.transform.scale(
                                    sprite,
                                    (int(self.iso_tile_width * 3 * zoom_level),
                                    int(self.iso_tile_height * 3 * zoom_level))
                                )
                                
                                iso_surface.blit(
                                    scaled_sprite,
                                    (iso_x - (self.iso_tile_width * zoom_level), 
                                    iso_y - (self.iso_tile_height * 2 * zoom_level))
                                )
                            else:
                                scaled_grass = pygame.transform.scale(
                                self.ground_sprite,
                                (int(self.iso_tile_width * zoom_level),
                                int(self.iso_tile_height * zoom_level))
                            )
                        if isinstance(building, TownCenter):
                            building_x, building_y = self.get_building_top_left(building)

                            if self.is_main_tile(building_x, building_y, row, col):
                                scaled_grass = pygame.transform.scale(self.ground_sprite,(int(self.iso_tile_width * zoom_level),int(self.iso_tile_height * zoom_level)))
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                                sprite1 = self.towncenterleft_sprite
                                scaled_sprite1 = pygame.transform.scale(
                                    sprite1,
                                    (int(self.iso_tile_width *3* zoom_level),
                                    int(self.iso_tile_height *3* zoom_level))
                                )
                                
                                iso_surface.blit(
                                    scaled_sprite1,
                                    (iso_x - (self.iso_tile_width * zoom_level)+1, 
                                    iso_y - (self.iso_tile_height * 2 * zoom_level)-1)
                                )
                                '''sprite2 = self.towncentermiddle_sprite
                                scaled_sprite2 = pygame.transform.scale(
                                    sprite2,
                                    (int(self.iso_tile_width * 3 * zoom_level),
                                    int(self.iso_tile_height * 3 * zoom_level))
                                )
                                
                                iso_surface.blit(
                                    scaled_sprite2,
                                    (iso_x - (self.iso_tile_width * zoom_level), 
                                    iso_y - (self.iso_tile_height * 2 * zoom_level))
                                )
                                sprite3 = self.towncenterright_sprite
                                scaled_sprite3 = pygame.transform.scale(
                                    sprite3,
                                    (int(self.iso_tile_width * 3 * zoom_level),
                                    int(self.iso_tile_height * 3 * zoom_level))
                                )
                                
                                iso_surface.blit(
                                    scaled_sprite3,
                                    (iso_x - (self.iso_tile_width * zoom_level)+1, 
                                    iso_y - (self.iso_tile_height * 2 * zoom_level)-1)
                                )'''
                            else:
                                scaled_grass = pygame.transform.scale(
                                self.ground_sprite,
                                (int(self.iso_tile_width * zoom_level),
                                int(self.iso_tile_height * zoom_level))
                            )

        max_scroll_x = map_surface_width - screen.get_width() + (self.iso_tile_width * zoom_level)
        max_scroll_y = map_surface_height - screen.get_height() + (self.iso_tile_height * zoom_level)

        view_x = max(0, min(pos_x * self.iso_tile_width * zoom_level, max_scroll_x))
        view_y = max(0, min(pos_y * self.iso_tile_height * zoom_level, max_scroll_y))

        screen.blit(iso_surface, (0, 0), 
                    (view_x, view_y, 
                    screen.get_width(), 
                    screen.get_height()))
        
        self.draw_minimap(screen, view_x, view_y, zoom_level)    
        self.display_fps(screen)
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
            return 0
        elif content == 'B':
            return 0
        else:
            return self.GRAY

    def display_fps(self, screen):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, True, self.WHITE)
        screen.blit(fps_text, (10, 10))
        self.clock.tick(60)

    def scale_sprite(self, sprite):
        """Scale a sprite based on current window size"""
        current_size = sprite.get_size()
        new_width = int(current_size[0] * self.scale_factor)
        new_height = int(current_size[1] * self.scale_factor)
        return pygame.transform.scale(sprite, (new_width, new_height))


    def load_barracks_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        barracks_path = os.path.join(project_root, "Sprite_aoe", "buildings","barracks.bmp")
        sprite = pygame.image.load(barracks_path).convert()
        sprite.set_colorkey((255, 0, 255))
        return self.scale_sprite(sprite)


        

    def is_main_tile(self, building_x, building_y, row, col):
        # Vérifiez si cette position (row, col) correspond à la tuile centrale d'un bâtiment
        if building_x +1 == col and building_y +2 == row:
            return True
        return False

    def get_building_top_left(self, building):
        # Trouver les coordonnées (x, y) du coin supérieur gauche du bâtiment
        for row in range(len(self.mapBuildings)):
            for col in range(len(self.mapBuildings[row])):
                if self.mapBuildings[row][col] == building:
                    return col, row
        return None, None  # Si non trouvé

    