<<<<<<< HEAD
import pygame

# ----------------------------------------

class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)

    def cam_move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def apply(self, target_rect):
        return target_rect.move(-self.rect.x, -self.rect.y)

    def reset(self, target_rect):
        """powraca na środek ekranu"""
        pass