"""
=========================================================================== [TODO LIST]

TODO LIST
[+] - Added
[-] - Removed
[!] - Tiny Changes
[*] - Changes

[* 0.1] - Save System
[+ 0.1] - Time System(Day & Night)
- World Edit & Create
[! 0.1] - Enemys
[+ 0.1] - Life System
[! 0.1] - Tools & Drops
[! 0.1] - RPG Games GUI
  [+ 0.1] - Main Menu
  [! 0.1] - Pause Menu
  [! 0.1] - Inventory
[+ 0.1] - Discord Rich Presence
[+ 0.1] - Player Color System

=========================================================================== [BUGS LIST]

=========================================================================== [MAP DICTIONARY]

MAP DICTIONARY:
  = Null
0 = Player Spawn
1 = Block
2 = SpikeBall
3 = Spike
4 = Checkpoint
5 = Door
6 = SleepCapsule
7 = Sign (0 = id, 1 = text, 2= style) e.g.: [7,"my text", 0]

"""

import pygame as pyg
from pygame.locals import *
from sys import exit
from .support import BetterPyGame,DataBase
import threading
import time
from pypresence import Presence
import random

BASE_level_map = [
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1',' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1', ' ',' '], 
[' ', '1', '1', ' ', ' ', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', ' ', '1', '1', '1', '1', ' ','1'], 
[' ', '1', '1', ' ', '0', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', '1', ' ',' '], 
[' ', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1', '1', ' ', '1', '1','1'], 
[' ', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', '6', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '1', '1',' '], 
[' ', '1', '1', ' ', ' ', ' ', ' ', '1', ' ', ' ', '1', '1', '1', '1', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', '1', '1', ' ', ' ', ' ', ' ', '1', ' ', ' ', '1','1'], 
[' ', ' ', ' ', ' ', ' ', ' ', '3', '1', ' ', ' ', '1', '1', '1', '1', '3', '3', ' ', ' ', '1', '1', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', '1', '3', ' ', ' ','4'], 
[' ', ' ', ' ', ' ', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', '1', '1', '1', ' ', ' ', '1', '1', ' ', ' ', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', ' ','1'], 
['1', '1', '1', '1', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', '1', '1', '1', ' ', ' ', '1', '1', ' ', ' ', '1', '1', '1', '1', ' ', ' ', '1', '1', '1', '1','1']
]

TEST_level_map = [
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','6','1'],
    ['1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','1','1','1','1','1'],
    ['1',' ',' ','0',' ',' ',[7,"Welcome! this map is for test some tile!",0],' ',' ',' ',' ',' ',' ','3','3','3','1','1','1', [7,"Sign with style 0",0],' ',' ',[7,"Sigb with style 1",1],' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','5',' ','4',' ','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']

]

DEFAULTS_MAP = {"test":TEST_level_map,"base":BASE_level_map}

TILE_SIZE = 64
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = len(TEST_level_map) * TILE_SIZE
GAMETITLE = "Plataformer Game"
VERSION = 0.1

HANDBAR_KEYS = [(1,K_1),(2,K_2),(3,K_3)]

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
C_DARKSLATEBLUE = (72, 61, 139)
C_LIGHTSALMON = (255, 190, 152)

# Setup support class
BPYG =  BetterPyGame(SCREEN)

# Fonts
FONTS_FOLDER = './data/fonts/'
PIXELATED_FONT = FONTS_FOLDER + 'pixelated.ttf'

BPYG.create_font('arial',24,False,False) # 0 Buttons
BPYG.create_font('arial',18,True,False) # 1 Debug Text
BPYG.create_font('arial',36,True,False) # 2 Main Title
BPYG.create_font('arial',14,False,False) # 3 Tiny Button
BPYG.create_font('arial', 20, False,False) # 4 TextBox
BPYG.create_font2(PIXELATED_FONT,24) # 5 Signs font

TEXTURES_FOLDER = './data/textures/'
SOUNDS_FOLDER = './data/sounds/'
SOUNDS_VOLUME = .45
PLAYER_COLORS = ["yellow","blue","green","purple","red"]

"""" DataBase"""
db = DataBase('./data/data.db',True)

MAX_SAVES_PROFILES = 10

basePlayer = {
    "name":"",
    "color":"",
    "inventory":{"handbar":[],"stored":[]},
    "stats":{"level":1,"exp":0,"maxhealth":100,"health":100},
    "checkpoint":(0,0),
    "time":{"hour":0,"minute":0,"day":1}
}

CONFIG_DEFAULT = {
    "volume":1,
    "RPC":True,
    'fps':60,
    "autosave":True
}
CURRENT_CONFIG = CONFIG_DEFAULT
CONFIG_TABLE = "config"
CONFIG_TABLE_COLUMNS = ["config",] # id INTEGER, config TEXT

SAVES_TABLE = "saves" #
SAVES_TABLE_COLUMNS = ["player","map",]

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
