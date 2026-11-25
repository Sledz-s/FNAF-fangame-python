import pygame
from dir import SCREENS_DIR
from assets import AssetManager
from my_random import Random

# ----------------------------------------

DEAFULT_SCREEN_W: int = 1280
DEAFULT_SCREEN_H: int = 720

class Video:
    def __init__(self, icon = None, title: str = "Nie ma fajnej nazwy", screen = None):
        self.screen     = screen
        self.fullscreen = False
        self.icon       = icon
        self.title      = title
        
        self.set_screen()

    def set_screen(self):
        self.set_icon()
        self.set_title()

    def resize_screen(self, width: int, height: int):
       self.screen = pygame.display.set_mode((width, height))
       return self.screen

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        return pygame.display.toggle_fullscreen()

    def get_video_modes(self):
        return pygame.display.list_modes()

    def set_icon(self):
      if self.icon is None:
        print("icon is not set")
        return

      try:
        icon_to_set = pygame.image.load(self.icon)
        pygame.display.set_icon(icon_to_set)
      except pygame.error as e:
        print(f"Can't load the icon: {e}")
        return
      
    def set_title(self):
        if self.title:
            pygame.display.set_caption(self.title)

class Background:
    __slots__ = ('image', 'rect')
    def __init__(self, assets: AssetManager, image_path, size=None):

        self.image = assets.load_image(image_path)

        if size:
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def draw(self, screen, camera):
        '''
        Rysuje tło na ekranie, uwzględniając pozycję kamery. 
        Jeśli szerokość tła jest większa niż szerokość ekranu, tło przesuwa się zgodnie z ruchem kamery. 
        W przeciwnym razie tło jest rysowane w stałej pozycji (0, 0).
        '''
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

    def update(self, deltatime):
        if not self.active:
            return False

        change = self.speed * deltatime

        if self.mode == "OUT":
            self.alpha += change

            if self.alpha >= 255:
                self.alpha = 255
                self.active = False
                return True

        else:
            self.alpha -= change

            if self.alpha <= 0:
                self.alpha = 0
                self.active = False

        return False

    def fade_transition(self, screen):
        if self.alpha > 0:
            self.surface.set_alpha(self.alpha)
            screen.blit(self.surface, (0, 0))

class ScreenEffect:
    def __init__(self):
        self.active = True

    def update(self, deltatime: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass

class ScreenEffects:
    def __init__(self):
        self.effects = []

    def add_effect(self, effect: ScreenEffect):
        self.effects.append(effect)

    def update(self, deltatime):
        for effect in self.effects:
            effect.update(deltatime)

        self.effects = [
            effect for effect in self.effects
            if effect.active
        ]

    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)


class FlashEffect(ScreenEffect):
    def __init__(self, color=(255, 255, 255), duration=0.2):
        super().__init__()

        self.color = color
        self.duration = duration
        self.timer = 0.0
        self.overlay = None

    def update(self, deltatime):
        self.timer += deltatime

        if self.timer >= self.duration:
            self.active = False

    def draw(self, screen):
        if self.active:
            if self.overlay is None:
                self.overlay = pygame.Surface(screen.get_size())

            self.overlay.fill(self.color)

            alpha = 255 * (1.0 - self.timer / self.duration)
            self.overlay.set_alpha(int(alpha))

            screen.blit(self.overlay, (0, 0))

class ImageEffect(ScreenEffect):
    def __init__(self, assets: AssetManager, image, alpha=255):
        super().__init__()

        self.image = assets.load_image(image)
        self.alpha = alpha

    def draw(self, screen):
        if self.active:
            self.image.set_alpha(self.alpha)
            screen.blit(self.image, (0, 0))

class AnimatedImageEffect(ScreenEffect):
    def __init__(self, assets: AssetManager, images, frame_time=0.05, alpha=(255 // 2), random_flag: bool = False):
        super().__init__()

        self.images = [
            assets.load_image(image)
            for image in images
        ]

        self.frame = 0
        self.frame_time = frame_time
        self.timer = 0.0
        self.alpha = alpha

        self.random_flag = random_flag
        if self.random_flag:
            self.random = Random()

    def update(self, deltatime):
        if not self.active:
            return

        self.timer += deltatime

        if self.timer >= self.frame_time:
            self.timer -= self.frame_time

            self.frame += 1

            if self.frame >= len(self.images):
                self.frame = 0

    def draw(self, screen):
        if self.active:
            image = self.images[self.frame]
            if not self.random_flag:
                image.set_alpha(self.alpha)

            else:
                val = self.random.randint(0,10)
                if self.random.randint(0, 1):
                    image.set_alpha(self.alpha - val)
                else:
                    image.set_alpha(self.alpha + val)

            
            screen.blit(image, (0, 0))