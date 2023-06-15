from random import randint
import pygame as pyg
from pygame.locals import *
from sys import exit

from data.src.settings import C_SANDYBROWN
from .settings import *
from .support import spritesheet

class Tile(pyg.sprite.Sprite):
    def __init__(self,Pos,Size,color=C_SANDYBROWN):
        super().__init__()
        self.priority = 0
        self.type = "Tile"
        if type(Size) == int:
            self.image= pyg.Surface((Size,Size))
        elif type(Size) in [tuple,list]:
            self.image = pyg.Surface((Size[0],Size[1]))
        if color:
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=Pos)

    def update(self,x_shift):
        self.rect.x += x_shift

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        

class DeadPoint(Tile):
    def __init__(self, Pos, Size):
        super().__init__(Pos, Size)
        self.type = "Damage"
        self.damage = 10000000000000000000

    def update(self, x_shift): # Fixed
        pass

class SpikeBall(Tile):
    def __init__(self, Pos, Size):
        super().__init__(Pos, Size,None)

        self.setup_assets()
        self.animation_index = 0

        self.type = "Damage"
        self.damage = 10
        self.color = (200,0,0)
        self.image = pyg.transform.scale(self.animations[int(self.animation_index)],(TILE_SIZE,TILE_SIZE))

        self.angle = 15
        self.frames = 0

    def setup_assets(self):
        path = TEXTURES_FOLDER + 'SpikeBall.png'
        s = spritesheet(path)
        self.animations = s.images_at(((1,1,16,16),(16,1,16,16),(32,1,16,16)),0)

    def animate(self):
        self.animation_index += 0.15
        if self.animation_index > len(self.animations):
            self.animation_index = 0
        self.image = pyg.transform.scale(self.animations[int(self.animation_index)],(TILE_SIZE,TILE_SIZE))

    def update(self, x_shift):
        self.animate()
        if self.frames < 10:
            self.frames += 1
            self.angle += randint(1,5)
        elif self.frames == 10:
            self.frames = 0
            #self.image = pyg.transform.rotate(self.image,self.angle)
        return super().update(x_shift)

    def draw(self,surface):
        surface.blit(self.image,self.rect)

class Spike(Tile):
    def __init__(self, Pos, Size):
        super().__init__(Pos, Size, color=None)
        self.import_assets()
        self.priority = 1
        self.animation_index = 0
        self.image = self.animation[int(self.animation_index)]
        self.rect = self.image.get_rect(topleft=Pos)
        self.Pos = Pos

        # Damage
        self.type = "Damage"
        self.damage = 10

    def animate(self):
        self.animation_index += 0.15
        if self.animation_index > len(self.animation):
            self.animation_index = 0
        self.image = pyg.transform.scale(self.animation[int(self.animation_index)],(TILE_SIZE,TILE_SIZE))
        r = self.image.get_rect()
        r.center = self.rect.center
        r.top =self.Pos[1]+TILE_SIZE
        r.height += 2
        self.rect = r
        """self.rect = self.image.get_rect()

        self.rect2 = self.rect
        self.rect2.topleft=self.Pos
        self.rect2.height += 2
        self.rect2.y += TILE_SIZE"""

    def import_assets(self):
        path = TEXTURES_FOLDER+'/spike.png'
        s = spritesheet(path)
        self.animation = s.images_at(((93,1,23,19),),0)
    
    def update(self,x_shift):
        self.animate()
        return super().update(x_shift)
    
    def draw(self,surface):
        surface.blit(self.image,self.rect)