import time
import random_native
import os

class Random:
    def __init__(self):
        seed = int.from_bytes(os.urandom(4), byteorder="little", signed=False)
        random_native.seed(seed)

    def randint(self, a: int, b: int) -> int:
        return random_native.randint(a, b)

    def choice(self, array: list):
        return random_native.choice(array)