"""
TODO LIST
[+] - Added
[-] - Removed
[!] - Tiny Changes
[*] - No Changes

- Player Sprite
[+ 0.1] - Menus
[+ 0.1] - Gravity System
[+ 0.1] - Add Launch.json
[+ 0.1] - World Class
[+ 0.1] - Time
- Save Select Menu
- Game Gui & Icons
- Plataforms

"""





import pygame as pyg
from pygame.locals import *
from .world import World
from .plugin import PooPEngine_Rework

pyg.init() # Pygame Init

# Game Pre-Build
SC_WIDTH = 800
SC_HEIGHT = 600
SC_SIZE = (SC_WIDTH,SC_HEIGHT)

SC_HALF_SIZE=(SC_WIDTH//2,SC_HEIGHT//2)

GAMETITLE = "TESTING GAME // "
VERSION = 0.1

# Cores
C_RED = (255,0,0)
C_GREEN = (0,255,0)
C_BLUE = (0,0,255)
C_BLACK = (0,0,0)
C_WHITE = (255,255,255)
C_GRAY = (100,100,100)
C_LIME = (30, 230, 86)

# Game Set
GRAVITY_FORCE = 3.2
JUMP_FORCE = GRAVITY_FORCE * 3 # Gravity Force + 200%
JUMP_FRAMES_WAIT = 10

# Screen Create
SCREEN = pyg.display.set_mode(SC_SIZE)
pyg.display.set_caption(GAMETITLE+str(VERSION)) # Set Screen Caption/Title

# Clock
PYG_CLOCK = pyg.time.Clock()
FPS = 60

# Setup Classes
CLS_WORLD = World()
PPE = PooPEngine_Rework(SCREEN)

# Fonts
PPE.create_font(size=26) # Title Font
PPE.create_font()