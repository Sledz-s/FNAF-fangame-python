
import pygame

from assets import AssetManager
from camera import Camera, CameraID
from animatronics import Freddy
from enum import Enum, auto
from button import ImageButton, CamButton, TextButton
from video import *
from my_random import Random
from audio import Audio

# ----------------------------------------
# --- KONSTANTY ---

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameState(Enum):
    STATE_START_TEXT = auto()
    STATE_TITLE = auto()
    STATE_LOADING = auto()
    STATE_GAME = auto()
    STATE_NIGHT_END = auto()

class SubStateMachine(Enum):
    SUBSTATE_OFFICE = auto()
    SUBSTATE_CAM = auto()

class AnimatronicID(Enum):
    FREDDY = auto()
    BONNIE = auto()
    CHICA = auto()
    FOXY = auto()
    PUPPET = auto()
    GOLDEN_FREDDY = auto()


# ----------------------------------------
# --- GAME ---


class Game:
    def __init__(self, video: Video, assets: AssetManager, audio: Audio) -> None:

        self.video = video
        self.screen = self.video.screen

        self.width, self.height = self.screen.get_size()
        self.running = True

        self.assets = assets
        self.audio = audio
        
        # self.video.toggle_fullscreen()

        # ----------------------------------------
        # Generator liczb losowych

        self.rng = Random()

        # ----------------------------------------
        # Maszyna stanów

        self._state = GameState.STATE_START_TEXT
        self._substate = None
        self._target_state = None

        # ----------------------------------------
        # Kamera

        self.current_cam_id = CameraID.CAM_1A

        # ----------------------------------------
        # Inicjalizacja

        self._init_assets()
        self._init_ui()
        self._init_entities()

        self.wait_time = 0.0

        # ----------------------------------------
        # TEST
        
        self.audio.music.play(0)
        self.audio.music.set_volume(0.25)

    # ----------------------------------------
    # --- ASSETS ---

    def _init_assets(self):

        self.font = pygame.font.Font(None, 36)

        self.text_cache = {}

        self.backgrounds = {
            GameState.STATE_START_TEXT: Background(
                self.assets,
                "screens/FryderykFramework.png"
            ),

            GameState.STATE_TITLE: Background(
                self.assets,
                "screens/title_PLACEHOLDER.png",
                (self.width, self.height)
            ),

            GameState.STATE_GAME: Background(
                self.assets,
                "screens/office_PLACEHOLDER.png"
            )
        }

        self.cam_bg = {
            CameraID.CAM_1A: Background(
                self.assets, "cam/cam01a_PLACEHOLDER.png"
            ),

            CameraID.CAM_1B: Background(
                self.assets, "cam/cam01b_PLACEHOLDER.png"
            ),

            CameraID.CAM_1C: Background(
                self.assets, "cam/cam01c_PLACEHOLDER.png"
            ),

            CameraID.CAM_2A: Background(
                self.assets, "cam/cam02a_PLACEHOLDER.png"
            ),

            CameraID.CAM_2B: Background(
                self.assets, "cam/cam02b_PLACEHOLDER.png"
            )
        }

        self.sfx_camera_static = ScreenEffects()
        self.sfx_camera_static.add_effect(
            ImageEffect(self.assets, image="bg/sfx/static/cam_static_1.png", alpha=100)
        )

    # ----------------------------------------
    # --- UI ---

    def _init_ui(self):

        self.new_game_bttn = TextButton(
            x=self.width - 160,
            y=160,
            text="NEW GAME",
            font=self.font,
            id="start"
        )

        self.camera_onoff_bttn = ImageButton(
            assets=self.assets,
            x=self.width // 2,
            y=self.height - 40,
            images=[
                "start_idle_PLACEHOLDER_.png",
                None,
                "start_pressed_PLACEHOLDER_.png"
            ]
        )

        self.cam_bttn = [
            CamButton(
                assets=self.assets,
                x=self.width - 160,
                y=160 + i * 40,
                images=[
                    "start_idle_PLACEHOLDER_.png",
                    None,
                    None,
                    "start_pressed_PLACEHOLDER_.png"
                ],
                id=cam_id
            )
            for i, cam_id in enumerate(CameraID)
        ]

        self.sfx_camera_static = ScreenEffects()
        self.sfx_camera_static.add_effect(
            AnimatedImageEffect(
            self.assets,
            images=[
               "bg/sfx/static/cam_static_1.png",
                "bg/sfx/static/cam_static_2.png",
                "bg/sfx/static/cam_static_3.png",
                "bg/sfx/static/cam_static_4.png",
                "bg/sfx/static/cam_static_5.png",
                "bg/sfx/static/cam_static_6.png",
                "bg/sfx/static/cam_static_7.png",
                "bg/sfx/static/cam_static_8.png"
                ],
            frame_time=0.05, alpha=70
            )
        )

    # ----------------------------------------
    # --- ENTITIES ---

    def _init_entities(self):

        self.camera = Camera(self.width, self.height)

        self.fade = FadeTransition(self.width,self.height,speed=400)

        self.current_night = None

    # ----------------------------------------
    # --- STATE MACHINE ---

    def change_state(self, new_state):

        if not self.fade.active:
            self._target_state = new_state
            self.fade.start("OUT")

    def init_state_change(self):

        self._state = self._target_state

        match self._state:

            case GameState.STATE_START_TEXT:
                self._substate = None

            case GameState.STATE_TITLE:
                self._substate = None

            case GameState.STATE_GAME:

                self.current_night = Night(curr_night=1, game=self)

                self._substate = SubStateMachine.SUBSTATE_OFFICE

            case GameState.STATE_NIGHT_END:
                self._substate = None

        self.fade.start("IN")
        self._target_state = None

    # ----------------------------------------
    # --- EVENTS ---

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            match self._state:

                case GameState.STATE_START_TEXT:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

                case GameState.STATE_TITLE:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

                    if self.new_game_bttn.handler(event):
                        self.change_state(
                            GameState.STATE_GAME
                        )

                case GameState.STATE_GAME:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.change_state(
                                GameState.STATE_TITLE
                            )

                    match self._substate:

                        case SubStateMachine.SUBSTATE_OFFICE:

                            if self.camera_onoff_bttn.handler(event):
                                self._substate = (
                                    SubStateMachine.SUBSTATE_CAM
                                )

                        case SubStateMachine.SUBSTATE_CAM:

                            for bttn in self.cam_bttn:
                                if bttn.handler(event):
                                    self.select_camera(bttn.id) 

                            if self.camera_onoff_bttn.handler(event):
                                self._substate = (
                                    SubStateMachine.SUBSTATE_OFFICE
                                )

    # ----------------------------------------
    # --- UPDATE ---

    def update(self, deltatime):

        if self.fade.update(deltatime):
            self.init_state_change()

        match self._state:

            case GameState.STATE_START_TEXT:

                self.wait_time += deltatime

                if self.wait_time >= 1.0:
                    self.wait_time = 0.0
                    self.change_state(
                        GameState.STATE_TITLE
                    )

            case GameState.STATE_TITLE:

                self.new_game_bttn.update()

            case GameState.STATE_GAME:

                self.current_night.update(deltatime)

                self.camera_onoff_bttn.update()

                if self._substate == SubStateMachine.SUBSTATE_OFFICE:
                    self._update_camera_view(deltatime)

                elif self._substate == SubStateMachine.SUBSTATE_CAM:

                    self.sfx_camera_static.update(deltatime)
                    
                    for bttn in self.cam_bttn:
                        bttn.update()

            case GameState.STATE_NIGHT_END:

                self.wait_time += deltatime

                if self.wait_time >= 1.0:
                    self.wait_time = 0.0
                    self.change_state(
                        GameState.STATE_TITLE
                    )

    # ----------------------------------------
    # --- DRAW ---

    def draw(self):
        background = self.backgrounds[self._state]

        match self._state:

            case GameState.STATE_TITLE:

                background.draw(self.screen,self.camera)
                self.new_game_bttn.draw(self.screen)

            case GameState.STATE_START_TEXT:

                background.draw(
                    self.screen,
                    self.camera
                )

                self.print_on_screen(
                    "Fryderyk Framework",
                    (self.width // 2, 30)
                )

            case GameState.STATE_GAME:

                godzina_tekst = (f"Godzina: {self.current_night.godzina if self.current_night.godzina != 0 else 12} AM")

                if self._substate == SubStateMachine.SUBSTATE_OFFICE:

                    background.draw(self.screen,self.camera)

                elif self._substate == SubStateMachine.SUBSTATE_CAM:

                    self.cam_bg[self.current_cam_id].draw(
                        self.screen,
                        self.camera
                    )

                    self.sfx_camera_static.draw(self.screen) # <----- here is static overlay

                    self.print_on_screen(
                        f"KAMERA: {self.current_cam_id.name}",
                        (self.width // 2, 30)
                    )

                    self.draw_animatronics_on_camera()

                    for bttn in self.cam_bttn:
                        bttn.draw(self.screen)

                    

                self.camera_onoff_bttn.draw(self.screen)

                self.print_on_screen(
                    godzina_tekst,
                    (100, 30)
                )

        # ----------------------------------------
        # Debug

        self.print_on_screen(
            f"State: {self._state.name}",
            (self.width - 150, 30)
        )

        self.fade.fade_transition(self.screen)

        pygame.display.flip()

    # ----------------------------------------
    # --- ANIMATRONICS RENDERING ---

    def draw_animatronics_on_camera(self):

        for animatronic in self.current_night.animatronics:

            if animatronic.is_visible_on_camera(self.current_cam_id):
                self.print_on_screen(f'Widoczny:{type(animatronic).__name__} {animatronic.location}',
                                    (self.width - 600, 60))

    # ----------------------------------------
    # --- HELPERS ---

    def print_on_screen(self, text, pos, color=WHITE):
        key = (text, color)

        if key not in self.text_cache:
            self.text_cache[key] = self.font.render(text, True, color)

        surf = self.text_cache[key]
        rect = surf.get_rect(center=pos)

        self.screen.blit(surf, rect)

    def select_camera(self, camera_id):
        self.current_cam_id = camera_id

        for bttn in self.cam_bttn:
            bttn.is_active = bttn.id == camera_id

    # ----------------------------------------
    # --- CAMERA VIEW ---

    def _update_camera_view(self, deltatime: float):
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
          self.camera.rect.x = max(0, min(self.camera.rect.x, max_x))  

class LoadingScreen:
    __slots__ = ('game', 'progress', 'tasks')

    def __init__(self, game):
        self.game = game
        self.progress = 0
        self.tasks = []

    def update(self, deltatime):
        pass

    def draw(self, screen):
        pass

class Night:
    """Zarządza logiką godzin i aktualizowaniem AI przeciwników."""

    def __init__(self, curr_night: int, game: Game) -> None:
        self.game: Game = game

        self.curr_night = curr_night
        self.accumulator: float = 0
        self.godzina: int = 0
        
        self.dl_godzina = 90

        self.night_events = [
            self.night_1_event,
            self.night_2_event,
            self.night_3_event,
        ]

        self._create_animatronics()
        
    def _create_animatronics(self):

        self.freddy: Freddy = Freddy(tick_interval=1.0,ai=1,rng=self.game.rng)
                
        self.animatronics: list = [
            self.freddy
        ]

    def update(self, deltatime: float):
        self.accumulator += deltatime

        while self.accumulator >= self.dl_godzina and self.godzina < 6:
            self.accumulator -= self.dl_godzina
            self.godzina += 1
            self.hour_event()

        for animatronic in self.animatronics:
            animatronic.update(deltatime)

    def _boost_ai(self, animatronic_id: AnimatronicID, amount: int):
        self.animatronics[animatronic_id.value].increase_ai(amount)

    def night_1_event(self):
        match self.godzina:
            case 1:
                pass

            case 2:
                pass

            case 3:
                self._boost_ai(AnimatronicID.FREDDY, 1)

            case 4:
                self._boost_ai(AnimatronicID.FREDDY, 2)

            case 5:
                self._boost_ai(AnimatronicID.FREDDY, 3)

            case 6:
                self.game.change_state(GameState.STATE_NIGHT_END)

    def night_2_event(self):
            match self.godzina:
                case 1:
                    pass
    
                case 2:
                    pass
    
                case 3:
                    self._boost_ai(AnimatronicID.FREDDY, 1)
    
                case 4:
                    self._boost_ai(AnimatronicID.FREDDY, 2)
    
                case 5:
                    self._boost_ai(AnimatronicID.FREDDY, 3)
    
                case 6:
                    self.game.change_state(GameState.STATE_NIGHT_END)

    def night_3_event(self):
            match self.godzina:
                case 1:
                    pass
    
                case 2:
                    pass
    
                case 3:
                    self._boost_ai(AnimatronicID.FREDDY, 1)
    
                case 4:
                    self._boost_ai(AnimatronicID.FREDDY, 2)
    
                case 5:
                    self._boost_ai(AnimatronicID.FREDDY, 3)
    
                case 6:
                    self.game.change_state(GameState.STATE_NIGHT_END)
    
    def hour_event(self):
        self.night_events[self.curr_night - 1]()