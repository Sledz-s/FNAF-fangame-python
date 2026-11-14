import time
import random_native

class Random:
    def __init__(self):
        seed = int(time.time()) & 0xFFFFFFFF
        random_native.seed(seed)

    def randint(self, a: int, b: int) -> int:
        return random_native.randint(a, b)