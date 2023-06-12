import pygame as pyg
from pygame.locals import *
from .config import *

class tiles(pyg.sprite.Group):
    def draw(self):
        for sprite in self.sprites():
            sprite.draw()

    def update(self):
        for sprite in self.sprites():
            sprite.update()