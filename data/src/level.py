import pygame as pyg
from pygame.locals import *
from sys import exit
from .tiles import Tile
from .player import player
from .settings import TILE_SIZE,SCREEN_WIDTH

class Level:
    def __init__(self,level_data,surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self,layout):
        self.tiles = pyg.sprite.Group()
        self.player = pyg.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    tile = Tile((x,y),TILE_SIZE)
                    self.tiles.add(tile)
                elif cell == 'P':
                    
                    player_sprite = player((x,y))
                    self.player.add(player_sprite)

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
                elif player.direction.x >0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        
        self.player.update()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.player.draw(self.display_surface)
        self.scroll_x()