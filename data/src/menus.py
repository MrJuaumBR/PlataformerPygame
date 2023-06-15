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
            save_select()
        if BTN_options:
            options()
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
        
        pyg.display.update()
        SCREEN.fill('white')
        CLOCK.tick(60)

def options():
    run = True
    list_discord_rpc = [True,False]
    index_discord_rpc = 0
    list_sound_level = [0,25,50,75,100]
    index_sound_level = 0
    while run:
        if AllScreenDraw():
            run = False
        BPYG.draw_text("Options",(25,25),2,True,(0,0,0))
        
        BPYG.draw_text("Discord Rich Presence: ",(HALF_SCREEN_WIDTH-210,75),1,True,C_BLACK)
        index_discord_rpc=BPYG.draw_select((HALF_SCREEN_WIDTH-200,100),1,((0,0,0),C_BEIGE),list_discord_rpc,index_discord_rpc)

        BPYG.draw_text("Volume: ",(HALF_SCREEN_WIDTH-210,150),1,True,C_BLACK)
        index_sound_level = BPYG.draw_select((HALF_SCREEN_WIDTH-200,175),1,(C_BLACK,C_BEIGE),list_sound_level,index_sound_level)
        for ev in pyg.event.get():
            if ev.type == QUIT:
                GAME_RUNNING = False
                DISCORD.join()
                pyg.quit()
                exit()

        pyg.display.update()
        CLOCK.tick(60)
        SCREEN.fill(C_WHITE)

def save_select():
    run = True
    saves = [{"name":"ProgrammerGuy",'size':'infinity'}]
    selected = {"name":"Not Selected","size":"0kb"}
    while run:
        if AllScreenDraw():
            run = False
        img_btns = []
        xy = [10,100]
        save_repeat = 0
        for save in saves:
            BPYG.draw_rect(xy,(TILE_SIZE*2,TILE_SIZE*2+50),C_CORNSILK,150)
            
            # Draw Image
            img = pyg.transform.scale((spritesheet(TEXTURES_FOLDER+'diskette.png').image_at((0,0,16,16),0)),(TILE_SIZE*2,TILE_SIZE*2))
            img_rect = Rect(xy[0],xy[1]+5,img.get_rect().width,img.get_rect().height)
            SCREEN.blit(img,img_rect)

            # Draw delete button
            delete_btn = BPYG.draw_button('Delete',(xy[0],xy[1]+TILE_SIZE*2+10),3,(C_BLACK,C_RED))
            # Info Display
            BPYG.draw_text(save["name"],xy,1,True,C_BLACK)

            img_btns.append((img_rect,save,delete_btn)) # Append to list
        
            # Position
            xy[0] += TILE_SIZE*2+10
            save_repeat += 1
            if save_repeat+1 >= int(SCREEN_WIDTH//(TILE_SIZE*2))-1:
                xy[1] += (TILE_SIZE * 2) + 60
                xy[0] = 10
                save_repeat = 0

        for img in img_btns:
            if img[2]:
                saves.pop(saves.index(img[1]))
            if img[0].collidepoint(pyg.mouse.get_pos()):
                if pyg.mouse.get_pressed(3)[0]:
                    selected = img[1]
        
        BTN_select = BPYG.draw_button(f'Select: {selected["name"]}',(HALF_SCREEN_WIDTH-300,HALF_SCREEN_HEIGHT+300),0,((0,0,0),C_GREEN))
        if BTN_select:
            game()

        for ev in pyg.event.get():
            if ev.type == QUIT:
                GAME_RUNNING = False
                DISCORD.join()
                pyg.quit()
                exit()

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

            BPYG.draw_text("Menu",(HALF_SCREEN_WIDTH+225,50),0,True,C_WHITE) # Menu Part
            BTN_resume = BPYG.draw_button("RESUME",(HALF_SCREEN_WIDTH+225,75),0,(C_WHITE,C_GREEN))

            BPYG.draw_text("Inventory",(HALF_SCREEN_WIDTH+225,HALF_SCREEN_HEIGHT+125),0,True,C_WHITE) # Inventory Part
            inv_block_pos = [HALF_SCREEN_WIDTH+ 225,HALF_SCREEN_HEIGHT+175]
            for i in range(5):
                for x in range(5):
                    BPYG.draw_rect(inv_block_pos,(TILE_SIZE/2,TILE_SIZE/2),C_BEIGE,200)
                    inv_block_pos[0] += TILE_SIZE/2+5
                inv_block_pos[1] += TILE_SIZE/2+5
                inv_block_pos[0] = HALF_SCREEN_WIDTH+225

            level.player.sprite.locked = True
            if BTN_resume:
                menu_open = False
                level.player.sprite.locked = False
        else:
            level.player.sprite.locked = False
        
        hbar_pos = [TILE_SIZE/2,SCREEN_HEIGHT-(TILE_SIZE+25)]
        for i in range(3):
            if i == 0:
                size = (TILE_SIZE/2+5,TILE_SIZE/2+5)
                color = C_NAVY
            else:
                size = (TILE_SIZE/2,TILE_SIZE/2)
                color = C_INDIGO
            BPYG.draw_rect(hbar_pos,size,color,190)
            BPYG.draw_text(str(i),hbar_pos,3,True,C_WHITE)
            hbar_pos[0] += size[0] + 5

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