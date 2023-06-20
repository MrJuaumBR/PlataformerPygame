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
        self.collide = True
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
        r.topleft = self.rect.topleft
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
        self.animation = s.images_at(((93,1,23,23),),0)
    
    def update(self,x_shift):
        self.animate()
        return super().update(x_shift)
    
    def draw(self,surface):
        surface.blit(self.image,self.rect)

class Checkpoint(Tile):
    def __init__(self, Pos, Size, color=C_SANDYBROWN):
        super().__init__(Pos, Size, color=None)
        self.import_assets()
        self.animation_index = 0 # 0.15
        self.image = pyg.transform.scale(self.animations[int(self.animation_index)],(TILE_SIZE,TILE_SIZE))

        self.type = 'checkpoint'
        self.collide = False
    
    def animate(self):
        self.animation_index += .15
        if self.animation_index > len(self.animations):
            self.animation_index = 0
        self.image = pyg.transform.scale(self.animations[int(self.animation_index)],(TILE_SIZE,TILE_SIZE))

    def action(self,player):
        if player.rect.colliderect(self.rect):
            player.checkpoint = self.rect.center
    def import_assets(self):
        path = TEXTURES_FOLDER+'flag.png'
        s = spritesheet(path)
        self.animations = s.images_at(((1,1,32,31),(32,1,32,31),(64,1,32,31),(96,1,32,31)),0)

    def update(self, x_shift):
        self.action(self.groups()[0].player)
        self.animate()
        return super().update(x_shift)
    
class Door(Tile):
    def __init__(self, Pos, Size):
        super().__init__(Pos, Size, None)
        self.state = "close"
        self.bstate = False
        self.type = "action"
        self.pos = Pos
        self.import_assets()
        self.image = self.images[self.state]
        self.collide = True
        self.rect = self.image.get_rect(topleft=Pos)
        self.hitbox = BPYG.draw_rect(self.rect.center,(TILE_SIZE*3,TILE_SIZE*3),(0,0,0),0)

    def import_assets(self):
        path = TEXTURES_FOLDER+'door.png'
        s = spritesheet(path)
        self.images = {"close":[],"open":[]}
        ci = s.image_at((42,0,7,32),0)
        self.images['close'] = pyg.transform.scale(ci,(ci.get_rect().width,TILE_SIZE))
        self.images['open'] = pyg.transform.scale(s.image_at((0,0,32,32),0),(TILE_SIZE,TILE_SIZE))

    def action(self,player):
        if BPYG.while_key_hold(K_KP_ENTER) or pyg.mouse.get_pressed(3)[2] and player.rect.colliderect(self.hitbox):
            self.bstate = not self.bstate
            if self.bstate:
                self.state = "open"
                self.collide = False
            else:
                if player.rect.colliderect(self.rect):
                    if player.facing == "left":
                        a = TILE_SIZE
                    elif player.facing == "right":
                        a = -TILE_SIZE
                    player.rect.x += a
                self.state = "close"
                self.collide = True

            self.sound = SOUNDS_FOLDER+f'door_{self.state}.wav'
            BPYG.play_sound(self.sound,SOUNDS_VOLUME)
            self.image = self.images[self.state]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            pyg.time.delay(250)
    
    def update(self,x_shift):
        player = self.groups()[0].player
        if self.hitbox.colliderect(player.rect):
            self.action(player)
        return super().update(x_shift)
    
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        self.hitbox = BPYG.draw_rect2(self.rect.center,(TILE_SIZE*3,TILE_SIZE*3),(0,0,0),0)

class sCapsule(Tile):
    def __init__(self, Pos, Size):
        super().__init__(Pos, Size, None)
        self.import_assets()
        self.image_index = 0

        self.image = pyg.transform.scale((self.images[int(self.image_index)]),(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft=Pos)

        self.type = "action"

        self.used = False

        self.hitbox = BPYG.draw_rect(self.rect.center,(TILE_SIZE*3,TILE_SIZE*3),(0,0,0),0)

    def import_assets(self):
        path = TEXTURES_FOLDER+'sCapsule.png'
        s = spritesheet(path)
        self.images = s.images_at(((11,5,42,56),(71,5,42,56)),0)

    def check_used(self):
        if self.used:
            self.image_index = 1
        else:
            self.image_index = 0
        self.image = pyg.transform.scale((self.images[int(self.image_index)]),(TILE_SIZE,TILE_SIZE))

    def action(self,player):
        if self.used:
            self.collide = False
            player.show = False
        else:
            self.collide = True
            player.show = True
        if BPYG.while_key_hold(K_KP_ENTER) or BPYG.while_key_hold(KSCAN_KP_ENTER) or pyg.mouse.get_pressed(3)[2] and player.rect.colliderect(self.hitbox): 
            self.used = not self.used
            self.check_used()
            if self.used:
                player.rect.center = self.rect.center
                player.canMove = False
                self.groups()[0].background.setTimePass(15)
            else:
                player.canMove = True
                self.groups()[0].background.setTimePass(30)
            pyg.time.delay(250)
   
    def update(self,x_shift):
        player = self.groups()[0].player
        if self.hitbox.colliderect(player.rect):
            self.action(player)
        return super().update(x_shift)

    def draw(self,surface):
        self.hitbox = BPYG.draw_rect2(self.rect.center,(TILE_SIZE*3,TILE_SIZE*3),(0,0,0),0)
        return super().draw(surface)
    
class Sign(Tile):
    def __init__(self, Pos, Size, text="A Sign",style=0):
        super().__init__(Pos, Size, None)
        self.import_assets()
        self.text = text
        self.open = False
        self.collide = False
        self.style = style
        self.type = 'action'
        self.image = pyg.transform.scale(self.images[self.style],(TILE_SIZE,TILE_SIZE))
        self.hitbox = BPYG.draw_rect2(self.rect.center,(TILE_SIZE*2,TILE_SIZE*2),(0,0,0),0)

    def import_assets(self):
        s=  spritesheet(TEXTURES_FOLDER+'sign.png')
        self.images =s.images_at(((0,0,32,32),(32,0,32,32)),0)

    def action(self,player):
        if (BPYG.while_key_hold(K_KP_ENTER) or BPYG.while_key_hold(KSCAN_KP_ENTER)) or pyg.mouse.get_pressed(3)[2]:
            self.open = not self.open
            pyg.time.delay(100)

    def update(self, x_shift):
        player = self.groups()[0].player
        if self.hitbox.colliderect(player.rect):
            self.action(player)
        else:
            self.open = False

        if self.open:
            BPYG.draw_text(self.text,(HALF_SCREEN_WIDTH-350,HALF_SCREEN_HEIGHT-250),5, True, C_WHITE,C_NAVY)
        return super().update(x_shift)

    def draw(self, surface):
        self.hitbox = BPYG.draw_rect2(self.rect.center,(TILE_SIZE*2,TILE_SIZE*2),(0,0,0),0)
        return super().draw(surface)
