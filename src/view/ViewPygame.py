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
from model.Ressources import Ressources
from model.Units import Units
from model.Buildings import Buildings


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
        
        self.grass_surface = None
        self.grass_tiles_width = grid_length_x * self.TILE_SIZE * 4
        self.grass_tiles_height = (grid_length_x + grid_length_y) * self.TILE_SIZE / 2
        
        
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
        self.full_minimap_mode = False
        self.minimap_zoom = 1.0
        
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
            "archer": os.path.join(project_root, "Sprite_aoe/villager/Archerstand001.png"),
            "swordsman": os.path.join(project_root, "Sprite_aoe/villager/Longswordstand001.png"),
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
            'tree':pygame.transform.scale(self.tiles["tree"],
                (1.8*self.TILE_SIZE,2.75* self.TILE_SIZE) 
            ),
            'gold':pygame.transform.scale(self.tiles["gold"],
                (1.76*self.TILE_SIZE,1.08* self.TILE_SIZE) 
            ),
            'swordsman':pygame.transform.scale(self.tiles["swordsman"],
                (0.99*self.TILE_SIZE,1.62* self.TILE_SIZE) 
            ),

        }

    def _create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                '''
                # Dessiner l'herbe de base, pas besoin de TILE_SIZE vu qu'il est pris en compte dans la taille de la surface
                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(
                    self.tiles["block"],
                    (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1])
                )'''
        return world

    def draw_map_2_5D(self):
        # Check if full minimap mode is active
        if hasattr(self, 'full_minimap_mode') and self.full_minimap_mode:
            self.draw_full_minimap()
            return
            
            

        self.screen.fill((0, 0, 0))
        self.camera.handle_input()
        
        # Calculer la zone visible de manière plus intelligente
        camera_x = -self.camera.scroll.x
        camera_y = -self.camera.scroll.y
        
        # Convertir les coordonnées écran en coordonnées de grille
        min_grid_x, min_grid_y = self.world_to_grid(camera_x - self.width/2, camera_y - self.height/2)
        max_grid_x, max_grid_y = self.world_to_grid(camera_x + self.width/2, camera_y + self.height/2)

        # Calculer des bornes supplémentaires avec un padding plus large
        padding_x = int(self.width / self.TILE_SIZE) + 4 
        padding_y = int(self.height / self.TILE_SIZE) + 4 

        min_grid_x = max(0, min_grid_x - padding_x)
        min_grid_y = max(0, min_grid_y - padding_y)
        max_grid_x = min(self.grid_length_x, max_grid_x + padding_x)
        max_grid_y = min(self.grid_length_y, max_grid_y + padding_y)

        render_list = []
        map_entities = self.map.get_map_entities()
        
        for x in range(min_grid_x, max_grid_x):
            for y in range(min_grid_y, max_grid_y):
                render_pos = self.world[x][y]["render_pos"]
                screen_x = render_pos[0] + self.camera.scroll.x
                screen_y = render_pos[1] + self.camera.scroll.y
                
                # Vérification de la visibilité avec une marge généreuse
                if (-self.TILE_SIZE * 2 <= screen_x <= self.width + self.TILE_SIZE * 2 and
                    -self.TILE_SIZE * 2 <= screen_y <= self.height + self.TILE_SIZE * 2):
                    
                    self.screen.blit(self.tiles["block"], (screen_x, screen_y))
                    
                    entity = map_entities[x][y]
                    
                    if entity:
                        # Gestion des ressources
                        if isinstance(entity, Ressources):
                            sprite_key = 'tree' if entity.__class__.__name__ == 'Wood' else 'gold'
                            render_list.append((
                                screen_y + self.TILE_SIZE//2,
                                (self.cached_sprites[sprite_key],
                                (screen_x + 10, screen_y - (2 if sprite_key == 'tree' else 0) * self.TILE_SIZE))
                            ))
                        
                        # Gestion des unités
                        elif isinstance(entity, Units):
                            sprite_mapping = {
                                'Villager': 'villager',
                                'Swordsman': 'swordsman',
                                'Horseman': 'horseman', 
                                'Archer': 'archer'
                            }
                            sprite_key = sprite_mapping.get(entity.__class__.__name__, None)
                            
                            if sprite_key and sprite_key in self.cached_sprites:
                                render_list.append((
                                    screen_y + self.TILE_SIZE//2,
                                    (self.cached_sprites[sprite_key],
                                    (screen_x - self.TILE_SIZE//2 + self.TILE_SIZE - (10 if sprite_key == 'swordsman' else 0), 
                                    screen_y - self.TILE_SIZE//2 - (20 if sprite_key == 'swordsman' else -10))
                                )))
                        
                        # Gestion des bâtiments
                        elif isinstance(entity, (TownCenter, Barracks, ArcheryRange, Stable, 
                                                Farm, House, Camp, Keep)):
                            self._add_building_to_render_list(
                                entity, x, y, screen_x, screen_y, render_list
                            )
                        if hasattr(entity, 'health_bar') and hasattr(entity, 'health') and not isinstance(entity, Buildings):
                            # Specific offsets for different entity types
                            offsets = {
                                'Villager': (50, -30),
                                'Swordsman': (40, -45),
                                'Archer': (25, -15),
                                'Horseman': (30, -25),
                                
                            }

                            # Get class name and corresponding offset
                            class_name = entity.__class__.__name__
                            offset_x, offset_y = offsets.get(class_name, (25, -15))

                            health_bar_x = screen_x + offset_x
                            health_bar_y = screen_y + offset_y

                            # Update and draw health bar
                            entity.health_bar.update(entity.health)
                            entity.health_bar.draw(self.screen, health_bar_x, health_bar_y)

        # Rendu trié par profondeur
        for _, (sprite, pos) in sorted(render_list, key=lambda x: x[0]):
            self.screen.blit(sprite, pos)
        
        # Reste des méthodes d'affichage
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
        # Vérifie si c'est la tuile principale (en haut à gauche) du bâtiment
        is_primary_tile = (
            (y == 0 or not isinstance(self.map.get_map_entities()[x - 1][y], building.__class__)) and
            (x == 0 or not isinstance(self.map.get_map_entities()[x][y - 1], building.__class__))
        )

        if is_primary_tile:
            sprite_key = building.__class__.__name__.lower()
            
            # Ajustements spécifiques pour chaque type de bâtiment
            offset_map = {
                'towncenter': (
                    -self.cached_sprites['towncenter'].get_width()//2 + 1.5*self.TILE_SIZE, 
                    -self.cached_sprites['towncenter'].get_height() + 2.7 * self.TILE_SIZE
                ),
                'barracks': (
                    -self.cached_sprites['barracks'].get_width()//2 + self.TILE_SIZE, 
                    -self.cached_sprites['barracks'].get_height()//2 + 0.5*self.TILE_SIZE
                ),
                'archeryrange': (
                    -self.cached_sprites['archeryrange'].get_width()//2 + 1.5*self.TILE_SIZE, 
                    -self.cached_sprites['archeryrange'].get_height()//2 + 0.5*self.TILE_SIZE
                ),
                'stable': (
                    -self.cached_sprites['stable'].get_width()//2 + self.TILE_SIZE, 
                    -self.cached_sprites['stable'].get_height()//2 + 0.5*self.TILE_SIZE
                ),
                'farm': (
                    -self.cached_sprites['farm'].get_width()//2 + self.TILE_SIZE, 
                    -self.cached_sprites['farm'].get_height()//2 + 1.5*self.TILE_SIZE
                ),
                'house': (
                    -self.cached_sprites['house'].get_width()//2 + self.TILE_SIZE, 
                    -self.cached_sprites['house'].get_height()//2 + self.TILE_SIZE//2
                ),
                'camp': (
                    -self.cached_sprites['camp'].get_width()//2 + self.TILE_SIZE, 
                    -self.cached_sprites['camp'].get_height()//2 + self.TILE_SIZE//2
                ),
                'keep': (
                    -self.cached_sprites['keep'].get_width()//2 + self.TILE_SIZE, 
                    -self.cached_sprites['keep'].get_height()//2 - 0.5 * self.TILE_SIZE + 10
                )
            }

            sprite_offset_x, sprite_offset_y = offset_map.get(sprite_key, (0, 0))
            
            sprite_x = screen_x + sprite_offset_x
            sprite_y = screen_y + sprite_offset_y

            render_list.append((
                screen_y + self.TILE_SIZE * 2,
                (self.cached_sprites[sprite_key], (sprite_x, sprite_y))
            ))

            # Dessiner la barre de vie centrée sur le bâtiment
            sprite = self.cached_sprites[sprite_key]
            
            health_bar_offsets = {
                'TownCenter': (-5, -5),
                'Barracks': (-20, -15),
                'ArcheryRange': (-25, -10),
                'Stable': (-30, -15),
                'Farm': (-20, -10),
                'House': (-15, -10),
                'Camp': (-20, -10),
                'Keep': (-20, -15)
            }

            # Get the class name and corresponding offset
            class_name = building.__class__.__name__
            offset_x, offset_y = health_bar_offsets.get(class_name, (-25, -10))  # Default offset if not specified

            if hasattr(building, 'health_bar') and hasattr(building, 'health'):
                health_bar_x = sprite_x + sprite.get_width() // 2 + offset_x
                health_bar_y = sprite_y + offset_y

                building.health_bar.update(building.health)
                building.health_bar.draw(self.screen, health_bar_x, health_bar_y)
                building.health_bar.draw(self.screen, health_bar_x, health_bar_y)

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
    def world_to_grid(self, world_x, world_y):
        """Convertit les coordonnées du monde en coordonnées de grille."""
        iso_x = world_x
        iso_y = world_y

        # Conversion isométrique inverse
        cart_x = (2 * iso_y + iso_x) / 2
        cart_y = (2 * iso_y - iso_x) / 2
        
        # On prend en compte la taille des tuiles
        grid_x = int(cart_x / self.TILE_SIZE)
        grid_y = int(cart_y / self.TILE_SIZE)

        return grid_x, grid_y
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
                building = self.map.get_map_entities()[x][y]
                
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
        """Dessine la minimap avec interaction pour les cartes rectangulaires"""
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
    
        # Calculer la position du viewport sur la minimap
        viewport_x = minimap_x + (-self.camera.scroll.x * scale_x) + (minimap_width / 2)
        viewport_y = minimap_y + (-self.camera.scroll.y * scale_y)
        
        # Additional adjustment for isometric perspective
        iso_offset_x = (abs(self.grid_length_x - self.grid_length_y) * self.TILE_SIZE * scale_x) / 2
        if self.grid_length_x > self.grid_length_y:
            viewport_x -= iso_offset_x
        else:
            viewport_x += iso_offset_x
    
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
        grass_tiles_size = (
            (self.grid_length_x + self.grid_length_y) * self.TILE_SIZE, 
            (self.grid_length_x + self.grid_length_y) * self.TILE_SIZE / 2
        )
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
    def draw_full_minimap(self):
        """Render a full-screen minimap with zoom and navigation capability"""
        # Create a semi-transparent surface
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
        
        # Allow zooming of the minimap
        zoom = getattr(self, 'minimap_zoom', 1.0)
        full_screen_minimap = pygame.transform.scale(
            self.minimap_base,
            (int(self.minimap_base.get_width() * zoom), int(self.minimap_base.get_height() * zoom))
        )
        
        # Center the zoomed minimap
        offset_x = (self.width - full_screen_minimap.get_width()) // 2
        offset_y = (self.height - full_screen_minimap.get_height()) // 2
        
        # Calcul de la zone totale de la minimap
        minimap_total_width = self.minimap_base.get_width() * zoom
        minimap_total_height = self.minimap_base.get_height() * zoom
        
        # Navigation logic based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Calcul du déplacement en fonction de la position de la souris
        scroll_speed = 10  # Vitesse de déplacement
        scroll_x = 0
        scroll_y = 0

        # Détermination du déplacement horizontal
        if mouse_pos[0] < self.width * 0.2:
            scroll_x = -scroll_speed
        elif mouse_pos[0] > self.width * 0.8:
            scroll_x = scroll_speed

        # Détermination du déplacement vertical
        if mouse_pos[1] < self.height * 0.2:
            scroll_y = -scroll_speed
        elif mouse_pos[1] > self.height * 0.8:
            scroll_y = scroll_speed

        # Mise à jour de l'offset pour la navigation
        self.full_minimap_offset_x = getattr(self, 'full_minimap_offset_x', 0) + scroll_x
        self.full_minimap_offset_y = getattr(self, 'full_minimap_offset_y', 0) + scroll_y
        
        # Limites de l'offset pour ne pas sortir de la minimap (correction)
        self.full_minimap_offset_x = max(
            min(self.full_minimap_offset_x, 
            (minimap_total_width - self.width) // 2 if minimap_total_width > self.width else 0), 
            (self.width - minimap_total_width) // 2 if minimap_total_width < self.width else 
            (self.width - minimap_total_width) // 2
        )
        self.full_minimap_offset_y = max(
            min(self.full_minimap_offset_y, 
            (minimap_total_height - self.height) // 2 if minimap_total_height > self.height else 0),
            (self.height - minimap_total_height) // 2 if minimap_total_height < self.height else
            (self.height - minimap_total_height) // 2
        )
        
        offset_x -= self.full_minimap_offset_x
        offset_y -= self.full_minimap_offset_y
        
        # Blit the semi-transparent overlay
        self.screen.blit(overlay, (0, 0))
        
        # Blit the minimap on top of the overlay
        self.screen.blit(full_screen_minimap, (offset_x, offset_y))

    def toggle_full_minimap(self):
        """Toggle between normal view and full-screen minimap"""
        self.full_minimap_mode = not getattr(self, 'full_minimap_mode', False)
        self.minimap_zoom = 1.0  # Reset zoom when toggling
        