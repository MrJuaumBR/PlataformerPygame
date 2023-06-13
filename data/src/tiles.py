import pygame as pyg
from pygame.locals import *
from sys import exit


class Tile(pyg.sprite.Sprite):
    def __init__(self,Pos,Size):
        super().__init__()
        self.image= pyg.Surface((Size,Size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=Pos)

    def update(self,x_shift):
        self.rect.x += x_shift
