import pygame as pyg
from pygame.locals import *
from sys import exit

from pygame.sprite import AbstractGroup
from .support import spritesheet
from .settings import *
from random import choice,randint

class clouds(pyg.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.import_assets()
        self.image = choice(self.images)
        
        self.speed = randint(2,10)
        self.change_frames = 0

        self.rect = self.image.get_rect(topleft=(0,randint(100,SCREEN_HEIGHT-100)))

    def import_assets(self):
        path = TEXTURES_FOLDER + "clouds.png"
        s = spritesheet(path)
        self.images = s.images_at(((1,1,125,46),(132,1,115,51),(83,67,139,31),(16,39,54,23)),0)

    def change_image(self):
        if self.rect.x >= SCREEN_WIDTH:
            self.change_frames += 1
            if self.change_frames == 60:
                self.image = choice(self.images)
                self.rect = self.image.get_rect(topleft=(0,randint(100,SCREEN_HEIGHT-300)))
                self.speed = randint(2,10)
                self.change_frames = 0

    def update(self):
        self.change_image()
        self.rect.x += self.speed