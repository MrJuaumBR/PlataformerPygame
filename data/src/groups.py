from random import randint
from typing import List, Sequence, Union
import pygame as pyg
from pygame.locals import *
from sys import exit

from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface
from .background import clouds
from .settings import *

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

class backgroundGroup(pyg.sprite.Group):
    def __init__(self, *sprites: Sprite | Sequence[Sprite]) -> None:
        super().__init__(*sprites)
        self.c_frames = 0
        self.maxFrames = 30
        self.minutes = 0
        self.maxminutes = 60
        self.hours = 12
        self.maxHours = 24
        self.day = 1
        self.gen_clouds()

        self.day_state = "morning"
        self.colors = {"morning":C_LIGHTSKYBLUE,"night":C_DARKSLATEBLUE,"afternoon":C_LIGHTSALMON}
        self.cur_color = self.colors[self.day_state]

    def gen_clouds(self):
        for _ in range(randint(3,9)):
            c = clouds(self)
            self.add(c)

    def time_logic(self):
        self.c_frames += 1
        if self.c_frames >= self.maxFrames:
            self.c_frames = 0
            self.minutes += 1
        if self.minutes >= self.maxminutes:
            self.minutes = 0
            self.hours += 1
        if self.hours >= self.maxHours:
            self.day += 1
            self.hours = 0
        if self.hours >= 18 or self.hours < 3:
            self.day_state = "night"
        elif self.hours < 12 and self.hours >= 3:
            self.day_state = "morning"
        elif self.hours > 12 and self.hours <= 18:
            self.day_state = "afternoon"
        self.cur_color = self.colors[self.day_state]

    def skipTime(self,days=0,hours=0,minutes=0):
        self.hours += hours
        self.day += days
        self.minutes += minutes

    def getTime(self):
        h = self.hours
        if self.hours<10:
            h = f'0{self.hours}'
        m = self.minutes
        if self.minutes<10:
            m = f'0{self.minutes}'
        return f"{h}:{m}"
    
    def getDay(self):
        d = self.day
        if self.day < 10:
            d = f'0{self.day}'
        return f"{d}"

    def setTimePass(self,FPS=30):
        self.maxFrames = FPS

    def update(self,player_lock:bool):
        if not player_lock:
            self.time_logic()
            return super().update()
        
    def draw(self,surface):
        surface.fill(self.cur_color)
        return super().draw(surface)