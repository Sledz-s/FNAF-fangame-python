import os
import sys

# ----------------------------------------

if getattr(sys, "frozen", False):
  BASE_DIR = sys._MEIPASS
else:
  BASE_DIR = os.path.dirname(os.path.dirname(__file__))

RSC_DIR = os.path.join(BASE_DIR, "rsc")
SCREENS_DIR = os.path.join(RSC_DIR, "screens")
CAMERAS_DIR = os.path.join(RSC_DIR, "cam")
