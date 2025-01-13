


'''
class ViewPygame():
    def __init__(self, map):
        self.FPS = 360
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
        self.load_tree_sprites()
        self.load_gold_sprites()
        self.load_villager_sprites()
        self.ground_sprite = self.load_grass_sprite()
        self.barracks_sprite = self.load_barracks_sprite()
        self.archeryrange_sprite = self.load_archeryrange_sprite()
        self.stable_sprite = self.load_stable_sprite()
        self.towncenterleft_sprite = self.load_towncenterleft_sprite()
        self.towncenterright_sprite = self.load_towncenterright_sprite()
        self.towncentermiddle_sprite = self.load_towncentermiddle_sprite()
        self.tree_positions = {}
        self.gold_positions = {}
        self.villager_positions = {}
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def load_grass_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        sprite_path = os.path.join(project_root, "Sprite_aoe", "miscellaneous","grass2.webp")
        
        ground_sprite = pygame.image.load(sprite_path).convert_alpha()
        
        return ground_sprite
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
        towncenterleft_path = os.path.join(project_root, "Sprite_aoe", "towncenter","Towncenterleft14.png")
        towncenterleft = pygame.image.load(towncenterleft_path).convert_alpha()
        return towncenterleft

    def load_towncenterright_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        towncenterright_path = os.path.join(project_root, "Sprite_aoe", "towncenter","Towncenterright14.png")
        towncenterright = pygame.image.load(towncenterright_path).convert_alpha()
        return towncenterright

    def load_towncentermiddle_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        towncentermiddle_path = os.path.join(project_root, "Sprite_aoe", "towncenter","Towncentermiddle14.png")
        towncentermiddle = pygame.image.load(towncentermiddle_path).convert_alpha()
        return towncentermiddle
            
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

    def load_villager_sprites(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        villager_path = os.path.join(project_root, "Sprite_aoe", "villager","standard_male","Stand Ground")
        self.villager_sprites = []
        
        for filename in os.listdir(villager_path):
            if filename.endswith(".bmp"):
                sprite_path = os.path.join(villager_path, filename)
                sprite = pygame.image.load(sprite_path).convert()
                sprite.set_colorkey((255, 0, 255))
                self.villager_sprites.append(sprite)
    '''  
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

        nbtuile_visible_x = screen.get_width() // self.iso_tile_width // zoom_level
        nbtuile_visible_y = screen.get_height() // self.iso_tile_height // zoom_level



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

                if (iso_x - self.iso_tile_width*pos_x > screen.get_width()) or (iso_y - self.iso_tile_height*pos_y > screen.get_height() or iso_x - self.iso_tile_width*pos_x < -self.iso_tile_width*zoom_level) or (iso_y - self.iso_tile_height*pos_y < -self.iso_tile_height*zoom_level):
                    continue


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
                            (int(self.iso_tile_width *1.25* zoom_level),
                            int(self.iso_tile_height *1.82* zoom_level))
                        )
                        iso_surface.blit(scaled_tree_sprite, 
                        (iso_x - self.iso_tile_width // 2 * zoom_level,
                         iso_y - (self.iso_tile_height * 2 * zoom_level)))
                        iso_surface.blit(scaled_tree_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level,iso_y - (self.iso_tile_height // 2 * zoom_level)))
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
                    elif cell_content == 'v':
                        scaled_sprite = pygame.transform.scale(
                            self.ground_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height * zoom_level))
                        )
                        iso_surface.blit(scaled_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                        
                        if (row, col) not in self.villager_positions:
                            self.villager_positions[(row, col)] = random.choice(self.villager_sprites)

                        villager_sprite = self.villager_positions[(row, col)]
                        scaled_villager_sprite = pygame.transform.scale(
                            villager_sprite,
                            (int(self.iso_tile_width * zoom_level),
                            int(self.iso_tile_height *2* zoom_level))
                        )
                        iso_surface.blit(scaled_villager_sprite, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
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
                                    int(self.iso_tile_height * 6 * zoom_level))
                                )
                                
                                iso_surface.blit(
                                    scaled_sprite,
                                    (iso_x - (self.iso_tile_width *1.5* zoom_level), 
                                    iso_y - (self.iso_tile_height * 5 * zoom_level))
                                )
                            else:
                                scaled_grass = pygame.transform.scale(
                                self.ground_sprite,
                                (int(self.iso_tile_width * zoom_level),
                                int(self.iso_tile_height * zoom_level))
                            )
                        
                        if isinstance(building, ArcheryRange):
                            building_x, building_y = self.get_building_top_left(building)

                            if self.is_main_tile(building_x, building_y, row, col):
                                scaled_grass = pygame.transform.scale(self.ground_sprite,(int(self.iso_tile_width * zoom_level),int(self.iso_tile_height * zoom_level)))
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                                sprite = self.archeryrange_sprite

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
                                int(self.iso_tile_height * zoom_level)))
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                        if isinstance(building,Stable):
                            building_x, building_y = self.get_building_top_left(building)

                            if self.is_main_tile(building_x, building_y, row, col):
                                scaled_grass = pygame.transform.scale(self.ground_sprite,(int(self.iso_tile_width * zoom_level),int(self.iso_tile_height * zoom_level)))
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                                sprite = self.stable_sprite

                                scaled_sprite = pygame.transform.scale(
                                    sprite,
                                    (int(self.iso_tile_width * 2.5 * zoom_level),
                                    int(self.iso_tile_height * 2.5 * zoom_level))
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
                                int(self.iso_tile_height * zoom_level)))
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                        if isinstance(building, TownCenter):
                            building_x, building_y = self.get_building_top_left(building)
                            if self.is_main_tile(building_x, building_y, row, col):
                                scaled_grass = pygame.transform.smoothscale(
                                    self.ground_sprite,
                                    (int(self.iso_tile_width * zoom_level),
                                    int(self.iso_tile_height * zoom_level))
                                )
                                iso_surface.blit(scaled_grass, (iso_x - self.iso_tile_width // 2 * zoom_level, iso_y))
                                
                                # Partie gauche
                                original_width, original_height = self.towncenterleft_sprite.get_size()
                                aspect_ratio = original_width / original_height
                                sprite_height = int(self.iso_tile_height * 3 * zoom_level)
                                sprite_width = int(sprite_height * aspect_ratio)
                                
                                scaled_sprite_left = pygame.transform.smoothscale(
                                    self.towncenterleft_sprite,
                                    (sprite_width, sprite_height)
                                )
                                
                                # Partie centrale
                                original_width_middle, original_height_middle = self.towncentermiddle_sprite.get_size()
                                aspect_ratio_middle = original_width_middle / original_height_middle
                                sprite_height_middle = sprite_height  # Même hauteur que la partie gauche
                                sprite_width_middle = int(sprite_height_middle * aspect_ratio_middle)
                                
                                scaled_sprite_middle = pygame.transform.smoothscale(
                                    self.towncentermiddle_sprite,
                                    (sprite_width_middle, sprite_height_middle)
                                )
                                
                                # Partie droite
                                original_width_right, original_height_right = self.towncenterright_sprite.get_size()
                                aspect_ratio_right = original_width_right / original_height_right
                                sprite_height_right = sprite_height  # Même hauteur que les autres parties
                                sprite_width_right = int(sprite_height_right * aspect_ratio_right)
                                
                                scaled_sprite_right = pygame.transform.smoothscale(
                                    self.towncenterright_sprite,
                                    (sprite_width_right, sprite_height_right)
                                )
                                
                                # Positionnement des sprites
                                base_y = iso_y - (sprite_height * 0.75)
                                
                                # Position partie gauche
                                left_x = iso_x - sprite_width
                                iso_surface.blit(scaled_sprite_left, (left_x, base_y))
                                
                                # Position partie centrale
                                middle_x = left_x + sprite_width
                                iso_surface.blit(scaled_sprite_middle, (middle_x, base_y))
                                
                                # Position partie droite
                                right_x = middle_x + sprite_width_middle
                                iso_surface.blit(scaled_sprite_right, (right_x, base_y))
                            else:
                                scaled_grass = pygame.transform.smoothscale(
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
            return 0
        elif content == 'T':
            return 0
        elif content == 'B':
            return 0
        elif content == 'v':
            return 0
        else:
            return self.GRAY

    def display_fps(self, screen):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, True, self.WHITE)
        screen.blit(fps_text, (10, 10))
        self.clock.tick(360)

    

    def load_barracks_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        barracks_path = os.path.join(project_root, "Sprite_aoe", "buildings","barracks.png")
        sprite = pygame.image.load(barracks_path).convert()
        sprite.set_colorkey((255, 0, 255))
        return sprite
    
    def load_archeryrange_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        barracks_path = os.path.join(project_root, "Sprite_aoe", "buildings","archery_range.png")
        sprite = pygame.image.load(barracks_path).convert_alpha()
        return sprite
    
    def load_stable_sprite(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        barracks_path = os.path.join(project_root, "Sprite_aoe", "buildings","stable.png")
        sprite = pygame.image.load(barracks_path).convert_alpha()
        return sprite


        

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
        return None, None  # Si non trouvé'''
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
from view.Camera import Camera


class ViewPygame:
    # Constantes de classe
        
    
    def __init__(self, grid_length_x, grid_length_y, width, height, screen, game_map, clock, game):
        pygame.init()
        self.game = game
        self.show_player_info = False
        self.panel_surface = None
        self.panel_rect = None
        self.clock = clock
        self.map = game_map
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.TILE_SIZE = 64
        self.width = width
        self.height = height
        self.screen = screen
        self.camera = Camera(self.width, self.height, self.grid_length_x, self.grid_length_y)
        
        # Créer la surface de fond une seule fois
        self.grass_tiles = pygame.Surface(
            (grid_length_x * self.TILE_SIZE * 2, (grid_length_y+2) * self.TILE_SIZE)
        ).convert_alpha()
        
        # Charger et mettre en cache tous les sprites au démarrage
        self.tiles = self._load_images()
        self.cached_sprites = self._precache_all_sprites()
        
        # Initialiser la minimap
        minimap_size = min(self.width, self.height) // 5
        self.minimap_base = pygame.Surface((minimap_size * 2, minimap_size), pygame.SRCALPHA).convert_alpha()
        self.create_static_minimap()
        
        # Créer le monde une seule fois
        self.world = self._create_world()
        self.initialize_player_panel()
        
        # Cache pour les positions de rendu (optimisation)
        self._render_positions_cache = {}
    
    def _load_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        SPRITE_PATHS = {
            "block": os.path.join(project_root, "Sprite_aoe/miscellaneous/block.png"),
            "tree": os.path.join(project_root, "Sprite_aoe/miscellaneous/tree.png"),
            "rock": os.path.join(project_root, "Sprite_aoe/miscellaneous/rock.png"),
            "towncenter": os.path.join(project_root, "Sprite_aoe/buildings/town_center.webp"),
            "barracks": os.path.join(project_root, "Sprite_aoe/buildings/barracks.png"),
            "gold": os.path.join(project_root, "Sprite_aoe/gold/GoldMine002.png"),
            "archeryrange": os.path.join(project_root, "Sprite_aoe/buildings/archery_range.png"),
            "stable": os.path.join(project_root, "Sprite_aoe/buildings/Stable.png"),
            "farm": os.path.join(project_root, "Sprite_aoe/buildings/farm.png"),
            "villager": os.path.join(project_root, "Sprite_aoe/villager/standard_male/StandGround/Villagerstand001.png")
        }
        
        return {name: pygame.image.load(path).convert_alpha() 
                for name, path in SPRITE_PATHS.items()}
    
    def _precache_all_sprites(self):
        """Pré-redimensionne tous les sprites nécessaires"""
        return {
            'towncenter': pygame.transform.scale(
                self.tiles["towncenter"], 
                (8 * self.TILE_SIZE, 4 * self.TILE_SIZE)
            ),
            'barracks': pygame.transform.scale(
                self.tiles["barracks"], 
                (int(4.5 * self.TILE_SIZE), int(4.5 * self.TILE_SIZE))
            ),
            'archeryrange':pygame.transform.scale(
                self.tiles["archeryrange"], 
                (5 * self.TILE_SIZE, 5 * self.TILE_SIZE)
            ),
            'stable': pygame.transform.scale(
            self.tiles["stable"], 
            (5 * self.TILE_SIZE, 5 * self.TILE_SIZE)
            ),
            'farm': pygame.transform.scale(
                self.tiles["farm"],
                (5 * self.TILE_SIZE, 5 * self.TILE_SIZE)
            ),
            'villager': pygame.transform.scale(
                self.tiles["villager"],
                (self.TILE_SIZE, self.TILE_SIZE)  # Taille 1x1 pour le villageois
            ),
        }

    def _create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                
                # Dessiner l'herbe de base
                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(
                    self.tiles["block"],
                    (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1])
                )
        return world

    def draw_map_2_5D(self):
        # Optimisation : stocker les références aux fonctions fréquemment utilisées
        _min = min
        _max = max
        _int = int
        
        self.screen.fill((0, 0, 0))
        self.camera.handle_input()
        
        # Dessiner le fond d'herbe
        self.screen.blit(self.grass_tiles, (self.camera.scroll.x, self.camera.scroll.y))
        
        # Calculer les marges pour la visibilité
        margin_x = self.width // 2
        margin_y = self.height // 2
        
        # Liste pour le tri en Z
        render_list = []
        
        # Optimisation : pré-charger les maps
        game_map = self.map.getMap()
        buildings_map = self.map.get_map_buildings()
        
        # Optimisation : stocker la largeur de la grass_tiles
        grass_width_half = self.grass_tiles.get_width()/2
        
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                screen_x = render_pos[0] + grass_width_half + self.camera.scroll.x
                screen_y = render_pos[1] + self.camera.scroll.y
                
                # Vérification de la visibilité avec marges pour la vue isométrique
                if (-margin_x <= screen_x <= self.width + margin_x and 
                    -margin_y <= screen_y <= self.height + margin_y):
                    
                    cell_content = game_map[y][x]
                    building = buildings_map[y][x]
                    
                    # Ajouter les éléments visibles à la liste de rendu
                    if cell_content == 'W':
                        tree = self.tiles["tree"]
                        render_list.append((
                            screen_y,
                            (tree, 
                            (screen_x, screen_y - tree.get_height() + self.TILE_SIZE - 20))
                        ))
                    elif cell_content == 'G':
                        gold = self.tiles["gold"]
                        render_list.append((
                            screen_y,
                            (gold, 
                            (screen_x, screen_y - (gold.get_height() - self.TILE_SIZE) / 2))
                        ))
                    elif cell_content == 'v':
                        render_list.append((
                            screen_y + self.TILE_SIZE,
                            (self.cached_sprites['villager'],
                            (screen_x - self.TILE_SIZE//2 + self.TILE_SIZE, 
                            screen_y - self.TILE_SIZE//2 + 10))
                        ))
                    
                    # Gestion des bâtiments
                    if building:
                        self._add_building_to_render_list(
                            building, x, y, screen_x, screen_y, render_list
                        )
        
        # Trier et dessiner les éléments
        if render_list:
            for _, (sprite, pos) in sorted(render_list, key=lambda x: x[0]):
                self.screen.blit(sprite, pos)
        
        # UI elements
        if not hasattr(self, 'fps_font'):
            self.fps_font = pygame.font.SysFont(None, 25)
        
        fps_text = self.fps_font.render(
            f'FPS: {_int(self.clock.get_fps())}',
            True,
            (255, 255, 255)
        )
        self.screen.blit(fps_text, (10, 10))
        
        self.draw_minimap()
        self.draw_player_info()

    def _add_building_to_render_list(self, building, x, y, screen_x, screen_y, render_list):
        #Méthode auxiliaire pour ajouter les bâtiments à la liste de rendu
        if isinstance(building, TownCenter):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[y - 1][x], TownCenter)) and \
               (x == 0 or not isinstance(self.map.get_map_buildings()[y][x - 1], TownCenter)):
                sprite_x = screen_x - self.cached_sprites['towncenter'].get_width()//2 + 1.5*self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['towncenter'].get_height() + 2.7 * self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 4,
                    (self.cached_sprites['towncenter'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Barracks):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[y - 1][x], Barracks)) and \
               (x == 0 or not isinstance(self.map.get_map_buildings()[y][x - 1], Barracks)):
                sprite_x = screen_x - self.cached_sprites['barracks'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['barracks'].get_height()//2 +0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['barracks'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, ArcheryRange):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[y - 1][x], ArcheryRange)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[y][x - 1], ArcheryRange)):  # Corrigé la vérification
                sprite_x = screen_x - self.cached_sprites['archeryrange'].get_width()//2 + 1.5*self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['archeryrange'].get_height()//2+0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['archeryrange'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Stable):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[y - 1][x], Stable)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[y][x - 1], Stable)):
                sprite_x = screen_x - self.cached_sprites['stable'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['stable'].get_height()//2 + 0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['stable'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Farm):  # Ajout de la condition pour la ferme
            if (y == 0 or not isinstance(self.map.get_map_buildings()[y - 1][x], Farm)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[y][x - 1], Farm)):
                sprite_x = screen_x - self.cached_sprites['farm'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['farm'].get_height()//2 + 0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['farm'], (sprite_x, sprite_y))
                ))


    def grid_to_world(self, grid_x, grid_y):
        # Calculer les coordonnées cartésiennes de la tuile
        rect = [
            (grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE),
            (grid_x * self.TILE_SIZE + self.TILE_SIZE, grid_y * self.TILE_SIZE),
            (grid_x * self.TILE_SIZE + self.TILE_SIZE, grid_y * self.TILE_SIZE + self.TILE_SIZE),
            (grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE + self.TILE_SIZE)
        ]

        # Conversion en coordonnées isométriques
        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        
        # Calculer la position minimale des coordonnées isométriques pour centrer la tuile
        minx = min([x for x, y in iso_poly]) -1
        miny = min([y for x, y in iso_poly]) -1

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny]  # Position rendue en isométrique pour le rendu visuel
        }

        return out


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    

    

    def draw_text(self,screen, text, size, colour, pos):

        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(topleft=pos)

        screen.blit(text_surface, text_rect)
    def create_static_minimap(self):
        """Crée la partie statique de la minimap une seule fois"""
        minimap_size = self.minimap_base.get_height()
        self.minimap_colors = {
        'W': (9, 82, 40),
        'G': (255, 215, 0),
        'default': (0, 128, 0),
        'TownCenter': (0, 0, 255),
        'Barracks': (255, 0, 0),
        'Stable': (128, 128, 128),
        'ArcheryRange': (0, 128, 255)
        }
        # Fond noir semi-transparent
        pygame.draw.rect(self.minimap_base, (0, 0, 0, 128), (0, 0, self.minimap_base.get_width(), minimap_size))
        
        # Calculer l'échelle
        max_iso_width = (self.grid_length_x + self.grid_length_y) * self.TILE_SIZE
        max_iso_height = (self.grid_length_x + self.grid_length_y) * self.TILE_SIZE / 2
        scale = min(minimap_size * 2 / max_iso_width, minimap_size * 1.2 / max_iso_height)
        
        center_x = self.minimap_base.get_width() // 2
        center_y = self.minimap_base.get_height() // 2
        
        offset_x = -(self.grid_length_x * self.TILE_SIZE * scale) / 2
        offset_y = -(self.grid_length_y * self.TILE_SIZE * scale) / 2
        
        # Pré-calculer toutes les positions et tailles
        point_width = int(self.TILE_SIZE * scale)
        point_height = int(self.TILE_SIZE * scale / 2)
        
        # Dessiner la carte statique
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                cart_x = x * self.TILE_SIZE * scale + offset_x
                cart_y = y * self.TILE_SIZE * scale + offset_y
                
                iso_x = (cart_x - cart_y)
                iso_y = (cart_x + cart_y) / 2
                
                screen_x = center_x + iso_x
                screen_y = center_y + iso_y
                
                cell_content = self.map.getMap()[y][x]
                building = self.map.get_map_buildings()[y][x]
                
                color = (0, 128, 0)  # Couleur par défaut
                if cell_content == 'W':
                    color = self.minimap_colors['W']
                elif cell_content == 'G':
                    color = self.minimap_colors['G']
                elif building is not None:
                    if isinstance(building, TownCenter):
                        color = self.minimap_colors['TownCenter']
                    elif isinstance(building, Barracks):
                        color = self.minimap_colors['Barracks']
                    elif isinstance(building,Stable):
                        color = self.minimap_colors['Stable']
                    elif isinstance(building,ArcheryRange):
                        color = self.minimap_colors['ArcheryRange']
                    
                
                points = [
                    (screen_x, screen_y),
                    (screen_x + point_width//2, screen_y + point_height//2),
                    (screen_x, screen_y + point_height),
                    (screen_x - point_width//2, screen_y + point_height//2)
                ]
                pygame.draw.polygon(self.minimap_base, color, points, 3)

    def draw_minimap(self):
        """Dessine la minimap avec interaction"""
        minimap_x = self.width - self.minimap_base.get_width() - 10
        minimap_y = 10
        
        # Calculer la position du viewport
        viewport_scale_x = self.minimap_base.get_width() / self.grass_tiles.get_width()
        viewport_scale_y = self.minimap_base.get_height() / self.grass_tiles.get_height()
        
        viewport_x = minimap_x + (-self.camera.scroll.x * viewport_scale_x)
        viewport_y = minimap_y + (-self.camera.scroll.y * viewport_scale_y)
        viewport_width = self.width * viewport_scale_x
        viewport_height = self.height * viewport_scale_y
        
        # Créer le rectangle de la minimap pour la détection des clics
        minimap_rect = pygame.Rect(minimap_x, minimap_y, 
                                 self.minimap_base.get_width(), 
                                 self.minimap_base.get_height())
        
        # Afficher la minimap pré-rendue
        self.screen.blit(self.minimap_base, (minimap_x, minimap_y))
        
        # Dessiner le viewport
        viewport_rect = pygame.Rect(viewport_x, viewport_y, viewport_width, viewport_height)
        pygame.draw.rect(self.screen, (255, 255, 255), viewport_rect, 1)
        
        # Cadre de la minimap
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (minimap_x-1, minimap_y-1, 
                         self.minimap_base.get_width()+2, 
                         self.minimap_base.get_height()+2), 1)
        
        # Gérer la navigation via la minimap
        mouse_pos = pygame.mouse.get_pos()
        grass_tiles_size = (self.grass_tiles.get_width(), self.grass_tiles.get_height())
        self.camera.handle_minimap_navigation(mouse_pos, minimap_rect, grass_tiles_size)
    

    def initialize_player_panel(self):
        minimap_size = min(self.width, self.height) // 5
        panel_width = minimap_size * 2
        
        player_count = len(self.game.lstPlayer)
        panel_height = 40 + (player_count * 55)
        
        self.panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        for y in range(panel_height):
            alpha = 180
            blue_value = int(15 * (y / panel_height))
            pygame.draw.line(
                self.panel_surface,
                (0, 0, blue_value, alpha),
                (0, y),
                (panel_width, y)
            )
        
        panel_x = self.width - panel_width - 10
        panel_y = 10 + minimap_size + 10
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    def draw_player_info(self):
        if not self.show_player_info:
            return
        
        self.screen.blit(self.panel_surface, self.panel_rect)
        
        pygame.draw.rect(self.screen, (30, 30, 50), self.panel_rect, 2)
        pygame.draw.rect(self.screen, (100, 100, 150), self.panel_rect.inflate(2, 2), 1)
        
        text_x = self.panel_rect.x + 10
        text_y = self.panel_rect.y + 10
        
        self.draw_text(
            self.screen,
            "Players Information",
            24,
            (220, 220, 255),
            (self.panel_rect.centerx - 60, text_y)
        )
        
        pygame.draw.line(
            self.screen,
            (100, 100, 150),
            (self.panel_rect.x + 10, text_y + 25),
            (self.panel_rect.right - 10, text_y + 25),
            1
        )
        
        text_y += 35
        
        for player in self.game.lstPlayer:
            player_bg_rect = pygame.Rect(text_x, text_y, self.panel_rect.width - 20, 45)
            player_color = player.getColor()
            
            r = (player_color >> 16) & 255
            g = (player_color >> 8) & 255
            b = player_color & 255
            bg_color = (r, g, b, 30)
            
            pygame.draw.rect(self.screen, bg_color, player_bg_rect, 0, 3)
            
            # Nom du joueur
            self.draw_text(
                self.screen,
                player.name,
                20,
                player_color,
                (text_x + 5, text_y + 20)
            )
            
            # Ressources avec texte simple
            resources_text = f"Wood: {player.wood}  Gold: {player.gold}  Food: {player.food}"
            self.draw_text(
                self.screen,
                resources_text,
                16,
                (200, 200, 200),
                (text_x + 5, text_y + 20)
            )
            
            # Unités
            units_text = f"Units: {player.countUnits()}"
            units_text_rect = self.draw_text(
                self.screen,
                units_text,
                16,
                (200, 200, 200),
                (text_x + self.panel_rect.width - 80, text_y + 20)  # Décalage ajusté pour éviter les dépassements
            )
            text_y += 55