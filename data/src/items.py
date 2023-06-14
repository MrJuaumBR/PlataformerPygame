import pygame as pyg
from pygame.locals import *
from sys import exit

class item():
    def __init__(self):        
        self.icon = pyg.Surface((16,16))
        self.image = pyg.Surface((32,32))

        # Tool Attributes
        self.name = ""
        self.can_mine = False
        self.damage = 0
        self.mine_power = 0
        self.ToolType = ""
        self.ToolTip = ""
        self.can_stack = False
        self.max_stack = 1
        self.current_stack = 1
