import pygame 

class Camera:
    def __init__(self, width, height,grid_length_x,grid_length_y):
        self.width = width
        self.height = height
        self.scroll = pygame.Vector2(0, 0)
        self.speed = 20  # Vitesse de déplacement de la caméra
        self.min_speed = 5
        self.max_speed = 50
        self.TILE_SIZE = 64  
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Mouvement de la caméra avec Z, Q, S, D
        if keys[pygame.K_z]:
            self.scroll.y += self.speed
        if keys[pygame.K_s]:
            self.scroll.y -= self.speed
        if keys[pygame.K_q]:
            self.scroll.x += self.speed
        if keys[pygame.K_d]:
            self.scroll.x -= self.speed
        self.clamp_scroll()
    

    

    def clamp_scroll(self):
        max_scroll_x = self.grid_length_x * self.TILE_SIZE*2 - self.width
        max_scroll_y = self.grid_length_y * self.TILE_SIZE + self.TILE_SIZE+15- self.height #pour bien afficher en bas

        self.scroll.x = max(-max_scroll_x, min(self.scroll.x, 0))
        self.scroll.y = max(-max_scroll_y, min(self.scroll.y, 0))
    
    def handle_minimap_navigation(self, mouse_pos, minimap_rect, grass_tiles_size):
        # Si on clique sur la minimap
        if pygame.mouse.get_pressed()[0]:  # Bouton gauche
            if minimap_rect.collidepoint(mouse_pos):
                # Calculer la position relative dans la minimap
                rel_x = (mouse_pos[0] - minimap_rect.x) / minimap_rect.width
                rel_y = (mouse_pos[1] - minimap_rect.y) / minimap_rect.height
                
                # Convertir en position de scroll
                target_scroll_x = -(rel_x * (grass_tiles_size[0] - self.width))
                target_scroll_y = -(rel_y * (grass_tiles_size[1] - self.height))
                
                # Mettre à jour le scroll
                self.scroll.x = target_scroll_x
                self.scroll.y = target_scroll_y
                
                # S'assurer que le scroll reste dans les limites
                self.clamp_scroll()