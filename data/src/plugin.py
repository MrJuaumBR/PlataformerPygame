"""IF YOU DON'T KNOW WHAT YOU MAKING, DON'T CHANGE NOTHING."""
"""
This a rework for PooPEngine!
"""

import pygame as pyg
from pygame.locals import *
from .config import *

class PooPEngine_Rework():
    def __init__(self,screen):
        self.screen = screen
        self.fonts = []

    def create_font(self,Name='arial',size=16,config={"bold":False,"italic":False}) -> tuple:
        """Create a font, and add to class Fonts List"""
        f = pyg.font.SysFont(Name,size,config["bold"],config["italic"])
        if len(self.fonts) > 0:
            if f in self.fonts:
                print(f'This font already exists.\n\nCan be found in index {self.fonts.index(f)} from PooPEngine_Rework Fonts List.\n\n')
            else:
                self.fonts.append(f)
                return (self.fonts.index(f), f)
        else:
            self.fonts.append(f)
            return (self.fonts.index(f), f)

    def draw_text(self,text="My Text",font=0,XY=(0,0),config={"antialias":False,"background":False,"colors":((0,0,0),(255,255,255))},):
        """Draw text with the font
        Config: if need background color setup colors[1] with the background color
        Colors: colors[0] is the text color, colors[1] is the background color if it set to True
        """
        if type(font) == int:
            font = self.fonts[font]
        if not config['background']:
            f = font.render(text,config['antialias'],config['colors'][0])
        else:
            f = font.render(text,config['antialias'],config['colors'][0],config['colors'][1])
        x = f.get_rect()
        x.topleft = XY
        self.screen.blit(f,x)
        return x

    def draw_button(self,text="My Button",XY=(0,0),font=0,colors=((0,0,0),(255,255,255))):
        """Draw Button"""
        config = {
            "antialias":True,
            "background":True,
            "colors":colors
        }
        f = self.draw_text(text,font,XY,config)
        if f.collidepoint(pyg.mouse.get_pos()):
            if pyg.mouse.get_pressed(3)[0]:
                return True
            else:
                return False
        else:
            return False

