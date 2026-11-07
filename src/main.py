import pygame
import random
import sys
import time
from button import Button
from video import *
from camera import Camera
from animatronics import Freddy
from enum import Enum
from dir import CAMERAS_DIR

# |-----------------------------|
# |FryderykEngine - prototyp 0.4|
# |                             |
# |          Made by            |
# |           sl3DZ             |
# |                             |
# |-----------------------------|

# ----------------------------------------
# --- KONSTANTY ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STATE_TITLE = "TITLE"
STATE_GAME = "GAME"

pizzeria = [[0, 0, 0] for _ in range(3)]

# ----------------------------------------

button_rect = pygame.Rect(180, 150, 140, 60)

class StateMachine(Enum):
    STATE_TITLE = 1
    STATE_GAME = 2

class SubStateMachine(Enum):
    SUBSTATE_OFFICE = 1
    SUBSTATE_CAM = 2

# ----------------------------------------

class Game:
    def __init__(self, screen) -> None:
        # ----------------------------------------

        self.screen = screen
        self.width, self.height = screen.get_size()
        self.running = True
        self.current_cam_id = None

        # ----------------------------------------

        self._state = StateMachine.STATE_TITLE
        self._substate = None
        self._target_state = None

        # ----------------------------------------

        self._init_assets()
        self._init_ui()
        self._init_entities()

    def _init_assets(self):
        """Ładowanie grafik i czcionek"""
        self.font = pygame.font.Font(None, 36)  #preload -> optymalizacja

        #title_img = random.choice(("title_PLACEHOLDER.png", "title_2_PLACEHOLDER.png"))

        self.backgrounds = {
            StateMachine.STATE_TITLE: Background("title_PLACEHOLDER.png", (self.width, self.height)),
            StateMachine.STATE_GAME: Background("office_PLACEHOLDER.png")
            }
        
        self.cam_bg = {'CAM_1': Background("cam01_PLACEHOLDER.png", folder=CAMERAS_DIR),
                       'CAM_2': Background("cam02_PLACEHOLDER.png", folder=CAMERAS_DIR)
                       }
        self._current_cam = "CAM_1"


    def _init_ui(self):
        """Tworzenie przycisków"""
        self.start_bttn = Button(
            x=self.width-160, y=160,
            idle="start_idle_PLACEHOLDER_.png",
            hover="start_hover_PLACEHOLDER_.png",
            pressed="start_pressed_PLACEHOLDER_.png")

        self.camera_onoff_bttn = Button(
            x=self.width // 2, y=self.height - 40,
            idle="start_idle_PLACEHOLDER_.png",
            pressed="start_pressed_PLACEHOLDER_.png")

        self.cam_bttn = [   # przyciski do wyboru kamery
            Button(x=self.width-160, y=160, idle = "start_idle_PLACEHOLDER_.png", id="CAM_1"),
            Button(x=self.width-160, y=120, idle = "start_idle_PLACEHOLDER_.png", id="CAM_2")]

    def _init_entities(self):
        """Powoływanie do życia logiki gry"""
        self.camera = Camera(self.width, self.height)
        self.fade = FadeTransition(self.width, self.height, speed=10)
        self.freddy = Freddy(pizzeria, 1.0, 20)
        self.current_night = None

    def change_state(self, new_state):
        if not self.fade.active:
            self._target_state = new_state
            self.fade.start("OUT")

    def init_state_change(self):
        """Logika wykonywana przy faktycznej zmianie stanu"""
        self._state = self._target_state

        match self._state:
            case StateMachine.STATE_TITLE:
                self._substate = None
            case StateMachine.STATE_GAME:
                self.current_night = Night(1)
                self.freddy.move(0, 0)
                self._substate = SubStateMachine.SUBSTATE_OFFICE

        self.fade.start("IN")
        self._target_state = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            match self._state:
                case StateMachine.STATE_TITLE:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False
                    if self.start_bttn.bttn_handler(event):
                        self.change_state(StateMachine.STATE_GAME)

                case StateMachine.STATE_GAME:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.change_state(StateMachine.STATE_TITLE)

                    match self._substate:
                        case SubStateMachine.SUBSTATE_OFFICE:
                            if self.camera_onoff_bttn.bttn_handler(event):
                                self._substate = SubStateMachine.SUBSTATE_CAM

                        case SubStateMachine.SUBSTATE_CAM:
                            for bttn in self.cam_bttn:
                                if bttn.bttn_handler(event):
                                    self._current_cam = bttn.id
                                    self.fade.start("IN")   # zamienić na szum miedzy kamerami ale teraz tez dziala

                            if self.camera_onoff_bttn.bttn_handler(event):
                                self._substate = SubStateMachine.SUBSTATE_OFFICE


    def update(self, deltatime):
        if self.fade.update():
            self.init_state_change()

        match self._state:
            case StateMachine.STATE_TITLE:
                self.start_bttn.bttn_update()
            case StateMachine.STATE_GAME:
                self.current_night.night_update(deltatime)
                self.freddy.update(deltatime)
                self.camera_onoff_bttn.bttn_update()

                if self._substate == SubStateMachine.SUBSTATE_OFFICE:
                    self._update_camera_view(deltatime)
                if self._substate == SubStateMachine.SUBSTATE_CAM:
                    for bttn in self.cam_bttn:
                        bttn.bttn_update()

    def draw(self) -> None:
        match self._state:
            case StateMachine.STATE_TITLE:
                self.backgrounds[self._state].bg_draw(self.screen, self.camera)
                self.print_on_screen("FryderykEngine prototype 0.4", (self.width // 2, 30))
                self.start_bttn.bttn_draw(self.screen)
            case StateMachine.STATE_GAME:
                # Wyświetlanie godziny
                godzina_tekst = f"Godzina: {self.current_night.godzina if self.current_night.godzina != 0 else 12} AM"
                
                if self._substate == SubStateMachine.SUBSTATE_OFFICE:
                    self.backgrounds[self._state].bg_draw(self.screen, self.camera)

                if self._substate == SubStateMachine.SUBSTATE_CAM:
                    self.cam_bg[self._current_cam].bg_draw(self.screen, self.camera)
                    self.print_on_screen("SYSTEM KAMER - PODGLĄD", (self.width // 2, self.height // 2))
                    for bttn in self.cam_bttn:
                        bttn.bttn_draw(self.screen)

                self.camera_onoff_bttn.bttn_draw(self.screen) # zawsze na końcu by przycisk był na 1 warstwie
                self.print_on_screen(godzina_tekst, (100, 30))

        # Debug
        self.print_on_screen(f"State: {self._state.name}", (self.width - 150, 30))

        self.fade.fade_transition(self.screen)
        pygame.display.flip()

    def print_on_screen(self, text, pos, color=WHITE):
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=pos)
        self.screen.blit(surf, rect)

    def _update_camera_view(self, deltatime: float) -> None:
        """Logika przesuwania widoku biura za pomocą myszki"""
        mouse_x, _ = pygame.mouse.get_pos()
        border = 150
        speed = 800 * deltatime

        # Przesunięcie w lewo
        if mouse_x < border:
            strength = (border - mouse_x) / border
            self.camera.cam_move(-speed * strength, 0)
        # Przesunięcie w prawo
        elif mouse_x > self.width - border:
            strength = (mouse_x - (self.width - border)) / border
            self.camera.cam_move(speed * strength, 0)

        # Ograniczenie (clipping) widoku do rozmiarów tła
        # Używamy self._state (Enum), aby pobrać aktualne tło biura
        bg_rect = self.backgrounds[self._state].rect
        max_x = max(0, bg_rect.width - self.width)
        self.camera.rect.x = max(0, min(self.camera.rect.x, max_x))


class Night:  # noc, kurde
    """Zarządza logiką godzin, aktualizowania AI przeciwników"""

    def __init__(self, curr_night):
        self.curr_night = curr_night
        self.accumulator: float = 0
        self.godzina: int = 0
        self.dl_godzina = 90

    def night_update(self, deltatime: float):
        self.accumulator += deltatime
        if self.accumulator >= self.dl_godzina:
            self.godzina += 1
            self.accumulator = 0
            # do to, dodać reszte logiki
            self.hour_event()

    def hour_event(self):
        if self.godzina == 6:
            pass


if __name__ == '__main__':

    random.seed(time.time())

    pygame.init()

    video_handle = Video(title="Fryderyk Engine V0.4" , screen=pygame.display.set_mode((DEAFULT_SCREEN_W, DEAFULT_SCREEN_H)))
    
    clock = pygame.time.Clock()

    game = Game(video_handle.screen)

    while game.running:
        deltatime = clock.tick(60) / 1000.0
        game.handle_events()
        game.update(deltatime)
        game.draw()

    # ----------------------------------------

    pygame.quit()
    sys.exit()
    # ----------------------------------------
