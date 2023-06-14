import pygame as pyg
from pygame.locals import *

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