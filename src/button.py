import pygame
import os
from dir import RSC_DIR

# ----------------------------------------

class Button:   # Do optymalizacji, sprawdzaj czy grafiki zostały już załadowane, żeby nie ładować kilka razy 1 obrazka do RAM-u
    def __init__(self, x, y, idle, hover=None, pressed=None, id = None):
        self.id = id
        self.image_idle = pygame.image.load(
            os.path.join(RSC_DIR, idle)).convert_alpha()

        self.image_hover = (
            pygame.image.load(os.path.join(RSC_DIR, hover)).convert_alpha()
            if hover else self.image_idle)

        self.image_pressed = (
            pygame.image.load(os.path.join(RSC_DIR, pressed)).convert_alpha()
            if pressed else self.image_hover)

        self.image = self.image_idle
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False

    def bttn_update(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        if hovered and self.is_pressed:
            self.image = self.image_pressed
        elif hovered:
            self.image = self.image_hover
        else:
            self.image = self.image_idle

    def bttn_draw(self, screen):
        screen.blit(self.image, self.rect)

    def bttn_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True
            self.is_pressed = False
        return False
