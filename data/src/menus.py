import pygame as pyg
from pygame.locals import *
from sys import exit
from data.src.settings import *
from data.src.tiles import *
from data.src.level import Level
from data.src.player import savePlayer,PCursor
from data.src.groups import backgroundGroup,TilesGroup
from ast import literal_eval

Tiles_Dict = {
    "Null":{"call":"erase"},
    "Tile":{"call":Tile},
    "Spike":{"call":Spike},
    "Checkpoint":{"call":Checkpoint},
    "Door":{"call":Door},
    "SleepCapsule":{"call":sCapsule},
    "Sign":{"call":Sign}
}

GAME_RUNNING = True
DISCORD = threading.Thread(target=Setup_Discord,args=(lambda : GAME_RUNNING,))
GAME_RUNNING = False
FPS = 30

def AllScreenDraw():
    BTN_exit = BPYG.draw_button('X',(SCREEN_WIDTH-24,5),0,((255,255,255),(200,50,50)))
    BPYG.draw_text(f"{int(CLOCK.get_fps())}",(SCREEN_WIDTH-24,32),1,False,((0,0,0)))

    return BTN_exit

def main():
    global CURRENT_CONFIG, FPS
    GAME_RUNNING = True
    
    CURRENT_CONFIG = literal_eval(db.get(1,'config')[1])
    GAME_RUNNING = CURRENT_CONFIG['RPC']
    FPS = CURRENT_CONFIG['fps']

    pimg =pyg.transform.scale(spritesheet(TEXTURES_FOLDER+f"player_yellow.png").image_at((16,16,16,16),0),(TILE_SIZE*2,TILE_SIZE*2))
    if GAME_RUNNING and CURRENT_CONFIG['RPC']:
        DISCORD.start()
    while True:
        if AllScreenDraw(): # All Screen 
            if CURRENT_CONFIG['RPC']:
                DISCORD.join(0.3)
                GAME_RUNNING = False
            pyg.quit()
            exit()
        BPYG.draw_text(GAMETITLE,(HALF_SCREEN_SIZE[0]+100,HALF_SCREEN_SIZE[1]),2,True,(0,0,0))
        SCREEN.blit(pimg,Rect(HALF_SCREEN_SIZE[0]+100,HALF_SCREEN_SIZE[1]-(TILE_SIZE*2+10),TILE_SIZE*2,TILE_SIZE*2))
        BTN_play = BPYG.draw_button('PLAY',(HALF_SCREEN_SIZE[0]-200,HALF_SCREEN_SIZE[1]-200),0,((0,0,0),(100,200,100)))
        BTN_options = BPYG.draw_button('OPTIONS',(HALF_SCREEN_SIZE[0]-200,HALF_SCREEN_SIZE[1]-150),0,((0,0,0),(100,100,200)))
        BTN_exit = BPYG.draw_button('EXIT',(HALF_SCREEN_SIZE[0]-200,HALF_SCREEN_SIZE[1]-100),0,((0,0,0),(200,100,100)))
        if BTN_play:
            play_menu()
        if BTN_options:
            options()
            #db.update("config",1,CONFIG_TABLE_COLUMNS,)
            CURRENT_CONFIG['volume'] = sound_level/100
            CURRENT_CONFIG['RPC'] = discord_rpc
            CURRENT_CONFIG['fps'] = fps_v
            CURRENT_CONFIG['autosave'] = autosave
            FPS = fps_v
            BPYG.volume = CURRENT_CONFIG['volume']
            db.update('config',1,CONFIG_TABLE_COLUMNS, [CURRENT_CONFIG,])
        if BTN_exit:
            GAME_RUNNING = False
            DISCORD.join(0.3)
            pyg.quit()
            exit()

        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join(0.3)
                pyg.quit()
                exit()
        
        pyg.display.update()
        SCREEN.fill('white')
        CLOCK.tick(FPS)
    GAME_RUNNING = False
    DISCORD.join(0.3)
    pyg.quit()
    exit()

def options():
    global discord_rpc, sound_level,fps_v, autosave
    run = True
    list_discord_rpc = [True,False]
    index_discord_rpc = list_discord_rpc.index(CURRENT_CONFIG['RPC'])
    discord_rpc = list_discord_rpc[index_discord_rpc]

    list_sound_level = [0,25,50,75,100]
    index_sound_level = list_sound_level.index(int(CURRENT_CONFIG['volume']*100))
    sound_level = list_sound_level[index_sound_level]

    list_fps = [30,60,120]
    index_fps = list_fps.index(int(CURRENT_CONFIG['fps']))
    fps_v = list_fps[index_fps]

    list_autosave = [True,False]
    index_autosave = list_autosave.index(CURRENT_CONFIG['autosave'])
    autosave = list_autosave[index_autosave]

    list_debug = list_discord_rpc
    index_debug = 0
    debug_v = list_debug[index_debug]
    while run:
        discord_rpc = list_discord_rpc[index_discord_rpc]
        sound_level = list_sound_level[index_sound_level]
        fps_v = list_fps[index_fps]
        autosave = list_autosave[index_autosave]
        debug_v = list_debug[index_debug]
        if AllScreenDraw():
            run = False
        BPYG.draw_text("Options",(25,25),2,True,(0,0,0))
        
        BPYG.draw_text("Discord Rich Presence(Need a restart): ",(HALF_SCREEN_WIDTH-210,75),1,True,C_BLACK)
        index_discord_rpc=BPYG.draw_select((HALF_SCREEN_WIDTH-200,100),1,((0,0,0),C_BEIGE),list_discord_rpc,index_discord_rpc)

        BPYG.draw_text("Volume: ",(HALF_SCREEN_WIDTH-210,150),1,True,C_BLACK)
        index_sound_level = BPYG.draw_select((HALF_SCREEN_WIDTH-200,175),1,(C_BLACK,C_BEIGE),list_sound_level,index_sound_level)

        BPYG.draw_text('FPS: ', (HALF_SCREEN_WIDTH-210, 225), 1, True, C_BLACK)
        BPYG.draw_text('This affect how the time in game pass, see the time calc is 60 frames = 1 second, and this calc dont change.',(HALF_SCREEN_WIDTH-250,270),3,True,C_RED)
        index_fps = BPYG.draw_select((HALF_SCREEN_WIDTH-200,250),1,((0,0,0),C_BEIGE),list_fps,index_fps)

        BPYG.draw_text("Autosave: ",(HALF_SCREEN_WIDTH-210, 300), 1, True, C_BLACK)
        index_autosave = BPYG.draw_select((HALF_SCREEN_WIDTH-210, 325), 1,(C_BLACK,C_BEIGE),list_autosave,index_autosave)

        BPYG.draw_text('Debug(Soon): ',(HALF_SCREEN_WIDTH-210,375), 1, True, C_BLACK)
        index_debug = BPYG.draw_select((HALF_SCREEN_WIDTH-200,400),1,(C_BLACK,C_BEIGE),list_debug,index_debug)
        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join(0.3)
                pyg.quit()
                exit()

        pyg.display.update()
        CLOCK.tick(FPS)
        SCREEN.fill(C_WHITE)

def play_menu():
    run = True
    while run:
        if AllScreenDraw():
            run = False
        BPYG.draw_text("Select game mode:" ,(50,50),0,True,C_BLACK)
        BTN_play = BPYG.draw_button("Play: Normal Mode",(HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT-200),1,(C_BLACK,C_GREEN))
        BTN_level_create = BPYG.draw_button("Play: Level Create",(HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT-100),1,(C_BLACK,C_GREEN))
        if BTN_play:
            save_select()
        if BTN_level_create:
            level_create()
        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join()
                pyg.quit()
                exit()
        
        pyg.display.update()
        CLOCK.tick(FPS)
        SCREEN.fill(C_WHITE)   

def level_create():
    run = True
    cur_map = []
    for _ in range(11):
        cur_map.append([])
    cur = PCursor((0,0))
    Tiles = TilesGroup()
    while run:
        if AllScreenDraw():
            run = False
        if BPYG.while_key_hold(K_LALT) or BPYG.while_key_hold(K_RALT):
            BPYG.draw_rect((0,0),(300,SCREEN_HEIGHT),C_NAVY,100,3)
            pos = [TILE_SIZE//2,TILE_SIZE//2]
            blocks = []
            for i,item in enumerate(Tiles_Dict):
                name = Tiles_Dict[item]
                b = BPYG.draw_button(item,pos,1,(C_BLACK,C_LIGHTSKYBLUE))
                pos[0] += TILE_SIZE+5
                if i+1 in [3,6,9,12,15,18,21]:
                    pos[1] += TILE_SIZE+5
                    pos[0] = TILE_SIZE//2
                blocks.append((b,item))
            for bt in blocks:
                if bt[0]:
                    c = Tiles_Dict[bt[1]]['call']
                    if callable(c):
                        t = c(cur.rect.topleft,TILE_SIZE)
                        Tiles.add(t)
                    pyg.time.delay(50)


        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join()
                pyg.quit()
                exit()
        pyg.display.update()
        cur.update()
        Tiles.update(cur.shift)
        CLOCK.tick(FPS)
        SCREEN.fill(C_WHITE)
        cur.draw()
        Tiles.draw(SCREEN)

def save_select():
    run = True
    saves = db.get_all(SAVES_TABLE)
    selected = {"name":"Not Selected","size":"0kb"}
    while run:
        if AllScreenDraw():
            run = False
        img_btns = []
        xy = [10,100]
        save_repeat = 0
        for s in saves:
            save = [s[0],s[1]]
            save[1] = literal_eval(save[1])
            BPYG.draw_rect(xy,(TILE_SIZE*2,TILE_SIZE*2+50),C_CORNSILK,150)
            
            # Draw Image
            img = pyg.transform.scale((spritesheet(TEXTURES_FOLDER+'diskette.png').image_at((0,0,16,16),0)),(TILE_SIZE*2,TILE_SIZE*2))
            img_rect = Rect(xy[0],xy[1]+5,img.get_rect().width,img.get_rect().height)
            SCREEN.blit(img,img_rect)

            # Draw delete button
            delete_btn = BPYG.draw_button('Delete',(xy[0],xy[1]+TILE_SIZE*2+10),3,(C_BLACK,C_RED))
            # Info Display
            BPYG.draw_text(save[1]["name"],xy,1,True,C_BLACK)

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
                db.delete(img[1][0],SAVES_TABLE)
                saves = db.get_all(SAVES_TABLE)
            if img[0].collidepoint(pyg.mouse.get_pos()):
                if pyg.mouse.get_pressed(3)[0]:
                    selected = img[1][1]
        
        BTN_select = BPYG.draw_button(f'Select: {selected["name"]}',(HALF_SCREEN_WIDTH-300,HALF_SCREEN_HEIGHT+300),0,((0,0,0),C_GREEN))
        BTN_create = BPYG.draw_button(f'+ Create',(HALF_SCREEN_WIDTH -(200-BPYG.fonts[0].size(f'Select: {selected["name"]}')[0]), HALF_SCREEN_HEIGHT+300),0,(C_BLACK,C_GREEN))
        if BTN_select:
            if selected["name"] != "Not Selected":
                s1 = db.get(selected['name'],SAVES_TABLE)
                s = savePlayer(literal_eval(s1[1])['name'],literal_eval(s1[1])['color'],literal_eval(s1[2]))
                s.update2(literal_eval(s1[1]))
                game(s)
        if BTN_create:
            create,player = create_character()
            if create:
                db.insert(SAVES_TABLE,["id",]+SAVES_TABLE_COLUMNS,[player.name,f'{player.get()}',f'{player.map}',])
                saves = db.get_all(SAVES_TABLE)
        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join(0.3)
                pyg.quit()
                exit()

        pyg.display.update()
        SCREEN.fill('white')
        CLOCK.tick(FPS)

def create_character():
    global index_player_color
    run = True
    index_player_color = 0

    list_map = list(DEFAULTS_MAP.keys())
    index_map = 0
    cur_map = DEFAULTS_MAP[list_map[index_map]]

    player_name = ""
    textbox_player_name = False
    warn_frames = 0
    warn = ""
    while run:
        if AllScreenDraw():
            run = False
            return (False,None)
        cur_map = DEFAULTS_MAP[list_map[index_map]]
        pimg = spritesheet(TEXTURES_FOLDER+f'player_{PLAYER_COLORS[index_player_color]}.png').image_at((16,16,16,16),0)
        pimg = pyg.transform.scale(pimg,(TILE_SIZE*2,TILE_SIZE*2))
        SCREEN.blit(pimg,Rect(HALF_SCREEN_HEIGHT+200,HALF_SCREEN_HEIGHT,TILE_SIZE*2,TILE_SIZE*2))

        BPYG.draw_text(f"Color: {PLAYER_COLORS[index_player_color].upper()}",(HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT-200),0,True,(0,0,0))
        index_player_color = BPYG.draw_select((HALF_SCREEN_WIDTH-190,HALF_SCREEN_HEIGHT-175),0,(C_BLACK,C_BEIGE),PLAYER_COLORS,index_player_color)

        BPYG.draw_text("Character Name: ",(HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT-125),0,True)
        textbox_player_name,player_name= BPYG.draw_textbox(rect=(HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT-100),font=4,colors=(C_BLACK,C_CORNSILK,C_LIGHTCYAN),active=textbox_player_name,current_text=player_name,oBlacklisted=[K_SPACE])

        BPYG.draw_text("MAP: ", (HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT-50),0,True)
        index_map = BPYG.draw_select((HALF_SCREEN_WIDTH-190,HALF_SCREEN_HEIGHT-25),0,(C_BLACK,C_BEIGE),list_map,index_map)

        BTN_create = BPYG.draw_button("Create",(HALF_SCREEN_WIDTH-200,HALF_SCREEN_HEIGHT+300),0,(C_BLACK,C_GREEN))
        if len(warn) >0:
            warn_frames += 1
            BPYG.draw_text(warn,(SCREEN_WIDTH-300,75),1,True,C_WHITE,C_RED)
            if warn_frames == FPS*3:
                warn_frames = 0
                warn = ""
        if BTN_create:
            if db.get(player_name,SAVES_TABLE):
                warn = "Already Have a player with this name."
            else:
                s = savePlayer(player_name,PLAYER_COLORS[index_player_color],cur_map)
                s.maxHealth = basePlayer['stats']['maxhealth']
                s.health = basePlayer['stats']['health']
                return (True,s)
        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join(0.3)
                pyg.quit()
                exit()

        pyg.display.update()
        CLOCK.tick(FPS)
        SCREEN.fill(C_WHITE)

def game(player):
    run = True
    menu_open = False
    background = backgroundGroup()
    level = Level(player.map,SCREEN)
    
    player_dict = player.get()

    level.player.sprite.checkpoint = player_dict['checkpoint']
    level.player.sprite.current_color = player_dict['color']
    level.player.sprite.maxHealth = player_dict['stats']['maxhealth']
    level.player.sprite.health = player_dict['stats']['health']
    level.player.sprite.import_character_assets()

    background.hours = player_dict['time']['hour']
    background.minutes = player_dict['time']['minute']
    background.day = player_dict['time']['day']
    while run:
        if menu_open:
            BPYG.draw_rect((HALF_SCREEN_WIDTH+200,0),(HALF_SCREEN_WIDTH-200,SCREEN_HEIGHT),(100,100,100),190)
            BPYG.draw_text("PAUSED",(HALF_SCREEN_SIZE[0],HALF_SCREEN_HEIGHT-200),0,True,(0,0,0))

            BPYG.draw_text("Menu",(HALF_SCREEN_WIDTH+225,50),0,True,C_WHITE) # Menu Part
            BTN_resume = BPYG.draw_button("RESUME",(HALF_SCREEN_WIDTH+225,75),0,(C_WHITE,C_GREEN))
            if not CURRENT_CONFIG['autosave']:
                BTN_autosave = BPYG.draw_button('Save',(HALF_SCREEN_WIDTH+225,125),0,(C_WHITE,C_INDIGO))
            else:
                BTN_autosave = False
            BTN_exit1 = BPYG.draw_button("Exit to save selector",(HALF_SCREEN_WIDTH+225,175),0,(C_WHITE,C_RED))
            BTN_exit2 = BPYG.draw_button("Exit to window",(HALF_SCREEN_WIDTH+225, 225), 0, (C_WHITE,C_RED))

            BPYG.draw_text(background.getTime()+", Day: "+background.getDay(),(HALF_SCREEN_WIDTH+225,HALF_SCREEN_HEIGHT+100),0,True,C_WHITE)
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
            elif BTN_exit1:
                if CURRENT_CONFIG['autosave']:
                    player.update(level)
                    db.update(SAVES_TABLE,f"{player.get()['name']}",SAVES_TABLE_COLUMNS,[player.get(),])    
                run = False
            elif BTN_exit2:
                if CURRENT_CONFIG['autosave']:
                    player.update(level)
                    db.update(SAVES_TABLE,f"{player.get()['name']}",SAVES_TABLE_COLUMNS,[player.get(),])
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING =False
                    DISCORD.join(0.3)
                pyg.quit()
                exit()
            elif BTN_autosave and not CURRENT_CONFIG['autosave']:
                player.update(level)
                db.update(SAVES_TABLE,f"{player.get()['name']}",SAVES_TABLE_COLUMNS,[player.get(),])
        else:
            level.player.sprite.locked = False
        
        hbar_pos = [TILE_SIZE/2,SCREEN_HEIGHT-(TILE_SIZE+25)]
        for i in HANDBAR_KEYS:
            if i[0] == 1:
                size = (TILE_SIZE/2+5,TILE_SIZE/2+5)
                color = C_NAVY
            else:
                size = (TILE_SIZE/2,TILE_SIZE/2)
                color = C_INDIGO
            BPYG.draw_rect(hbar_pos,size,color,190)
            BPYG.draw_text(str(i[0]),hbar_pos,3,True,C_WHITE)
            hbar_pos[0] += size[0] + 5

        if AllScreenDraw():
            player.update(level)
            run = False
        for ev in pyg.event.get():
            if ev.type == QUIT:
                if CURRENT_CONFIG['autosave']:
                    player.update(level)
                    db.update(SAVES_TABLE,f"{player.get()['name']}",SAVES_TABLE_COLUMNS,[player.get(),])
                if CURRENT_CONFIG['RPC']:
                    GAME_RUNNING = False
                    DISCORD.join(0.3)
                pyg.quit()
                exit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    menu_open = not menu_open
                elif ev.key == K_l:
                    background.skipTime(hours=1)

        background.update(level.player.sprite.locked)
        pyg.display.update()
        CLOCK.tick(FPS)

        background.draw(SCREEN)
        level.run(background)
        for sprite in level.tiles.sprites():
            if level.player.sprite.debug:
                BPYG.draw_rect(sprite.rect.topleft,(TILE_SIZE,TILE_SIZE),C_BLACK,0,4)