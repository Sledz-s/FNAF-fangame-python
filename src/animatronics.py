
import my_random

# ----------------------------------------

class Animatronic:
    def __init__(self, board: list, tick_interval: float, ai: int, rng: my_random.Random) -> None:

        self.board = board
        self.tick_interval = tick_interval
        self.ai: int = ai
        self.accumulator = 0.0

        self.rng = rng

        self.cam_x = 0
        self.cam_y = 0
        self.cam_x_old = 0
        self.cam_y_old = 0

        self.board[self.cam_x][self.cam_y] = 1

    # ----------------------------------------

    def move(self, cam_x: int, cam_y: int):
        """Zmienia pozycję animatronika w tablicy."""

        self.board[self.cam_x_old][self.cam_y_old] = 0

        self.cam_x = cam_x
        self.cam_y = cam_y

        self.board[self.cam_x][self.cam_y] = 1

        self.cam_x_old = self.cam_x
        self.cam_y_old = self.cam_y

    # ----------------------------------------

    def zwieksz_ai(self, wielkosc: int):
        """Zwiększa agresywność animatronika."""

        self.ai += wielkosc

        if self.ai > 20:
            self.ai = 20

    # ----------------------------------------

    def border(self) -> bool:
        """Sprawdza, czy wybrany kafel jest sąsiadujący."""

        return (
            abs(self.cam_x - self.cam_x_old)
            + abs(self.cam_y - self.cam_y_old)
        ) == 1


# ----------------------------------------
# FREDDY
# ----------------------------------------

class Freddy(Animatronic):
    """Fredyrek Fazmis"""

    def __init__(self, board, tick_interval, ai, rng):
        super().__init__(board, tick_interval, ai, rng)

    def update(self, delta: float):
        """Tick-Rate."""

        self.accumulator += delta

        if self.accumulator >= self.tick_interval:
            self.think()
            self.accumulator -= self.tick_interval

    def think(self):
        """
        Porusza się po kamerach, aby zbliżyć się do biura.
        """

        if self.ai < self.rng.randint(0, 20):
            return

        self.cam_x = self.rng.randint(0, 2)
        self.cam_y = self.rng.randint(0, 2)

        while not self.border():
            self.cam_x = self.rng.randint(0, 2)
            self.cam_y = self.rng.randint(0, 2)

        self.move(self.cam_x, self.cam_y)


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
