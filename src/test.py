from enum import Enum

class Color(Enum):
  RED = 1
  GREEN = 2
  BLUE = 3

kolor = Color.RED

print(kolor.value)
print(kolor.name)