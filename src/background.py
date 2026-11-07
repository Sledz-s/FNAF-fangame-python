import pygame
import os
from dir import SCREENS_DIR

# ----------------------------------------


class Background:
    def __init__(self, image_path, size=None, folder=SCREENS_DIR):
        full_path = os.path.join(folder, image_path)
        self.image = pygame.image.load(full_path).convert()

        if size:
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def bg_draw(self, screen, camera):
        if self.rect.width > screen.get_width():
            screen.blit(self.image, (-camera.rect.x, -camera.rect.y))
        else:
            screen.blit(self.image, (0, 0))


class FadeTransition:
    def __init__(self, width, height, speed=5):
        self.surface = pygame.Surface((width, height))
        self.surface.fill((0, 0, 0))
        self.alpha = 0
        self.speed = speed
        self.mode = None  # "OUT" (do czarnego) lub "IN" (z czarnego)
        self.active = False

    def start(self, mode):
        self.mode = mode
        self.active = True
        self.alpha = 0 if mode == "OUT" else 255

    def update(self):
        if not self.active:
            return False

        if self.mode == "OUT":
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                self.active = False
                return True
        else:
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False
        return False

    def fade_transition(self, screen):
        if self.alpha > 0:
            self.surface.set_alpha(self.alpha)
            screen.blit(self.surface, (0, 0))