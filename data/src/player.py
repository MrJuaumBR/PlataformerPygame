import pygame as pyg
from pygame.locals import *
from sys import exit
from .support import spritesheet
from random import randint

class player(pyg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # Player Draw
        self.image = self.animations['idle'][self.frame_index]
        self.image = pyg.transform.scale(self.image,size=(64,64))
        self.rect = self.image.get_rect(topleft=pos)

        # Player Movement
        self.direction = pyg.math.Vector2(0,0)
        self.SPEED = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # Player Status
        self.status = "idle"
        self.facing = "right"
        
    def animate(self):
        animation = self.animations[self.status]

        # loop
        self.frame_index +=self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index =0

        self.image = pyg.transform.scale(animation[int(self.frame_index)],(64,64))
        if self.facing == "left":
            self.image = pyg.transform.flip(self.image,True,False)

    def import_character_assets(self):
        character_path = "./data/textures/player.png"
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}
        ss = spritesheet(character_path)
        self.animations['run'] = ss.images_at([(0,0,16,16),(16,0,16,16),(32,0,16,16)])
        self.animations['idle'] = (ss.image_at((16,16,16,16)),)
        self.animations['jump'] = (ss.image_at((0,16,16,16)),)
        self.animations['fall'] = (ss.image_at((32,16,16,16)),)

    def get_input(self):
        keys = pyg.key.get_pressed()
        if keys[K_RIGHT] or keys[K_d]:
            self.direction.x = 1
            self.facing = "right"
        elif keys[K_LEFT] or keys[K_a]:
            self.direction.x = -1
            self.facing = "left"
        else:
            self.direction.x = 0

        if keys[K_SPACE] or keys[K_UP] or keys[K_w]:
            self.jump()

    def get_status(self):
        if self.direction.y <0:
            self.status = "jump"
        elif self.direction.y >1:
            self.status = "fall"
        else:
            if self.direction.x  != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):

        self.get_input()
        self.get_status()
        self.animate()