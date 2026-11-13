import pygame
import random
import sys
import time
from array import array
from video import *
from audio import Audio
from assets import AssetManager

from game import Game

from dir import CAMERAS_DIR


# |-----------------------------|
# |      FryderykFramework      |
# |         prototyp 0.4        |
# |                             |
# |          Made by            |
# |           sl3DZ             |
# |                             |
# |-----------------------------|

# ----------------------------------------


if __name__ == '__main__':

    random.seed(time.time())

    pygame.init()

    video_handle = Video(title="Fryderyk Engine V0.4" , screen=pygame.display.set_mode((DEAFULT_SCREEN_W, DEAFULT_SCREEN_H)))
    audio_handle = Audio()
    clock = pygame.time.Clock()
    assets_handle = AssetManager()

    game = Game(
        video=video_handle,
        assets=assets_handle,
        audio=audio_handle
        )

    while game.running:
        deltatime = clock.tick(60) / 1000.0
        game.handle_events()
        game.update(deltatime)
        game.draw()

    # ----------------------------------------

    pygame.quit()
    sys.exit()
    # ----------------------------------------
