# Import Libraries  Locals

from data.src.config import *
from data.src.player import Player
from data.src.groups import *
from data.src.tiles import *


# Import Libraries from PyPi
from sys import exit
import pygame as pyg
from pygame.locals import *



def main():
    tilesGroup = tiles()
    e = EndOfScreen(tilesGroup)

    plr = Player((0,0),tilesGroup)
    plr.EndOfScreen = e

    while True:
        for ev in pyg.event.get():
            if ev.type == QUIT:
                pyg.quit()
                exit()

        pyg.display.update()
        SCREEN.fill(C_WHITE)
        tilesGroup.draw()
        tilesGroup.update()
        PYG_CLOCK.tick(FPS)


main() # Run Game