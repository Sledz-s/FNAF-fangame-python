import pygame
import os
from dir import RSC_DIR
from assets import AssetManager

# ----------------------------------------

class Button:   # Do optymalizacji, sprawdzaj czy grafiki zostały już załadowane, żeby nie ładować kilka razy 1 obrazka do RAM-u
    def __init__(self, assets: AssetManager, x, y, idle, hover=None, pressed=None, id = None):
        self.id = id
        self.image_idle = assets.load_image(idle)


        self.image_hover = (
            assets.load_image(hover)
            if hover else self.image_idle
        )

        self.image_pressed = (
            assets.load_image(pressed)
            if pressed else self.image_hover
        )

        self.image = self.image_idle
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        if hovered and self.is_pressed:
            self.image = self.image_pressed
        elif hovered:
            self.image = self.image_hover
        else:
            self.image = self.image_idle

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True
            self.is_pressed = False
        return False
