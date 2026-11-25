import pygame
import os
from dir import RSC_DIR

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}    

    def load_image(self, filename):
        path = os.path.join(RSC_DIR, filename)

        if path not in self.images:
            self.images[path] = pygame.image.load(path).convert_alpha()

        return self.images[path]

    def unload_imge(self, filename):
        pass

    def load_sound(self, filename):
        path = os.path.join(RSC_DIR, filename)

        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)

        return self.sounds[path]

    def get_path(self, filename):
        return os.path.join(RSC_DIR, filename)