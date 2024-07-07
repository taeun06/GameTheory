import pygame as pg
import numpy as np
from abc import *

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)

pg.init()
pg.font.init()
screen_size = np.array((1366,768))
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Simulation Screen")

DEFAULT_FONT  = pg.font.SysFont('nanumsquareregular',20,False,False)
DEFAULT_COLOR = BLACK
BG_COLOR      = WHITE
ANTIALIAS     = True
SHOW_FPS      = True

sprite_list = []
Board = None
Title = None
fpsBox = None

""" class Box():

    def __init__(self ,rect:pg.Rect ,color = DEFAULT_COLOR ,width = 3):
        self.rect  = pg.Rect(rect)
        self.color = color
        self.width = width

        self.SubBox_list = []

    def add_Box(self,box):
        self.SubBox_list.append(box)

    def draw(self):
        pg.draw.rect(screen,self.color,self.rect,self.width)
        flattened = np.array(self.SubBox_list).flatten()
        for SubBox in flattened:
            SubBox.draw() """
    
""" class TextBox():

    def __init__(self ,text ,font = DEFAULT_FONT ,color = DEFAULT_COLOR ,center = None
                ,topleft = None ,topright = None ,bottomleft = None ,bottomright = None):
        self.text  = text
        self.font  = font
        self.color = color
        self.image = self.font.render(self.text,ANTIALIAS,self.color)
        self.rect  = self.image.get_rect()
        if   center      is not None: self.rect.center      = center
        elif topleft     is not None: self.rect.topleft     = topleft
        elif topright    is not None: self.rect.topright    = topright
        elif bottomleft  is not None: self.rect.bottomleft  = bottomleft
        elif bottomright is not None: self.rect.bottomright = bottomright
        else: raise ValueError("no position information given in TextBox object")
    
    def draw(self):
        screen.blit(self.image,self.rect.topleft) """

""" class Button():

    def __init__(self ,rect:pg.rect ,text:str ,font = DEFAULT_FONT ,color:tuple = DEFAULT_COLOR):
        self.rect:pg.Rect = rect
        self.text:str     = text
        self.font         = font
        self.color:tuple  = color
        self.image = self.font.render(self.text,ANTIALIAS,self.color)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw(self):
        pg.draw.rect(screen,self.color,self.rect)
        screen.blit(self.image,self.image_rect.center)

    def is_clicked(self,pos:list):
        return self.rect.collidepoint(pos) """

""" def flip_screen():
    screen.fill(WHITE)
    for sprite in sprite_list:
        sprite.draw()
    pg.display.update()
 """
""" def update_screen(fps):
    global Board, Title, fpsBox
    if Board is None:
        print(Board)
        raise ValueError("Board is not initialized.")
    if SHOW_FPS is True:
        sprite_list.remove(fpsBox)
        fpsBox = TextBox(f"FPS:{int(fps)}",topleft=[0,0])
        sprite_list.append(fpsBox) """

def init(board_size:int,board_scale):     #삭제 예정. 나중에 메인 이벤트 루프에 풀어서 넣을 계획
    global Board, Title, fpsBox
    Board = Box([0,0,board_size,board_size])
    Board.rect.center = screen_size/2
    sprite_list.append(Board)

    section_size = board_size/board_scale
    for i in range(board_scale):
        line = []
        for j in range(board_scale):
            section = Box([0,0,section_size,section_size],width=1)
            section.rect.topleft = np.array([i,j])*section_size + Board.rect.topleft
            line.append(section)
        Board.SubBox_list.append(line)
    
    Title = TextBox("시뮬레이션 화면",center = [screen_size[0]/2,20])
    sprite_list.append(Title)

    if SHOW_FPS is True:
        fpsBox = TextBox("FPS:",topleft = [0,0])
        sprite_list.append(fpsBox)