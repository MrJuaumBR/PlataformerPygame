import pygame as pyg
from pygame.locals import *
from sys import exit
from data.src.settings import *
from data.src.tiles import *
from data.src.level import Level

GAME_RUNNING = True
DISCORD = threading.Thread(target=Setup_Discord,args=(lambda : GAME_RUNNING,))
GAME_RUNNING = False

def AllScreenDraw():
    BTN_exit = BPYG.draw_button('X',(SCREEN_WIDTH-24,5),0,((255,255,255),(200,50,50)))
    BPYG.draw_text(f"{int(CLOCK.get_fps())}",(SCREEN_WIDTH-24,32),1,False,((0,0,0)))

    return BTN_exit

def main():
    GAME_RUNNING = True
    
    DISCORD.start()
    while True:
        if AllScreenDraw(): # All Screen 
            GAME_RUNNING = False
            DISCORD.join()
            pyg.quit()
            exit()
        BPYG.draw_text(GAMETITLE,(HALF_SCREEN_SIZE[0]+100,HALF_SCREEN_SIZE[1]),2,True,(0,0,0))
        BTN_play = BPYG.draw_button('PLAY',(HALF_SCREEN_SIZE[0]-200,HALF_SCREEN_SIZE[1]-200),0,((0,0,0),(100,200,100)))
        BTN_options = BPYG.draw_button('OPTIONS',(HALF_SCREEN_SIZE[0]-200,HALF_SCREEN_SIZE[1]-150),0,((0,0,0),(100,100,200)))
        BTN_exit = BPYG.draw_button('EXIT',(HALF_SCREEN_SIZE[0]-200,HALF_SCREEN_SIZE[1]-100),0,((0,0,0),(200,100,100)))
        if BTN_play:
            game()
        if BTN_options:
            pass
        if BTN_exit:
            GAME_RUNNING = False
            DISCORD.join()
            pyg.quit()
            exit()

        for ev in pyg.event.get():
            if ev.type == QUIT:
                GAME_RUNNING = False
                DISCORD.join()
                pyg.quit()
                exit()
            elif ev.type == KEYDOWN:
                if ev.key == K_x:
                    GAME_RUNNING = False
        
        pyg.display.update()
        SCREEN.fill('white')
        CLOCK.tick(60)

def game():
    run = True
    menu_open = False

    level = Level(level_map,SCREEN)

    while run:
        if menu_open:
            BPYG.draw_rect((HALF_SCREEN_WIDTH+200,0),(HALF_SCREEN_WIDTH-200,SCREEN_HEIGHT),(100,100,100),190)
            BPYG.draw_text("PAUSED",(HALF_SCREEN_SIZE[0],HALF_SCREEN_HEIGHT-200),0,True,(0,0,0))
            level.player.sprite.locked = True
        else:
            level.player.sprite.locked = False
            
        if AllScreenDraw():
            run = False
        for ev in pyg.event.get():
            if ev.type == QUIT:
                GAME_RUNNING = False
                DISCORD.join()
                pyg.quit()
                exit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    menu_open = not menu_open

        pyg.display.update()
        CLOCK.tick(60)

        SCREEN.fill(C_LIGHTSKYBLUE)
        level.run()