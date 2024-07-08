import pygame as pg
import numpy as np
from abc import *

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)

pg.init()
SCREEN_SIZE = np.array((1366,768))
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Simulation Screen")

DEFAULT_FONT  = pg.font.SysFont('nanumsquareregular',20,False,False)
DEFAULT_COLOR = BLACK
BG_COLOR      = WHITE
ANTIALIAS     = True

# 이후 표시상의 편의를 위해 임의로 지정한 상수
# 스프라이트의 anchor 속성에 이용됨
CENTER      = 0
TOPLEFT     = 1
TOPRIGHT    = 2
BOTTOMLEFT  = 3
BOTTOMRIGHT = 4

def flip_screen():
    pg.display.flip()

class Rectangle(pg.sprite.Sprite):
    # - 내부가 채워진 사각형을 나타내는 스프라이트 클래스
    # - 직사각형 객체가 가지는 속성
    #    1.직사각형을 나타내는 이미지 - image
    #    2.직사각형의 위치, 크기를 나타내는 pygame.Rect 객체 - rect
    #    참고)이외의 init 함수에 들어가는 값들은 위치를 편리하게 정하기 위한 수단
    #         center, topleft, topright, bottomleft, bottomright 중 하나의 값만 넣어야 함 (그렇지 않으면 기대한 대로 작동하지 않음)
    # - 직사각형 객체가 가지는 메서드
    #    1.스프라이트를 화면에 그리는 함수 - draw(self)
    #    2.스프라이트의 속성이 바뀔 시 그에 맞게 image 속성을 재로딩하는 함수 - update(self)
    def __init__(self ,size:tuple ,color:tuple = DEFAULT_COLOR
                ,center = None ,topleft = None ,topright = None ,bottomleft = None ,bottomright = None):
        super().__init__()
        self.color = color
        self.image = pg.Surface(size)
        self.image.fill(self.color)
        self.rect  = self.image.get_rect()
        if   center      is not None: self.rect.center      = center
        elif topleft     is not None: self.rect.topleft     = topleft
        elif topright    is not None: self.rect.topright    = topright
        elif bottomleft  is not None: self.rect.bottomleft  = bottomleft
        elif bottomright is not None: self.rect.bottomright = bottomright
        else: raise ValueError("no position information given in Rectangle object")

    def draw(self):
        screen.blit(self.image,self.rect.topleft)

    def update(self):
        self.image = pg.Surface(self.rect.size)
        self.image.fill(self.color)

class TextBox(pg.sprite.Sprite):
    # - 텍스트가 들어간 스프라이트를 나타내는 스프라이트 클래스
    # - 텍스트박스 객체가 가지는 속성
    #    1.텍스트박스의 텍스트 색 - color : tuple
    #    2.텍스트박스에 들어갈 텍스트 - text :str
    #    3.텍스트박스에 들어갈 폰트 - font
    #    4.텍스트박스의 위치, 크기를 나타내는 pygame.Rect 객체 - rect
    #    5.update 함수 호출 시 위치가 고정되는 기준을 나타내는 속성 - anchor (int에 해당하기는 하나 정수로서의 의미가 없음)
    # - 플레이어 객체가 가지는 메서드
    #    1.스프라이트를 화면에 그리는 함수 - draw(self)
    #    2.스프라이트의 속성이 바뀔 시 그에 맞게 image 속성을 재로딩하는 함수 - update(self)
    def __init__(self ,text:str ,font = DEFAULT_FONT ,color:tuple = DEFAULT_COLOR
                ,center = None ,topleft = None ,topright = None ,bottomleft = None ,bottomright = None
                ,anchor = CENTER):
        super().__init__()
        self.text  = text
        self.font  = font
        self.color = color
        self.image = self.font.render(self.text,ANTIALIAS,self.color)
        self.rect  = self.image.get_rect()
        self.anchor = anchor
        if   center      is not None: self.rect.center      = center      ; self.anchorpos = center
        elif topleft     is not None: self.rect.topleft     = topleft     ; self.anchorpos = topleft
        elif topright    is not None: self.rect.topright    = topright    ; self.anchorpos = topright
        elif bottomleft  is not None: self.rect.bottomleft  = bottomleft  ; self.anchorpos = bottomleft
        elif bottomright is not None: self.rect.bottomright = bottomright ; self.anchorpos = bottomright
        else: raise ValueError("no position information given in TextBox object")
    
    def draw(self):
        screen.blit(self.image,self.rect.topleft)

    def update(self):
        self.image = self.font.render(self.text,ANTIALIAS,self.color)
        self.rect.size = self.image.get_rect().size
        if   self.anchor == CENTER      : self.rect.center      = self.anchorpos
        elif self.anchor == TOPLEFT     : self.rect.topleft     = self.anchorpos
        elif self.anchor == TOPRIGHT    : self.rect.topright    = self.anchorpos
        elif self.anchor == BOTTOMLEFT  : self.rect.bottomleft  = self.anchorpos
        elif self.anchor == BOTTOMRIGHT : self.rect.bottomright = self.anchorpos

class Button(pg.sprite.Sprite):
    # - 클릭을 감지하는 버튼을 나타내는 스프라이트 클래스
    # - 버튼 객체가 가지는 속성
    #    1.버튼의 텍스트 색 - color : tuple
    #    2.버튼에 들어갈 텍스트 - text :str
    #    3.버튼에 들어갈 폰트 - font
    #    4.버튼의 위치, 크기를 나타내는 pygame.Rect 객체 - rect
    #    5.update 함수 호출 시 위치가 고정되는 기준을 나타내는 속성 - anchor (int에 해당하기는 하나 정수로서의 의미가 없음)
    # - 버튼 객체가 가지는 메서드
    #    1.스프라이트를 화면에 그리는 함수 - draw(self)
    #    2.스프라이트의 속성이 바뀔 시 그에 맞게 image 속성을 재로딩하는 함수 - update(self)
    def __init__(self ,text:str ,font = DEFAULT_FONT ,color:tuple = None
                ,center = None ,topleft = None ,topright = None ,bottomleft = None ,bottomright = None
                ,anchor = CENTER):
        super().__init__()
        self.text  = text
        self.font  = font
        self.color = color
        self.image = self.font.render(self.text,ANTIALIAS,self.color)
        self.rect  = self.image.get_rect()
        self.anchor = anchor
        if   center      is not None: self.rect.center      = center      ; self.anchorpos = center
        elif topleft     is not None: self.rect.topleft     = topleft     ; self.anchorpos = topleft
        elif topright    is not None: self.rect.topright    = topright    ; self.anchorpos = topright
        elif bottomleft  is not None: self.rect.bottomleft  = bottomleft  ; self.anchorpos = bottomleft
        elif bottomright is not None: self.rect.bottomright = bottomright ; self.anchorpos = bottomright
        else: raise ValueError("no position information given in TextBox object")

    def draw(self):
        if self.color is not None:
            frame = pg.Surface(self.rect.size)
            frame.fill(self.color)
            screen.blit(frame,self.rect.topleft)

        screen.blit(self.image,self.rect.center)

    def update(self):
        self.image = self.font.render(self.text,ANTIALIAS,self.color)
        self.rect.size = self.image.get_rect().size
        if   self.anchor == CENTER      : self.rect.center      = self.anchorpos
        elif self.anchor == TOPLEFT     : self.rect.topleft     = self.anchorpos
        elif self.anchor == TOPRIGHT    : self.rect.topright    = self.anchorpos
        elif self.anchor == BOTTOMLEFT  : self.rect.bottomleft  = self.anchorpos
        elif self.anchor == BOTTOMRIGHT : self.rect.bottomright = self.anchorpos

    def is_clicked(self,pos:list) -> bool:
        return self.rect.collidepoint(pos)