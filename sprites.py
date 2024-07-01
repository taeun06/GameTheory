import pygame as pg
import numpy as np
from abc import *

pg.init()
screen_size = np.array((1366,768))
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Simulation Screen")

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)

DEFAULT_FONT  = pg.font.SysFont('nanumsquareregular',20,False,False)
DEFAULT_COLOR = BLACK
BG_COLOR      = WHITE
ANTIALIAS     = True

sprite_list = []

class Box():

    def __init__(self ,rect:pg.Rect ,color = DEFAULT_COLOR ,width = 3):
        self.rect  = pg.Rect(rect)
        self.color = color
        self.width = width

        self.SubBox_list = []

    def add_Box(self,box):
        self.SubBox_list.append(box)
    
class TextBox():

    def __init__(self,center,text,font = DEFAULT_FONT,color = DEFAULT_COLOR):
        self.text  = text
        self.font  = font
        self.color = color
        self.txt   = self.font.render(self.text,ANTIALIAS,self.color)
        self.rect  = self.txt.get_rect()
        self.rect.center = center

class Button():

    def __init__(self ,rect:pg.rect ,text ,color = DEFAULT_COLOR):
        self.rect  = rect
        self.text  = text
        self.color = color

    def is_clicked(self,pos:list):
        return self.rect.collidepoint(pos)

def init(board_size:int,board_scale):
    Board = Box([0,0,board_size,board_size])
    Board.rect.center = screen_size/2
    sprite_list.append(Board)

    section_size = board_size/board_scale
    for i in range(board_scale):
        line = []
        for j in range(board_scale):
            section = Box([0,0,section_size,section_size])
            section.rect.topleft = np.array([i,j])*section_size
            line.append(section)
        Board.SubBox_list.append(line)
    
    Title = TextBox([screen_size[0]/2,20],"시뮬레이션 화면")
    sprite_list.append(Title)