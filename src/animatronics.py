
import my_random

# ----------------------------------------

from enum import Enum, auto
from camera import CameraID

class Location(Enum):
    SHOW_STAGE = auto()
    DINING_AREA = auto()
    PIRATE_COVE = auto()
    WEST_HALL = auto()
    EAST_HALL = auto()
    WEST_CORNER = auto()
    EAST_CORNER = auto()
    OFFICE = auto()

CAMERA_LOCATIONS = {
    CameraID.CAM_1A: Location.SHOW_STAGE,
    CameraID.CAM_1B: Location.DINING_AREA,
    CameraID.CAM_1C: Location.PIRATE_COVE,
    CameraID.CAM_2A: Location.WEST_HALL,
    CameraID.CAM_2B: Location.EAST_HALL,
}

FREDDY_PATHS = {
    Location.SHOW_STAGE: [
        Location.DINING_AREA
    ],

    Location.DINING_AREA: [
        Location.SHOW_STAGE,
        Location.EAST_HALL
    ],

    Location.EAST_HALL: [
        Location.DINING_AREA,
        Location.EAST_CORNER
    ],

    Location.EAST_CORNER: [
        Location.EAST_HALL,
        Location.OFFICE
    ],

    Location.OFFICE: []
}

# ----------------------------------------

class Animatronic:
    def __init__(self, tick_interval: float, ai: int, rng: my_random.Random, location: Location, paths: dict) -> None:

        self.tick_interval = tick_interval
        self.ai: int = ai
        self.accumulator = 0.0

        self.rng = rng

        self.location = location

        self.paths = paths

    def move(self, new_location: Location):
        if self.can_move_to(new_location):
            self.location = new_location
            self.play_sound()

    def play_sound(self):
        pass

    def zwieksz_ai(self, wielkosc: int):
        """Zwiększa agresywność animatronika."""

        self.ai += wielkosc

        if self.ai > 20:
            self.ai = 20

    def get_available_moves(self):
        return self.paths.get(self.location, [])

    def is_visible_on_camera(self, camera_id: CameraID) -> bool:
        return (
            camera_id in CAMERA_LOCATIONS
            and self.location == CAMERA_LOCATIONS[camera_id]
        )

    def can_move_to(self, location: Location) -> bool:
        return location in self.get_available_moves()

# ----------------------------------------
# FREDDY
# ----------------------------------------

class Freddy(Animatronic):
    """Fredyrek Fazmis"""

    def __init__(self, tick_interval, ai, rng):
        super().__init__(tick_interval, ai, rng, Location.SHOW_STAGE, FREDDY_PATHS)

    def update(self, delta: float):
        """Tick-Rate."""

        self.accumulator += delta

        while self.accumulator >= self.tick_interval:
            self.think()
            self.accumulator -= self.tick_interval

    def think(self):
        if self.ai < self.rng.randint(0, 20):
            return

        available_moves = self.get_available_moves()

        if not available_moves:
            return

        next_location = available_moves[
            self.rng.randint(0, len(available_moves) - 1)
        ]

        self.move(next_location)


# ----------------------------------------
# BONNIE
# ----------------------------------------

class Bonnie(Animatronic):
    pass

# ----------------------------------------
# CHICA
# ----------------------------------------

class Chica(Animatronic):
    pass


# ----------------------------------------
# FOXY
# ----------------------------------------

class Foxy(Animatronic):
    pass


# ----------------------------------------
# PUPPET
# ----------------------------------------

class Puppet(Animatronic):
    pass


# ----------------------------------------
# GOLDEN FREDDY
# ----------------------------------------

class GoldenFreddy(Animatronic):
    pass
