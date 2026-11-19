import pygame
from dir import RSC_DIR
from assets import AssetManager

from enum import Enum, auto


class ButtonState(Enum):
    IDLE = auto()
    HOVER = auto()
    PRESSED = auto()
    ACTIVE = auto()

# ----------------------------------------

class Button:
    __slots__ = ('id', 'images', 'image', 'rect', 'is_pressed')

    def __init__(self, x, y, images: list, id=None):
        self.id = id
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        if hovered and self.is_pressed:
            self.image = self.images[2]
        elif hovered:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True

            self.is_pressed = False
        return False

class ImageButton(Button):
    def __init__(self, assets: AssetManager, x, y, images, id=None):
        idle_image = assets.load_image(images[0])

        hover_image = (
            assets.load_image(images[1])
            if images[1] else idle_image
        )

        pressed_image = (
            assets.load_image(images[2])
            if images[2] else hover_image
        )

        loaded_images = (
            idle_image,
            hover_image,
            pressed_image
        )

        super().__init__(x, y, loaded_images, id)
    
class TextButton(Button):
    def __init__(self, x, y, text, font, id=None):

        images = (
            font.render(text, True, (255, 255, 255)),
            font.render(text, True, (255, 255, 0)),
            font.render(text, True, (255, 0, 0))
        )

        super().__init__(x, y, images, id)

class CamButton(Button):
    __slots__ = ('is_active',)

    def __init__(self, assets: AssetManager, x, y, images, id=None):
        idle_image = assets.load_image(images[0])

        hover_image = (
            assets.load_image(images[1])
            if images[1] else idle_image
        )

        pressed_image = (
            assets.load_image(images[2])
            if images[2] else hover_image
        )

        active_image = (
            assets.load_image(images[3])
            if images[3] else pressed_image
        )

        loaded_images = (
            idle_image,
            hover_image,
            pressed_image,
            active_image
        )

        super().__init__(x, y, loaded_images, id)

        self.is_active = False

    def update(self):
        if self.is_active:
            self.image = self.images[3]
            return

        super().update()