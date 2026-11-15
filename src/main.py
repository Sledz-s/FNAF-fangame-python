import pygame
import random
import sys
import time
from video import Video, DEAFULT_SCREEN_W, DEAFULT_SCREEN_H
from audio import Audio
from assets import AssetManager

from game import Game


# |-----------------------------|
# |      FryderykFramework      |
# |         prototyp 0.5        |
# |                             |
# |          Made by            |
# |           sl3DZ             |
# |                             |
# |-----------------------------|

# ----------------------------------------

AP_TITLE: str = "Fryferyk Framework 0.5"

if __name__ == '__main__':

    random.seed(time.time())

    pygame.init()
    pygame.mixer.init()

    assets_handle = AssetManager()

    video_handle = Video(title=AP_TITLE , screen=pygame.display.set_mode((DEAFULT_SCREEN_W, DEAFULT_SCREEN_H)))
    audio_handle = Audio(assets_handle)
    clock = pygame.time.Clock()
    

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
