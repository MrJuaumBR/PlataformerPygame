import pygame as pyg
from pygame.locals import *
from .config import *

class EndOfScreen(pyg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.size = (SC_WIDTH,10)
        self.StartPos = (0,SC_HEIGHT-10)
        self.color = C_GRAY
        self.rect = Rect(self.StartPos[0],self.StartPos[1],self.size[0],self.size[1])

    def draw(self):
        pyg.draw.rect(SCREEN,self.color,self.rect)

    def update(self):
        """Action to update"""