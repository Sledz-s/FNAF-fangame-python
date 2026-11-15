import pygame

from assets import AssetManager
from camera import Camera
from animatronics import Freddy
from enum import Enum, IntEnum
from button import Button
from video import *
from dir import CAMERAS_DIR
from my_random import Random

# ----------------------------------------
# --- KONSTANTY ---

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

STATE_TITLE = "TITLE"
STATE_GAME = "GAME"

pizzeria = [[0, 0, 0] for _ in range(3)]

# ----------------------------------------

class StateMachine(Enum):
    STATE_START_TEXT = 1
    STATE_TITLE = 2
    STATE_GAME = 3
    STATE_NIGHT_END = 4
    STATE_GAME_OVER = 5


class SubStateMachine(Enum):
    SUBSTATE_OFFICE = 1
    SUBSTATE_CAM = 2

class AnimatronicID(IntEnum):
    FREDDY = 0
    BONNIE = 1
    CHICA = 2
    FOXY = 3
    PUPPET = 4
    GOLDEN_FREDDY = 5

class Game:
    def __init__(self, video: Video, assets: AssetManager, audio) -> None:
        # ----------------------------------------
        # Podstawowe ustawienia

        self.video = video
        self.screen = self.video.screen

        self.width, self.height = self.screen.get_size()
        self.running = True
        self.current_cam_id = None

        self.assets = assets

        self.video.toggle_fullscreen()

        # ----------------------------------------
        # Generator liczb losowych (C)

        self.rng = Random()

        # ----------------------------------------
        # Maszyna stanów

        self._state = StateMachine.STATE_START_TEXT
        self._substate = None
        self._target_state = None

        # ----------------------------------------
        # Inicjalizacja

        self._init_assets()
        self._init_ui()
        self._init_entities()

        self.wait_time = 0.0

    def _init_assets(self):
        """Ładowanie grafik i czcionek"""

        self.font = pygame.font.Font(None, 36)

        self.backgrounds = {
            StateMachine.STATE_START_TEXT: Background(
                self.assets, "screens/FryderykFramework.png"
            ),
            StateMachine.STATE_TITLE: Background(
                self.assets, "screens/title_PLACEHOLDER.png",
                (self.width, self.height)
            ),
            StateMachine.STATE_GAME: Background(
                self.assets, "screens/office_PLACEHOLDER.png"
            )
        }

        self.cam_bg = {
            'CAM_1': Background(self.assets, "cam/cam01_PLACEHOLDER.png"),
            'CAM_2': Background(self.assets, "cam/cam02_PLACEHOLDER.png")
        }

        self._current_cam = "CAM_1"

    def _init_ui(self):
        """Tworzenie przycisków"""

        self.start_bttn = Button(
            assets=self.assets,
            x=self.width - 160,
            y=160,
            idle="start_idle_PLACEHOLDER_.png",
            hover="start_hover_PLACEHOLDER_.png",
            pressed="start_pressed_PLACEHOLDER_.png"
        )

        self.camera_onoff_bttn = Button(
            assets=self.assets,
            x=self.width // 2,
            y=self.height - 40,
            idle="start_idle_PLACEHOLDER_.png",
            pressed="start_pressed_PLACEHOLDER_.png"
        )

        self.cam_bttn = [
            Button(
                assets=self.assets,
                x=self.width - 160,
                y=160,
                idle="start_idle_PLACEHOLDER_.png",
                id="CAM_1"
            ),
            Button(
                assets=self.assets,
                x=self.width - 160,
                y=120,
                idle="start_idle_PLACEHOLDER_.png",
                id="CAM_2"
            )
        ]

    def _init_entities(self):
        """Powoływanie do życia logiki gry"""

        self.camera = Camera(self.width, self.height)
        self.fade = FadeTransition(self.width, self.height, speed=10)

        # Przekazujemy generator do AI Freddy'ego
        self.freddy = Freddy(pizzeria, 1.0, 20, self.rng)

        self.animatronics = [
        self.freddy
        ]

        self.current_night = None



    def change_state(self, new_state):
        if not self.fade.active:
            self._target_state = new_state
            self.fade.start("OUT")

    def init_state_change(self):
        """Logika wykonywana przy faktycznej zmianie stanu"""

        self._state = self._target_state

        match self._state:
            case StateMachine.STATE_START_TEXT:
                self._substate = None

            case StateMachine.STATE_TITLE:
                self._substate = None

            case StateMachine.STATE_GAME:
                self.current_night = Night(
                    curr_night=1,
                    game=self,
                    animatronics=self.animatronics
                )

                self.freddy.move(0, 0)
                self._substate = SubStateMachine.SUBSTATE_OFFICE

            case StateMachine.STATE_NIGHT_END:
                self._substate = None

        self.fade.start("IN")
        self._target_state = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            match self._state:
                case StateMachine.STATE_START_TEXT:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False

                case StateMachine.STATE_TITLE:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False

                    if self.start_bttn.handler(event):
                        self.change_state(StateMachine.STATE_GAME)

                case StateMachine.STATE_GAME:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.change_state(StateMachine.STATE_TITLE)

                    match self._substate:
                        case SubStateMachine.SUBSTATE_OFFICE:
                            if self.camera_onoff_bttn.handler(event):
                                self._substate = SubStateMachine.SUBSTATE_CAM

                        case SubStateMachine.SUBSTATE_CAM:
                            for bttn in self.cam_bttn:
                                if bttn.handler(event):
                                    self._current_cam = bttn.id
                                    self.fade.start("IN")

                            if self.camera_onoff_bttn.handler(event):
                                self._substate = SubStateMachine.SUBSTATE_OFFICE

    def update(self, deltatime):
        if self.fade.update():
            self.init_state_change()

        match self._state:
            case StateMachine.STATE_START_TEXT:
                self.wait_time += deltatime

                if self.wait_time >= 1.0:
                    self.wait_time = 0.0
                    self.change_state(StateMachine.STATE_TITLE)

            case StateMachine.STATE_TITLE:
                self.start_bttn.update()

            case StateMachine.STATE_GAME:
                self.current_night.night_update(deltatime)
                self.freddy.update(deltatime)
                self.camera_onoff_bttn.update()

                if self._substate == SubStateMachine.SUBSTATE_OFFICE:
                    self._update_camera_view(deltatime)

                if self._substate == SubStateMachine.SUBSTATE_CAM:
                    for bttn in self.cam_bttn:
                        bttn.update()

            case StateMachine.STATE_NIGHT_END:
                self.wait_time += deltatime

                if self.wait_time >= 1.0:
                    self.wait_time = 0.0
                    self.change_state(StateMachine.STATE_TITLE)

    def draw(self) -> None:
        match self._state:
            case StateMachine.STATE_TITLE:
                self.backgrounds[self._state].bg_draw(self.screen, self.camera)
                self.print_on_screen(
                    "Fryderyk Framework prototype 0.4",
                    (self.width // 2, 30)
                )
                self.start_bttn.draw(self.screen)

            case StateMachine.STATE_START_TEXT:
                self.backgrounds[self._state].bg_draw(self.screen, self.camera)
                self.print_on_screen(
                    "Fryderyk Framework",
                    (self.width // 2, 30)
                )

            case StateMachine.STATE_GAME:
                godzina_tekst = (
                    f"Godzina: {self.current_night.godzina if self.current_night.godzina != 0 else 12} AM"
                )

                if self._substate == SubStateMachine.SUBSTATE_OFFICE:
                    self.backgrounds[self._state].bg_draw(
                        self.screen, self.camera
                    )

                if self._substate == SubStateMachine.SUBSTATE_CAM:
                    self.cam_bg[self._current_cam].bg_draw(
                        self.screen, self.camera
                    )

                    self.print_on_screen(
                        "SYSTEM KAMER - PODGLĄD",
                        (self.width // 2, self.height // 2)
                    )

                    for bttn in self.cam_bttn:
                        bttn.draw(self.screen)

                self.camera_onoff_bttn.draw(self.screen)
                self.print_on_screen(godzina_tekst, (100, 30))

        # Debug
        self.print_on_screen(
            f"State: {self._state.name}",
            (self.width - 150, 30)
        )

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

        if mouse_x < border:
            strength = (border - mouse_x) / border
            self.camera.cam_move(-speed * strength, 0)

        elif mouse_x > self.width - border:
            strength = (mouse_x - (self.width - border)) / border
            self.camera.cam_move(speed * strength, 0)

        bg_rect = self.backgrounds[self._state].rect
        max_x = max(0, bg_rect.width - self.width)

        self.camera.rect.x = max(
            0,
            min(self.camera.rect.x, max_x)
        )


class Night:
    """Zarządza logiką godzin i aktualizowaniem AI przeciwników."""

    def __init__(self, curr_night: int, game: Game, animatronics: list) -> None:
        self.game = game

        self.animatronics = animatronics

        self.curr_night = curr_night
        self.accumulator: float = 0
        self.godzina: int = 0
        
        self.dl_godzina = 90

        self.night_events = [
            self.night_1_event,
            self.night_2_event,
            self.night_3_event,
        ]

    def night_update(self, deltatime: float):
        self.accumulator += deltatime

        while self.accumulator >= self.dl_godzina:
            self.accumulator -= self.dl_godzina
            self.godzina += 1
            self.hour_event()

    def boost_ai(self, animatronic_id: AnimatronicID, amount: int):
        self.animatronics[animatronic_id.value].zwieksz_ai(amount)

    def night_1_event(self):
        match self.godzina:
            case 1:
                pass

            case 2:
                pass

            case 3:
                self.boost_ai(AnimatronicID.FREDDY, 1)

            case 4:
                self.boost_ai(AnimatronicID.FREDDY, 2)

            case 5:
                self.boost_ai(AnimatronicID.FREDDY, 3)

            case 6:
                self.game.change_state(StateMachine.STATE_NIGHT_END)

    def night_2_event(self):
            match self.godzina:
                case 1:
                    pass
    
                case 2:
                    pass
    
                case 3:
                    self.boost_ai(AnimatronicID.FREDDY, 1)
    
                case 4:
                    self.boost_ai(AnimatronicID.FREDDY, 2)
    
                case 5:
                    self.boost_ai(AnimatronicID.FREDDY, 3)
    
                case 6:
                    self.game.change_state(StateMachine.STATE_NIGHT_END)

    def night_3_event(self):
            match self.godzina:
                case 1:
                    pass
    
                case 2:
                    pass
    
                case 3:
                    self.boost_ai(AnimatronicID.FREDDY, 1)
    
                case 4:
                    self.boost_ai(AnimatronicID.FREDDY, 2)
    
                case 5:
                    self.boost_ai(AnimatronicID.FREDDY, 3)
    
                case 6:
                    self.game.change_state(StateMachine.STATE_NIGHT_END)
    
    def hour_event(self):
        self.night_events[self.curr_night - 1]()