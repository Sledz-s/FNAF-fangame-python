import random

# ----------------------------------------

class Animatronic:
    def __init__(self, board: list, tick_interval, ai: int) -> None:
        self.board = board
        self.tick_interval = tick_interval
        self.ai: int = ai
        self.accumulator = 0.0

        self.cam_x = 0
        self.cam_y = 0
        self.cam_x_old = 0
        self.cam_y_old = 0

        self.board[self.cam_x][self.cam_y] = 1

    def move(self, cam_x, cam_y):
        """zmienia pozycje animatronika w tablicy"""
        self.board[self.cam_x_old][self.cam_y_old] = 0
        self.cam_x = cam_x
        self.cam_y = cam_y
        self.board[self.cam_x][self.cam_y] = 1
        self.cam_x_old = self.cam_x
        self.cam_y_old = self.cam_y

    def zwieksz_ai(self, wielkosc):
        """sluzy do zwiekszania agresywnosci animatronika, nie uzywac wartosci ujemnych"""
        self.ai += wielkosc
        if self.ai > 20:  # cap ai, żeby nie wywalilo wiecej niz 20
            self.ai = 20

    def border(self):  # do usunięcia
        """Sprawdza czy kafel do którego ma się poruszać jest obok"""
        return abs(self.cam_x - self.cam_x_old) + abs(self.cam_y - self.cam_y_old) == 1

# ----------------------------------------

class Freddy(Animatronic):
    """Fredyrek Fazmis"""

    def __init__(self, board, tick_interval, ai):
        super().__init__(board, tick_interval, ai)

    def update(self, delta):  # Tick-Rate
        self.accumulator += delta
        if self.accumulator >= self.tick_interval:
            self.think()
            self.accumulator -= self.tick_interval

    def think(self):  # De facto logika animatronika
        """
        Porusza się po kamerach by zbliżyć się do biura,
        świecenie na niego na kamerach odstraszy go!
        Jeśli jest przy drzwiach, już ich nie opuści
        """
        if self.ai < random.randint(0, 20):
            return

        self.cam_x = random.randint(0, 2)
        self.cam_y = random.randint(0, 2)

        while not self.border():
            self.cam_x = random.randint(0, 2)
            self.cam_y = random.randint(0, 2)

        self.move(self.cam_x, self.cam_y)

# ----------------------------------------


class Bonnie(Animatronic):
    pass
# ----------------------------------------


class Chica(Animatronic):
    pass
# ----------------------------------------


class Foxy(Animatronic):
    pass
# ----------------------------------------


class Puppet(Animatronic):
    pass
# ----------------------------------------


class GoldenFreddy(Animatronic):
    pass
import random

# ----------------------------------------

class Animatronic:
    def __init__(self, board: list, tick_interval, ai: int) -> None:
        self.board = board
        self.tick_interval = tick_interval
        self.ai: int = ai
        self.accumulator = 0.0

        self.cam_x = 0
        self.cam_y = 0
        self.cam_x_old = 0
        self.cam_y_old = 0

        self.board[self.cam_x][self.cam_y] = 1

    def move(self, cam_x, cam_y):
        """zmienia pozycje animatronika w tablicy"""
        self.board[self.cam_x_old][self.cam_y_old] = 0
        self.cam_x = cam_x
        self.cam_y = cam_y
        self.board[self.cam_x][self.cam_y] = 1
        self.cam_x_old = self.cam_x
        self.cam_y_old = self.cam_y

    def zwieksz_ai(self, wielkosc):
        """sluzy do zwiekszania agresywnosci animatronika, nie uzywac wartosci ujemnych"""
        self.ai += wielkosc
        if self.ai > 20:  # cap ai, żeby nie wywalilo wiecej niz 20
            self.ai = 20

    def border(self):  # do usunięcia
        """Sprawdza czy kafel do którego ma się poruszać jest obok"""
        return abs(self.cam_x - self.cam_x_old) + abs(self.cam_y - self.cam_y_old) == 1

# ----------------------------------------

class Freddy(Animatronic):
    """Fredyrek Fazmis"""

    def __init__(self, board, tick_interval, ai):
        super().__init__(board, tick_interval, ai)

    def update(self, delta):  # Tick-Rate
        self.accumulator += delta
        if self.accumulator >= self.tick_interval:
            self.think()
            self.accumulator -= self.tick_interval

    def think(self):  # De facto logika animatronika
        """
        Porusza się po kamerach by zbliżyć się do biura,
        świecenie na niego na kamerach odstraszy go!
        Jeśli jest przy drzwiach, już ich nie opuści
        """
        if self.ai < random.randint(0, 20):
            return

        self.cam_x = random.randint(0, 2)
        self.cam_y = random.randint(0, 2)

        while not self.border():
            self.cam_x = random.randint(0, 2)
            self.cam_y = random.randint(0, 2)

        self.move(self.cam_x, self.cam_y)

# ----------------------------------------


class Bonnie(Animatronic):
    pass
# ----------------------------------------


class Chica(Animatronic):
    pass
# ----------------------------------------


class Foxy(Animatronic):
    pass
# ----------------------------------------


class Puppet(Animatronic):
    pass
# ----------------------------------------


class GoldenFreddy(Animatronic):
    pass