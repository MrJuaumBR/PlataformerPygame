"""
=========================================================================== [TODO LIST]

TODO LIST
[+] - Added
[-] - Removed
[!] - Tiny Changes

[! 0.1] - Save System
- Time System(Day & Night)
- World Edit & Create
[! 0.1] - Enemys
[+ 0.1] - Life System
[! 0.1] - Tools & Drops
[! 0.1] - RPG Games GUI
  [+ 0.1] - Main Menu
  [! 0.1] - Pause Menu
  [! 0.1] - Inventory
[+ 0.1] - Discord Rich Presence

=========================================================================== [MAP DICTIONARY]

MAP DICTIONARY:
  = Null
0 = Player Spawn
1 = Block
3 = SpikeBall
4 = Spike

"""
import pygame as pyg
from pygame.locals import *
from sys import exit
from .support import BetterPyGame,DataBase
import threading
import time
from pypresence import Presence
import random

level_map = [
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1',' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1', ' ',' '], 
[' ', '1', '1', ' ', ' ', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', ' ', '1', '1', '1', '1', ' ','1'], 
[' ', '1', '1', ' ', '0', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ',' '], 
[' ', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', '1', ' ', '1', '1','1'], 
[' ', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '1', '1',' '], 
[' ', '1', '1', ' ', ' ', ' ', ' ', '1', ' ', ' ', '1', '1', '1', '1', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', '1', '1', ' ', ' ', ' ', ' ', '1', ' ', ' ', '1','1'], 
[' ', ' ', ' ', ' ', ' ', ' ', '4', '1', ' ', ' ', '1', '1', '1', '1', '4', '4', ' ', ' ', '1', '1', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', '1', '4', ' ', ' ',' '], 
[' ', ' ', ' ', ' ', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', '1', '1', '1', ' ', ' ', '1', '1', ' ', ' ', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', ' ','1'], 
['1', '1', '1', '1', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', '1', '1', '1', ' ', ' ', '1', '1', ' ', ' ', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', '1','1']
]


TILE_SIZE = 64
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = len(level_map) * TILE_SIZE
GAMETITLE = "Plataformer Game"
VERSION = 0.1

pyg.init()
SCREEN = pyg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),FULLSCREEN)
CLOCK = pyg.time.Clock()

SCREEN_HEIGHT = SCREEN.get_size()[1] # Update for the fullscreen window size
SCREEN_WIDTH = SCREEN.get_size()[0]
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

HALF_SCREEN_HEIGHT = SCREEN_HEIGHT//2
HALF_SCREEN_WIDTH = SCREEN_WIDTH//2
HALF_SCREEN_SIZE = (HALF_SCREEN_WIDTH,HALF_SCREEN_WIDTH)

C_LIGHTCYAN = (224, 255, 255)
C_CORNSILK = (255, 248, 220)
C_SANDYBROWN = (244, 164, 96)
C_LIGHTSKYBLUE = (135, 206, 250)
C_WHITE = (255,255,255)
C_BLACK = (0,0,0)
C_RED = (255,0,0)
C_GREEN = (0,255,0)
C_BLUE = (0,0,255)
C_BEIGE = (238, 220, 154)
C_NAVY = (10, 17, 114)
C_INDIGO = (40, 30, 93)

# Setup support class
BPYG =  BetterPyGame(SCREEN)

# Fonts
BPYG.create_font('arial',24,False,False) # 0 Buttons
BPYG.create_font('arial',18,True,False) # 1 Debug Text
BPYG.create_font('arial',36,True,False) # 2 Main Title
BPYG.create_font('arial',14,False,False) # 3 Tiny Button

TEXTURES_FOLDER = './data/textures/'
SOUNDS_FOLDER = './data/sounds/'

# DataBase
MAX_SAVES_PROFILES = 10
CONFIG_TABLE = "config"
CONFIG_TABLE_COLUMNS = ["config",] # id INTEGER, config TEXT
SAVES_TABLE = "" #

db = DataBase('./data/data.db',True)
db.create_table("config",["id INTEGER PRIMARY KEY AUTOINCREMENT","config TEXT"])
#db.insert('config',CONFIG_TABLE_COLUMNS,["'{}'",])

""" DISCORD RICH PRESENCE SETUP"""

DISCORD_ID = "1118603178473173074" # Discord Application.

states = ["Let's learn Python!",f'{GAMETITLE} developed in Python','What do you think?','Potato, Potato i like!']

if DISCORD_ID:
    RPC = Presence(DISCORD_ID)
    RPC.connect()
    print("Connected with discord.")
    RPC.update(
    state=random.choice(states), 
    details="Playing...",
    large_text=GAMETITLE,
    large_image=str(random.randint(1,2))
    )

def Setup_Discord(GAME_RUNNING):
    while True:
        if not GAME_RUNNING():
            print("Break Discord.")
            exit()
            break
