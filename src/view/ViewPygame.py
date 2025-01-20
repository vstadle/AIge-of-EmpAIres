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
        
    
    def __init__(self, grid_length_x, grid_length_y, game_map, clock, game):
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
        self.width = 1550
        self.height = 865
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.camera = Camera(self.width, self.height, self.grid_length_x, self.grid_length_y)
        self.fps_font = pygame.font.SysFont(None, 25)
        # Créer la surface de fond une seule fois
        iso_height = (grid_length_x + grid_length_y) * self.TILE_SIZE / 2
        self.grass_tiles = pygame.Surface(
            (grid_length_x * self.TILE_SIZE * 4, iso_height + 2*self.TILE_SIZE) # Ajout de TILE_SIZE pour le bas
        ).convert_alpha()
        
        # Charger et mettre en cache tous les sprites au démarrage
        self.tiles = self._load_images()
        self.cached_sprites = self._precache_all_sprites()
        
        # Initialiser la minimap
        minimap_size = min(self.width, self.height) // 5
        self.minimap_base = pygame.Surface((minimap_size * 2, minimap_size), pygame.SRCALPHA).convert_alpha()
        self.create_static_minimap()
        #Initialiser les FPS
        self.fps_update_frequency = 500  # Mise à jour toutes les 500ms
        self.last_fps_update = pygame.time.get_ticks()
        self.current_fps_display = "FPS: 0"
        self.fps_samples = []
        self.max_samples = 10  # Nombre d'échantillons
        # Créer le monde une seule fois
        self.world = self._create_world()
        self.initialize_player_panel()
        
        # Cache pour les positions de rendu (optimisation)
        self._render_positions_cache = {}

        # Pré-rendre le texte des FPS
        self.fps_surface = self.fps_font.render(
                self.current_fps_display,
                True,
                (255, 255, 255)
            )
    
    def _load_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        SPRITE_PATHS = {
            "block": os.path.join(project_root, "Sprite_aoe/miscellaneous/block.png"),
            "tree": os.path.join(project_root, "Sprite_aoe/miscellaneous/tree1.png"),
            "rock": os.path.join(project_root, "Sprite_aoe/miscellaneous/rock.png"),
            "towncenter": os.path.join(project_root, "Sprite_aoe/buildings/town_center.webp"),
            "barracks": os.path.join(project_root, "Sprite_aoe/buildings/barracks.png"),
            "gold": os.path.join(project_root, "Sprite_aoe/gold/GoldMine002.png"),
            "archeryrange": os.path.join(project_root, "Sprite_aoe/buildings/archery_range.png"),
            "stable": os.path.join(project_root, "Sprite_aoe/buildings/Stable.png"),
            "farm": os.path.join(project_root, "Sprite_aoe/buildings/farm1.png"),
            "villager": os.path.join(project_root, "Sprite_aoe/villager/standard_male/StandGround/Villagerstand001.png"),
            "house": os.path.join(project_root,"Sprite_aoe/buildings/house.png"),
            "camp": os.path.join(project_root, "Sprite_aoe/buildings/lumber_camp.png"),
            "keep": os.path.join(project_root, "Sprite_aoe/buildings/keep.png"),
            "horseman": os.path.join(project_root, "Sprite_aoe/villager/Horsearcherstand011.png"),
            "archer": os.path.join(project_root, "Sprite_aoe/villager/Archerstand001.png")
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
                (5 * self.TILE_SIZE, 4.22 * self.TILE_SIZE)
            ),
            'stable': pygame.transform.scale(
            self.tiles["stable"], 
            (5 * self.TILE_SIZE, 5 * self.TILE_SIZE)
            ),
            'farm': pygame.transform.scale(
                self.tiles["farm"],
                (5 * self.TILE_SIZE, 3 * self.TILE_SIZE)
            ),
            'villager': pygame.transform.scale(
                self.tiles["villager"],
                (self.TILE_SIZE, self.TILE_SIZE) 
            ),
            'house': pygame.transform.scale(
                self.tiles["house"],
                (2.96*self.TILE_SIZE, 2.5*self.TILE_SIZE)
            ),
            'camp': pygame.transform.scale(
                self.tiles["camp"],
                (2.96*self.TILE_SIZE, 2.5*self.TILE_SIZE)
            ),
            'keep': pygame.transform.scale(
                self.tiles["keep"],
                (2.96*self.TILE_SIZE, 2.5*self.TILE_SIZE)
            ),
            'horseman':pygame.transform.scale(
                self.tiles["horseman"],
                (1.88*self.TILE_SIZE, 1.8*self.TILE_SIZE) 
            ),
            'archer':pygame.transform.scale(
                self.tiles["archer"],
                (self.TILE_SIZE, self.TILE_SIZE) 
            ),
        }

    def _create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                
                # Dessiner l'herbe de base, pas besoin de TILE_SIZE vu qu'il est pris en compte dans la taille de la surface
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
        tree_positions = [] #liste pour regrouper les positions des arbres
        # Optimisation : pré-charger les maps
        game_map = self.map.getMap()
        buildings_map = self.map.get_map_buildings()
        
        # Optimisation : stocker la largeur de la grass_tiles
        grass_width_half = self.grass_tiles.get_width()/2
        camera_scroll_x = self.camera.scroll.x
        camera_scroll_y = self.camera.scroll.y
        tree = self.tiles["tree"]
        tree_height = tree.get_height()
    
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                screen_x = render_pos[0] + grass_width_half + self.camera.scroll.x
                screen_y = render_pos[1] + self.camera.scroll.y
                
                # Vérification de la visibilité avec marges pour la vue isométrique
                if (-margin_x <= screen_x <= self.width + margin_x and 
                    -margin_y <= screen_y <= self.height + margin_y):
                    
                    cell_content = game_map[x][y]
                    building = buildings_map[x][y]
                    
                    # Ajouter les éléments visibles à la liste de rendu
                    if cell_content == 'W':
                        tree = self.tiles["tree"]
                        tree_positions.append((
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
                    elif cell_content == 'h':
                        render_list.append((
                            screen_y + self.TILE_SIZE,
                            (self.cached_sprites['horseman'],
                            (screen_x - self.TILE_SIZE//2 + 0.5  * self.TILE_SIZE, 
                            screen_y - self.TILE_SIZE//2 - self.TILE_SIZE))
                        ))
                    elif cell_content == 'a':
                        render_list.append((
                            screen_y + self.TILE_SIZE,
                            (self.cached_sprites['archer'],
                            (screen_x - self.TILE_SIZE//2 + 0.5  * self.TILE_SIZE, 
                            screen_y - self.TILE_SIZE//2 - self.TILE_SIZE))
                        ))
                    
                    # Gestion des bâtiments
                    if building:
                        self._add_building_to_render_list(
                            building, x, y, screen_x, screen_y, render_list
                        )
        tree_positions.sort(key=lambda x: x[0])
    
        
        # Dessiner tous les arbres en une seule opération
        if tree_positions:
            for _, (tree, pos) in sorted(tree_positions, key=lambda x: x[0]):
                self.screen.blit(tree, pos)
        # Trier et dessiner les éléments
        if render_list:
            for _, (sprite, pos) in sorted(render_list, key=lambda x: x[0]):
                self.screen.blit(sprite, pos)
        
        
        self.draw_minimap()
        self.draw_player_info()
        self._update_fps_display()
        self.screen.blit(self.fps_surface, (10, 10))


    def _update_fps_display(self):
        current_time = pygame.time.get_ticks()
        
        # Ajouter le FPS actuel aux échantillons
        current_fps = self.clock.get_fps()
        self.fps_samples.append(current_fps)
        
        # Garder seulement les N derniers échantillons
        if len(self.fps_samples) > self.max_samples:
            self.fps_samples.pop(0)
        
        # Mettre à jour l'affichage toutes les 500ms
        if current_time - self.last_fps_update >= self.fps_update_frequency:
            # Calculer la moyenne des FPS
            avg_fps = sum(self.fps_samples) / len(self.fps_samples)
            self.current_fps_display = f"FPS: {int(avg_fps)}"
            self.last_fps_update = current_time
            
            # Pré-rendre le texte des FPS
            self.fps_surface = self.fps_font.render(
                self.current_fps_display,
                True,
                (255, 255, 255)
            )
    def _add_building_to_render_list(self, building, x, y, screen_x, screen_y, render_list):
        #Méthode auxiliaire pour ajouter les bâtiments à la liste de rendu
        
        if isinstance(building, TownCenter):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], TownCenter)) and \
               (x == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], TownCenter)):
                sprite_x = screen_x - self.cached_sprites['towncenter'].get_width()//2 + 1.5*self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['towncenter'].get_height() + 2.7 * self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 4,
                    (self.cached_sprites['towncenter'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Barracks):
            if (x == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], Barracks)) and \
               (y == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], Barracks)):
                sprite_x = screen_x - self.cached_sprites['barracks'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['barracks'].get_height()//2 +0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['barracks'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, ArcheryRange):
            if (x == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], ArcheryRange)) and \
            (y == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], ArcheryRange)):
                sprite_x = screen_x - self.cached_sprites['archeryrange'].get_width()//2 + 1.5*self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['archeryrange'].get_height()//2+0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['archeryrange'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Stable):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], Stable)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], Stable)):
                sprite_x = screen_x - self.cached_sprites['stable'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['stable'].get_height()//2 + 0.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['stable'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Farm):  # Ajout de la condition pour la ferme
            if (y == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], Farm)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], Farm)):
                sprite_x = screen_x - self.cached_sprites['farm'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['farm'].get_height()//2 + 1.5*self.TILE_SIZE
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['farm'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, House):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], House)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], House)):
                sprite_x = screen_x - self.cached_sprites['house'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['house'].get_height()//2 + self.TILE_SIZE//2
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['house'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Camp):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], Camp)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], Camp)):
                sprite_x = screen_x - self.cached_sprites['camp'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['camp'].get_height()//2 + self.TILE_SIZE//2
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['camp'], (sprite_x, sprite_y))
                ))
        elif isinstance(building, Keep):
            if (y == 0 or not isinstance(self.map.get_map_buildings()[x - 1][y], Keep)) and \
            (x == 0 or not isinstance(self.map.get_map_buildings()[x][y - 1], Keep)):
                sprite_x = screen_x - self.cached_sprites['keep'].get_width()//2 + self.TILE_SIZE
                sprite_y = screen_y - self.cached_sprites['keep'].get_height()//2 - 0.5 * self.TILE_SIZE + 10
                render_list.append((
                    screen_y + self.TILE_SIZE * 2,
                    (self.cached_sprites['keep'], (sprite_x, sprite_y))
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
        'ArcheryRange': (0, 128, 255),
        'Farm': (165,42,42),
        'House':(255,255,255),
        'Camp': (214,87,11),
        'Keep' : (255,192,203)
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
        
        # Pré-calculer toutes les posit ions et tailles
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
                
                cell_content = self.map.getMap()[x][y]
                building = self.map.get_map_buildings()[x][y]
                
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
                    elif isinstance(building,Farm):
                        color = self.minimap_colors['Farm']
                    elif isinstance(building, House):
                        color = self.minimap_colors['House']
                    elif isinstance(building, Camp):
                        color = self.minimap_colors['Camp']
                    elif isinstance(building, Keep):
                        color = self.minimap_colors['Keep']

                    
                
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
        
        # Calcul de la taille totale du monde isométrique
        world_iso_width = (self.grid_length_x + self.grid_length_y) * self.TILE_SIZE
        world_iso_height = (self.grid_length_x + self.grid_length_y) * self.TILE_SIZE / 2
        
        # Obtenir les dimensions de la minimap
        minimap_width = self.minimap_base.get_width()
        minimap_height = self.minimap_base.get_height()
        
        # Calculer les échelles
        scale_x = minimap_width / world_iso_width
        scale_y = minimap_height / world_iso_height
        
        # Calculer le décalage initial du monde isométrique
        # La moitié de la grass_tiles est toujours visible au début
        initial_offset_x = self.grass_tiles.get_width() / 4
        
        # Calculer la position du viewport sur la minimap en tenant compte du décalage initial
        viewport_x = minimap_x + (-self.camera.scroll.x * scale_x) - (initial_offset_x * scale_x)
        viewport_y = minimap_y + (-self.camera.scroll.y * scale_y)
        
        # Calculer les dimensions du viewport
        viewport_width = self.width * scale_x
        viewport_height = self.height * scale_y
        
        # S'assurer que le viewport reste dans les limites de la minimap
        viewport_x = max(minimap_x, min(viewport_x, minimap_x + minimap_width - viewport_width))
        viewport_y = max(minimap_y, min(viewport_y, minimap_y + minimap_height - viewport_height))
        
        # Créer le rectangle de la minimap pour la détection des clics
        minimap_rect = pygame.Rect(minimap_x, minimap_y, minimap_width, minimap_height)
        
        # Afficher la minimap pré-rendue
        self.screen.blit(self.minimap_base, (minimap_x, minimap_y))
        
        # Dessiner le viewport
        viewport_rect = pygame.Rect(viewport_x, viewport_y, viewport_width, viewport_height)
        pygame.draw.rect(self.screen, (255, 255, 255), viewport_rect, 1)
        
        # Cadre de la minimap
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (minimap_x-1, minimap_y-1, 
                        minimap_width+2, 
                        minimap_height+2), 1)
        
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