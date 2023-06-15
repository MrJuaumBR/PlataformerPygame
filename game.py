import pygame as pyg
from pygame.locals import *
from sys import exit

from data.src.menus import *

# Pygame Setup

if __name__ == '__main__':
    if db.get(1,'config'):
        print('Config line exists!')
    else:
        print('Config line not exists!')
        db.insert('config',CONFIG_TABLE_COLUMNS,["'{}'",])
    main()