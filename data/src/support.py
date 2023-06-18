import pygame as pyg
from pygame.locals import *
import sqlite3 as sql


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pyg.image.load(filename).convert()
        except pyg.error as message:
            print ('Unable to load spritesheet image:', filename)
            raise (SystemExit, message)
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pyg.Rect(rectangle)
        image = pyg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pyg.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class BetterPyGame():
    """
        A Simple Pygame assist plugin
    """
    def __init__(self,SCREEN):
        self.SCREEN = SCREEN
        self.fonts = []
        self.volume = 1
    
    def create_font(self, font_name='arial', font_size = 16, bold=False, italic=False) -> pyg.font:
        """
        Create a font
        font_name = Who font you will use(Font from your PC)
        font_size = Size in pixels of the font
        bold = Weight of font
        italic = a text decoration
        """
        f = pyg.font.SysFont(font_name,font_size,bold,italic)
        if f in self.fonts:
            raise(f"This font already exists in fonts list. font don't created, you can acess this in index: {self.fonts.index(f)}")
        else:
            self.fonts.append(f)
        return (self.fonts.index(f), f)
    
    def while_key_hold(self,key):
        keys = pyg.key.get_pressed()
        if keys[key]:
            return True
        else:
            return False

    def draw_text(self, text="A text",Pos=(0,0),font=0,antialias=False,color=(0,0,0), background_color=None) -> pyg.Surface:
        """
        Draw a text in SCREEN
        text = Your text
        Pos = Text position
        font = a font or you index in fonts list
        antialias = a variable to draw, if you want make a text more rounded set to True
        color = RGB Color (R,G,B)
        background_color = if equal None, don't have background, else RGB Color (R,G,B)
        """
        if type(font) == int:
            font = self.fonts[font]
        
    
        r = font.render(text,antialias,color,background_color)
        g = r.get_rect()
        g.topleft= Pos
        self.SCREEN.blit(r,g)
        return g

    def draw_button(self, text="A Button", Pos=(0,0),font=0,colors=((0,0,0),(255,255,255))) -> bool:
        """
        Draw a button in SCREEN and return a boolean
        text = button show text
        Pos = button position
        font = a font or you index in fonts list
        colors = (color 1= color of font, color 2= color of background)
        return a bool(True or False)
        """
        r = self.draw_text(text,Pos,font,False,colors[0],colors[1])
        if r.collidepoint(pyg.mouse.get_pos()):
            if pyg.mouse.get_pressed(3)[0]:
                pyg.time.wait(100)
                return True
            else:
                return False
        else:
            return False

    def draw_rect(self,Pos=(0,0), Size=(0,0), color=(0,0,0), alpha=None) -> Rect:
        """
        Draw a rectangle in screen and return it
        Pos = Position
        Size = Size of rectangle
        color = RGB Color (R,G,B)
        alpha = transparency (0 -> 255)
        """
        if alpha:
            s = pyg.Surface(Size)
            s.fill(color)
            s.set_alpha(alpha)
            r = s.get_rect(topleft=Pos)
            self.SCREEN.blit(s,r)
        else:
            r = pyg.draw.rect(self.SCREEN,color,Rect(Pos[0],Pos[1],Size[0],Size[1]))
        return r
    
    def draw_rect2(self,Pos=(0,0), Size=(0,0), color=(0,0,0), alpha=None) -> Rect:
        """
        Draw a rectangle in screen and return it
        Pos = Position
        Size = Size of rectangle
        color = RGB Color (R,G,B)
        alpha = transparency (0 -> 255)
        """
        if type(alpha) == int:
            s = pyg.Surface(Size,pyg.SRCALPHA)
            R,G,B = color
            color = (R,G,B,alpha)
            s.fill(color)
            r = s.get_rect(center=Pos)
            self.SCREEN.blit(s,r)
        else:
            r = Rect(Pos[0],Pos[1],Size[0],Size[1])
            r.center = Pos
            pyg.draw.rect(self.SCREEN,color,r)
        return r

    def draw_select(self,Pos=(0,0),font=0,colors=((0,0,0),(100,100,100)),options=[],current_option=0):
        if type(font) == int:
            font = self.fonts[font]
        cur = options[current_option]
        X_change = int(font.size(str(cur))[0]*1.25)+1
        self.draw_text(str(cur),(Pos[0]-(X_change/4),Pos[1]),font,True,colors[0],colors[1])
        Back = self.draw_button("<",(Pos[0]-X_change,Pos[1]),font,colors) # Back
        Next = self.draw_button(">",(Pos[0]+X_change, Pos[1]), font, colors) # Next
        if Back:
            current_option -= 1
            if current_option<0:
                current_option = len(options)-1
        elif Next:
            current_option += 1
            if current_option>len(options)-1:
                current_option = 0
        return current_option

    def draw_textbox(self,rect=(0,0),colors=((0,0,0),(100,100,100),(100,100,200)),font=0,active=False,current_text="",oBlacklisted=[]):
        """
        rect = Rectangle(X,Y,W,H)
        colors = 3 Colors in RGB ((1th is text color),(2nd is textbox bg when not active),(3rd is textbox bg when active))
        font= font to render
        active = Bool to check if it active to edit
        current_text= is the current text, make it to "" in start.
        oBlacklisted = Key blacklisted(will be add to a list)
        """
        blacklist = [K_RETURN,K_ESCAPE,K_TAB,K_DELETE,K_BACKSPACE]
        for b in oBlacklisted:
            if not b in blacklist:
                blacklist.append(b)

        width = 0
        if type(font) == int:
            font = self.fonts[font]
        if len(str(current_text)) == 0:
            my_text = "                         "
        else:
            my_text = current_text
        if len(str(current_text)) > 1:
            width += int(font.size(str(current_text))[0] * 1.1)
        if active:
            bg_c = 2
        else:
            bg_c = 1
        box2 =self.draw_text(str(my_text),(rect[0],rect[1]),font,True,colors[0],colors[bg_c])
        if pyg.mouse.get_pressed(3)[0]:
            if box2.collidepoint(pyg.mouse.get_pos()):
                active = True
            else:
                active = False
        else:
            if not active:
                active = False
        if active:
            if not width >= (self.SCREEN.get_size()[0]*2):
                if self.while_key_hold(K_BACKSPACE):
                    current_text = current_text[:-1]
                    pyg.time.delay(100)
                for ev in pyg.event.get():
                    if ev.type == KEYDOWN:
                        if not ev.key in blacklist:
                            current_text += ev.unicode
        return (active,current_text)

    def set_volume(self,volume=1):
        """
        Set All sounds and musics volume
        """
        self.volume = volume

    def play_sound(self,file,individual_volume=None):
        """
        Play a sound file(.wav)
        """
        if not individual_volume:
            individual_volume = self.volume
        s = pyg.mixer.Sound(file)
        s.set_volume(individual_volume)
        s.play()

    def set_color(self, surface,color):
        """Fill all pixels of the surface with color, preserve transparency."""
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pyg.Color(r, g, b, a))

class DataBase():
    def __init__(self,database='/database.db',autocommit=True):
        self.db_path = database
        self.autocommit = autocommit
        self.setup_database()

    def to_(self,values:list) -> str:
        val = ""
        for i,value in enumerate(values):
            if value == values[-1]:
                v = f""" "{value}" """
            else:
                v = f""" "{value}", """
            val += v
        return val
    
    def co_(self,columns:list) -> str:
        val = ""
        for i,value in enumerate(columns):
            if value == columns[-1]:
                v = value
            else:
                v = value+", "
            val += v
        return val

    def jo_(self,columns:list,values:list) -> str:
        val = ""
        for i,value in enumerate(values):
            if value == values[-1]:
                v = columns[i] + f"""="{value}" """
            else:
                v = columns[i] + f"""="{value}", """
            val += v
        return val

    def ac(self):
        if self.autocommit:
            self.db.commit()

    def setup_database(self):
        """
        Setup the basic of database
        """
        self.db = sql.connect(self.db_path)
        self.cur = self.db.cursor()
        self.db.commit()

    def create_table(self,name:str,values:list):
        """
        Create a table if not exists
        name = Table Name
        valies = List of Values Name & Types ["name TEXT","value INTEGER"] ...
        """
        val = self.co_(values)
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {name} ({val})""")
        self.ac()

    def get(self,id,table:str):
        if type(id) == str:
            id = f'{id}'
        return self.cur.execute(f"""
        SELECT * FROM {table} WHERE id=?
        """,(id,)).fetchone()
    
    def get_all(self,table:str):
        return self.cur.execute(f"""
                                SELECT * FROM {table}
                                """).fetchall()

    def insert(self,table:str,columns:list,values:list):
        values = self.to_(values)
        columns = self.co_(columns)
        self.cur.execute(f"""INSERT INTO {table} ({columns}) VALUES({values})""")
        self.ac()

    def update(self,table:str,id:int,columns:list,values:list):
        val = self.jo_(columns,values)
        self.cur.execute(f"""
        UPDATE {table} SET {val} WHERE id=?
        """, (id,))
        self.ac()

    def delete(self,id,table:str):
        if self.get(id,table):
            self.cur.execute(f"""
                DELETE FROM {table} WHERE id=?
            """,(id,))
            self.ac()