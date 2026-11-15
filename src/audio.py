
import pygame
from assets import AssetManager


class Audio:
    def __init__(self, assets: AssetManager):
        self.assets = assets

    def play_sound(self, filename):
        sound = self.assets.load_sound(filename)
        sound.play()

    def stop_sound(self, filename):
        sound = self.assets.load_sound(filename)
        sound.stop()

    def set_volume(self, filename, volume):
        sound = self.assets.load_sound(filename)
        sound.set_volume(volume)

    def set_master_volume(self, volume):
        for sound in self.assets.sounds.values():
            sound.set_volume(volume)

class Music:
    def __init__(self, assets: AssetManager):
        self.assets = assets

    def play_music(self, filename, loops=-1):
        path = self.assets.get_path(filename)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)