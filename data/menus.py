"""IF YOU DON'T KNOW WHAT YOU MAKING, DON'T CHANGE NOTHING."""

# Import Libraries  Locals

from data.src.config import *
from data.src.player import Player
from data.src.groups import *
from data.src.tiles import *


# Import Libraries from PyPi
import pygame as pyg
from pygame.locals import *

# Import Python libraries
from sys import exit
from random import randint

pyg.init()

def game():
    run = True

    tilesGroup = tiles()
    e = EndOfScreen(tilesGroup)

    plr = Player((0,0),tilesGroup)
    plr.EndOfScreen = e
    
    for i in range(randint(15,40)):
        plataform((randint(0,SC_WIDTH),randint(0,SC_HEIGHT)),(randint(16,32),randint(16,32)),tilesGroup)
    tilesGroup.player = plr
    while run:
        # Draw
        PPE.draw_text(f"{CLS_WORLD.Time}:00, {CLS_WORLD.Day}/{CLS_WORLD.Month}/{CLS_WORLD.Year}",XY=(SC_WIDTH-100,10),font=1) # Time Draw
        PPE.draw_text(f"{int(PYG_CLOCK.get_fps())}",XY=(SC_WIDTH-100,25)) # FPS Show
        

        for ev in pyg.event.get():
            if ev.type == QUIT:
                pyg.quit()
                exit()

        # Update
        pyg.display.update()
        SCREEN.fill(C_WHITE)
        tilesGroup.draw()
        tilesGroup.update()
        CLS_WORLD.update()
        PYG_CLOCK.tick(FPS)

def main():
    while True:
        PPE.draw_text(GAMETITLE+str(VERSION),XY=SC_HALF_SIZE)
        Btn_play = PPE.draw_button("PLAY",(SC_HALF_SIZE[0]-250,300),0,((0,0,0),C_GRAY))
        Btn_option = PPE.draw_button("OPTIONS",(SC_HALF_SIZE[0]-250,350),0,((0,0,0),C_GRAY))
        Btn_exit = PPE.draw_button("EXIT",(SC_HALF_SIZE[0]-250,400),0,((0,0,0),C_RED))
        if Btn_play:
            game()
        
        if Btn_option:
            print('Cooming Soon!')

        if Btn_exit:
            pyg.quit()
            exit()

        for ev in pyg.event.get():
            if ev.type == QUIT:
                pyg.quit()
                exit()
        
        pyg.display.update()
        SCREEN.fill(C_WHITE)
        PYG_CLOCK.tick(FPS)