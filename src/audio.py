import pygame
from assets import AssetManager

class Audio:
    __slots__ = ('assets', 'music', 'sfx')
    def __init__(self, assets: AssetManager):
        self.assets = assets

        self.music: Music = Music(self.assets)
        self.sfx: SoundEffect = SoundEffect(self.assets)

    def set_master_volume(self, volume: float) -> None:
        for sound in self.assets.sounds.values():
            sound.set_volume(volume)

        self.music.set_volume(volume)

    def fadeout(self, time_ms: int) -> None:
         pygame.mixer.fadeout(time_ms)

class SoundEffect:
    __slots__ = ('assets', 'sfx_list', 'last_sfx')

    def __init__(self, assets: AssetManager):
        self.assets = assets
        self.sfx_list: list = []
        self.last_sfx = 0

    def play(self, id: int) -> None:
        '''Play sfx from the list'''

        self.last_sfx = id

        sound = self.assets.load_sound(self.sfx_list[id])
        sound.play()

    def stop(self, id: int) -> None:
        '''Stop sfx'''

        sound = self.assets.load_sound(self.sfx_list[id])
        sound.stop()

    def play_last_sfx(self) -> None:
        '''Play last played sfx'''

        sound = self.assets.load_sound(self.sfx_list[self.last_sfx])
        sound.play()

    def set_volume(self, id: int, volume: float) -> None:
        '''Set sfx volume'''

        sound = self.assets.load_sound(self.sfx_list[id])
        sound.set_volume(volume)

    def get_volume(self, id: int) -> float:
        '''Get sfx volume'''

        sound = self.assets.load_sound(self.sfx_list[id])
        return sound.get_volume()

class Music:
    __slots__ = ('assets', 'trakcs')
    def __init__(self, assets: AssetManager):

        self.assets = assets
        self.trakcs: list = ["audio/music/Fnaf1_Menu.mp3"]

    def play(self, id: int, loops: int =-1) -> None:
        '''Play music'''    
        pygame.mixer.music.load(self.assets.get_path(self.trakcs[id]))
        pygame.mixer.music.play(loops)

    def stop(self) -> None:
        '''Stop curr playing music'''
        pygame.mixer.music.stop()

    def pause(self) -> None:
        '''Pause curr playing music'''
        pygame.mixer.music.pause()

    def resume(self) -> None:
        '''Resume paused music'''
        pygame.mixer.music.unpause()

    def set_volume(self, volume: int) -> None:
        '''Set curr playing music volume'''
        pygame.mixer.music.set_volume(volume)

    def get_volume(self):
        pass