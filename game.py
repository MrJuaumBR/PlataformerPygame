import pygame as pyg
from pygame.locals import *
from sys import exit
from data.src.settings import *
from data.src.tiles import *
from data.src.level import Level

# Pygame Setup
pyg.init()
screen = pyg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),FULLSCREEN)
clock = pyg.time.Clock()

level = Level(level_map,screen)

while True:
    for event in pyg.event.get():
        if event.type == QUIT:
            pyg.quit()
            exit()

    screen.fill('black')
    level.run()

    pyg.display.update()
    clock.tick(60)
