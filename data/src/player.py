import pygame as pyg
from pygame.locals import *
from sys import exit
from .support import spritesheet
from .settings import *
from random import randint

class player(pyg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()

        self.current_color = "yellow"

        self.import_character_assets()

        self.frame_index = 0
        self.animation_speed = 0.15
        self.type = "Player"

        

        # Player Draw
        self.image = self.animations['idle'][self.frame_index]
        self.image = pyg.transform.scale(self.image,size=(64,64))
        self.rect = self.image.get_rect(topleft=pos)
        self.priority = 1000

        # Player Movement
        self.direction = pyg.math.Vector2(0,0)
        self.SPEED = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.locked = False

        # Player Status
        self.status = "idle"
        self.facing = "right"
        
        self.on_ground = False
        self.already_on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Life Control
        self.health = 100
        self.maxHealth = self.health
        self.heal_frame = 300 # 5 Second
        self.take_damage_frame = 30 # 0.5 second
        self.health_bar_width = int(self.health*3.5)
        if self.health_bar_width > 500: # Limiter to width
            self.health_bar_width = 500
        self.health_ratio = self.maxHealth / self.health_bar_width
        self.respawn_cooldown = 0# FPS * Seconds = 60 * 5.
        self.respawned = False

    def take_damage(self,damage):
        if self.health >0 and self.status != "dead" and self.take_damage_frame == 0:
            self.take_damage_frame = 30
            self.heal_frame = 300
            self.health -= damage
            self.direction.y = 5
            if self.facing == "right":
                a = -1
            elif self.facing == "left":
                a = 1
            self.direction.x = 5 * a
            if self.health <= 0:
                self.health = 0
                BPYG.play_sound(SOUNDS_FOLDER+'dead.wav',.45)
                self.status = "dead"   
                self.respawn_cooldown = 60 * 5
            else:
                BPYG.play_sound(SOUNDS_FOLDER+'hurt.wav',.3)
                
    def heal_damage(self,heal):
        if self.heal_frame <= 0 and self.status != "dead":
            self.health += heal
            self.heal_frame = 3
            if self.health >= self.maxHealth:
                self.health = self.maxHealth
                self.heal_frame = 300

    def heal_logic(self):
        if self.health > 0:
            if self.take_damage_frame > 0:
                self.take_damage_frame -= 1
        # Draws
        pyg.draw.rect(SCREEN,(200,75,75),(10,10,self.health/self.health_ratio,25))
        pyg.draw.rect(SCREEN,(255,255,255),(10,10,self.health_bar_width,25),4)
        if self.status == "dead":
            BPYG.draw_text("Dead X(",(25,12),1,True,(0,0,0))
        else:
            BPYG.draw_text(f"{int(self.health)}/{self.maxHealth}",(25,12),1,True,(0,0,0))
        
        if self.health < self.maxHealth:
            if self.heal_frame > 0 and self.status != "dead":
                self.heal_frame -= 1
            elif self.heal_frame == 0:
                self.heal_damage(self.maxHealth*0.025) # 0.25% per Second
        # Player Revive
        if self.status == "dead" and self.health <= 0 and self.respawn_cooldown > 0:
            BPYG.draw_text(f"You died, {int(self.respawn_cooldown//60)}s to respawn",(self.rect.centerx,self.rect.centery-125),0,True,C_RED)
            self.respawn_cooldown -= 1
            if self.respawn_cooldown <= 0:
                self.respawn_cooldown = 0
                self.status = "idle"
                self.locked = False
                self.health = self.maxHealth // 2
                self.respawned = True

    def animate(self):
        animation = self.animations[self.status]

        # loop
        self.frame_index +=self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index =0

        self.image = pyg.transform.scale(animation[int(self.frame_index)],(64,64)) # Resize Image

        if self.facing == "left": # Flip Image if to left
            self.image = pyg.transform.flip(self.image,True,False)

        if self.on_ground:
            if self.on_right:
                self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            elif self.on_left:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ceiling:
            if self.on_right:
                self.rect = self.image.get_rect(topright=self.rect.topright)
            elif self.on_left:
                self.rect = self.image.get_rect(topleft =self.rect.topleft)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def import_character_assets(self):
        character_path = f"./data/textures/player_{self.current_color}.png"
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'dead':[]}
        ss = spritesheet(character_path)
        self.animations['run'] = ss.images_at([(0,0,16,16),(16,0,16,16),(32,0,16,16)],0)
        self.animations['idle'] = (ss.image_at((16,16,16,16),0),)
        self.animations['jump'] = (ss.image_at((0,16,16,16),0),)
        self.animations['fall'] = (ss.image_at((32,16,16,16),0),)
        self.animations['dead'] = (ss.image_at((48,16,16,16),0),)

    def get_input(self):
        if self.status != "dead" and not self.locked:
            keys = pyg.key.get_pressed()
            if keys[K_RIGHT] or keys[K_d]:
                self.direction.x = 1
                self.facing = "right"
            elif keys[K_LEFT] or keys[K_a]:
                self.direction.x = -1
                self.facing = "left"
            else:
                self.direction.x = 0

            if (keys[K_SPACE] or keys[K_UP] or keys[K_w]) and self.on_ground:
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
                if self.health > 0:
                    self.status = "idle"
                else:
                    self.status = "dead"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if not self.health <= 0:
            self.direction.y = self.jump_speed

    def draw(self):
        SCREEN.blit(self.image,self.rect)

    def update(self):
        if not self.locked and self.health > 0:
            self.get_input()
            self.get_status()
            self.animate()
            self.heal_logic()
        elif self.health <= 0:
            self.animate()
            self.heal_logic()
            self.direction.x = 0
            self.direction.y = 0
            self.on_ground = False
            self.on_ceiling = False
            self.on_left = False
            self.on_right = False
            
        else:
            self.direction.x = 0
            self.direction.y = 0

class savePlayer():
    def __init__(self,name:str,color:tuple) -> None:
        self.color = color
        self.name = name

    def get(self):
        b = basePlayer
        b["name"] = self.name
        b["color"] = self.color
        return b