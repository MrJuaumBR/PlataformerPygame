import pygame as pyg
from pygame.locals import *
from .config import *

class Player(pyg.sprite.Sprite):
    def __init__(self,XY,groups):
        super().__init__(groups)

        # Only if need reset rect
        self.StartPos = XY
        self.size = (32,64)

        # How Sprite is shown in game
        self.color = C_BLACK

        # Real Sprite
        self.rect = Rect(self.StartPos[0],self.StartPos[1],self.size[0],self.size[1])

        # Logic vars
        self.EndOfScreen = None

        # Movement
        self.speed = 5
        self.lastSide = "Left"
        self.Mov = [0,0]
        self.JumpFramesCount = 0
        self.JumpCountdown = False

    def jump(self):
        """Jump Action"""
        if not self.JumpCountdown:
            if self.Mov[1] > 0: 
                self.Mov[1] = 0 # Set Mov to 0 if > 0

            self.Mov[1] -= JUMP_FORCE

            if self.rect.y -self.Mov[1] < 0:
                self.Mov[1] = 0 # Reset if < 0

        self.JumpCountdown = True

    def control(self):
        """Player Control Logic"""
        keys = pyg.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]: # Left
            self.lastSide = "Left"
            self.Mov[0] -= self.speed
        elif keys[K_RIGHT] or keys[K_d]: # Right
            self.lastSide = "Right"
            self.Mov[0] += self.speed
        else:
            self.Mov[0] *= 0.3

        CheckTouch = self.rect.colliderect(self.EndOfScreen.rect)
        if (keys[K_UP] or keys[K_w] or keys[K_SPACE]) and CheckTouch: # Jump
            self.jump()
        else:
            self.Mov[0] *= 0.2

        # Control Limits
        if self.lastSide=="Left":
            if self.rect.x-self.Mov[0] < 0:
                self.Mov[0] = self.Mov[0]-self.rect.x
        elif self.lastSide == "Right":
            if self.rect.x+self.Mov[0] > SC_WIDTH:
                self.Mov[0] = SC_WIDTH-self.rect.x
        
        if self.rect.x > SC_WIDTH:
            self.rect.x = SC_WIDTH-self.size[0]
            self.Mov[0] = 0
        if self.rect.x <0:
            self.rect.x = self.size[0]
            self.Mov[0] = 0
        if self.rect.y <0:
            self.rect.y = self.size[1]
            self.Mov[1] = 0
        if self.rect.y > SC_HEIGHT:
            self.rect.y = SC_HEIGHT-self.size[1]*2
            self.Mov[1] = 0

    def gravity(self):
        """Gravity Control"""
        if not self.JumpCountdown:
            
            self.Mov[1] += GRAVITY_FORCE # Player Fall
            """if self.rect.y > SC_HEIGHT:
                self.Mov[1] -= self.size[1]"""
        else:
            self.Mov[1] += GRAVITY_FORCE * 0.3 # 30% of Force
        if self.rect.colliderect(self.EndOfScreen.rect):
            self.Mov[1] = 0
            self.rect.y = self.EndOfScreen.rect.top-(self.size[1]-2)


    def draw(self):
        """Draw Player Object"""
        pyg.draw.rect(SCREEN,self.color,self.rect)

    def update(self):
        """Update Player"""
        self.gravity()
        self.control()
        if self.JumpCountdown:
            self.JumpFramesCount+=1
            if self.JumpFramesCount >= JUMP_FRAMES_WAIT:
                self.JumpCountdown = False
                self.JumpFramesCount = 0
        self.rect.x += self.Mov[0]
        self.rect.y += self.Mov[1]
        