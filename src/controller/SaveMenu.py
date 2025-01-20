import pygame
import os
import sys


class SaveMenu:
    def __init__(self, uihandler):
        self.uihandler = uihandler

    def display(self, screen, font):
        # Charger l'image de fond
        background = pygame.image.load(f"../data/img/menu_background.png")
        button_image = pygame.image.load(f"../data/img/button.png")

        buttons = [
            ("Charger", self.uihandler.show_load_game_menu),
            ("Sauvegarder", lambda *_: self.uihandler.saveGame()),
            ("Supprimer", self.delete_save),
            ("Retour", None)  # Retour au menu principal
        ]
        
        menu_active = True
        while menu_active:
            # Ajuster et afficher l'image de fond
            screen.blit(pygame.transform.scale(background, screen.get_size()), (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            screen_width, screen_height = screen.get_size()

            # Dessiner les boutons avec effets visuels
            for i, (text, action) in enumerate(buttons):
                button_width, button_height = 300, 50
                x = (screen_width - button_width) // 2
                y = (screen_height - (len(buttons) * (button_height + 20))) // 2 + i * (button_height + 20)
                button_rect = pygame.Rect(x, y, button_width, button_height)

                # Effet visuel au survol
                is_hovered = button_rect.collidepoint(mouse_pos)
                button_color = (200, 200, 100) if is_hovered else (160, 82, 45)

                # Dessiner le bouton
                pygame.draw.rect(screen, button_color, button_rect)
                screen.blit(pygame.transform.scale(button_image, button_rect.size), button_rect.topleft)

                # Ajouter le texte centré sur le bouton
                label = font.render(text, True, (255, 255, 255))
                label_rect = label.get_rect(center=button_rect.center)
                screen.blit(label, label_rect)

            # Rafraîchir l'écran
            pygame.display.flip()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                    for i, (text, action) in enumerate(buttons):
                        button_width, button_height = 300, 50
                        x = (screen_width - button_width) // 2
                        y = (screen_height - (len(buttons) * (button_height + 20))) // 2 + i * (button_height + 20)
                        button_rect = pygame.Rect(x, y, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            if text == "Retour":
                                menu_active = False  # Sortir de cette boucle
                                self.uihandler.show_menu()  # Retourner au menu principal
                            elif action:
                                action(screen, font)

    def delete_save(self, screen, font):
        files = os.listdir('../save/')
        clock = pygame.time.Clock()
        delete_active = True
        while delete_active:
            screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            y = 100

            for file in files:
                label = font.render(file, True, (255, 255, 255))
                rect = label.get_rect(topleft=(100, y))
                color = (200, 200, 0) if rect.collidepoint(mouse_pos) else (255, 255, 255)
                label = font.render(file, True, color)
                screen.blit(label, rect.topleft)
                y += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    delete_active = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    y = 100
                    for file in files:
                        rect = pygame.Rect(100, y, 400, 30)
                        if rect.collidepoint(mouse_pos):
                            os.remove(f"../save/{file}")
                            files.remove(file)
                            break
                        y += 40

            clock.tick(60)
