import pygame as pyg
from pygame.locals import *
from sys import exit

from data.src.menus import *
from data.src.settings import *

# Database Setup
db.create_table("config",["id INTEGER PRIMARY KEY AUTOINCREMENT","config TEXT"]) 
db.create_table("saves",["id TEXT","player TEXT"])

if __name__ == '__main__':
    if db.get(1,'config'):
        print('Config line exists!')
    else:
        print('Config line not exists!')
        db.insert('config',CONFIG_TABLE_COLUMNS,[CONFIG_DEFAULT,])
    main()     