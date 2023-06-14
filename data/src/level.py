import pygame as pyg
from pygame.locals import *
from sys import exit
from .tiles import *
from .player import player
from .settings import *
from .groups import TilesGroup

class Level:
    def __init__(self,level_data,surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        self.world_spawn = (0,0)

    def setup_level(self,layout):
        self.tiles = TilesGroup()
        self.player = pyg.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == '1':
                    tile = Tile((x,y),TILE_SIZE)
                    self.tiles.add(tile)
                elif cell == '0':
                    self.world_spawn = (x,y)
                    player_sprite = player((x,y))
                    self.player.add(player_sprite)
                elif cell == '3':
                    tile = SpiekBall((x,y),TILE_SIZE)
                    self.tiles.add(tile)
        
        self.tiles.add(DeadPoint((HALF_SCREEN_WIDTH-30,SCREEN_HEIGHT+50),(SCREEN_WIDTH+60,15))) # Dead Point

    def check_take_damage(self,player,sprite):
        if sprite.type == "Damage":
            player.take_damage(sprite.damage)

    def scroll_x(self):
        player = self.player.sprite

        player_x = player.rect.centerx
        directionx = player.direction.x

        if player_x < SCREEN_WIDTH//4 and directionx < 0:
            self.world_shift = 8
            player.SPEED = 0
        elif player_x > SCREEN_WIDTH-(SCREEN_WIDTH//4) and directionx > 0:
            self.world_shift = -8
            player.SPEED = 0
        else:
            self.world_shift = 0
            player.SPEED = 8

    def horizontal_movement_collision(self):
        player= self.player.sprite

        player.rect.x += player.direction.x * player.SPEED
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x <0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                    self.check_take_damage(player,sprite)
                elif player.direction.x >0:
                    player.rect.right = sprite.rect.left
                    player.on_right =True
                    self.current_x = player.rect.right
                    self.check_take_damage(player,sprite)
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and(player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        if not player.locked:
            player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    if not player.already_on_ground:
                        BPYG.play_sound(SOUNDS_FOLDER+'fall.wav',.45)
                        player.already_on_ground = True
                    self.check_take_damage(player,sprite)
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    self.check_take_damage(player,sprite)

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
            player.already_on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.player.draw(self.display_surface)