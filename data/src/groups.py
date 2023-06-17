from typing import List
import pygame as pyg
from pygame.locals import *
from sys import exit

from pygame.rect import Rect
from pygame.surface import Surface

class TilesGroup(pyg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.player = None
    """
    def draw(self, surface: Surface) -> List[Rect]:
        return super().draw(surface)
    """
    def draw(self, surface: Surface) -> List[Rect]:
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.priority):
            sprite.draw(surface)