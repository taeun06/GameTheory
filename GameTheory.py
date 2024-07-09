import pygame as pg
import numpy as np
import sprites as spr
from math import *
import random

def always_recover(self): #R type
    self.turn = True

def always_destroy(self): #D type
    self.turn = False

def maintain_score(self): #MS type
    if self.score > MAINTAIN_LEVEL_SCO: self.turn = True
    else:                               self.turn = False

def maintain_env(self): #ME type
    if self.environment < MAINTAIN_LEVEL_ENV: self.turn = True
    else:                                     self.turn = False

def alter_action(self): #A type
    self.turn = ~ self.turn

def maintain_proportional(self): #MP type
    if self.environment * MAINTAIN_LEVEL_RATIO < self.score: self.turn = True
    else:                                                    self.turn = False

def get_dist(v1:list ,v2:list) -> float:
    v1:np.ndarray = np.array(v1)
    v2:np.ndarray = np.array(v2)
    return np.sqrt((v1-v2) @ (v1-v2))

def score_to_color(self):
    sco = self.score
    env = self.environment

    if sco <= 0:
        self.section.color = [255,255,255]
        return 0

    self.section.color = [255 / exp(sco / START_SCORE),255 / exp(sco / START_SCORE),255 / exp(sco / START_SCORE)]
    if env > 0: self.section.color[2] += (255 - 255 / exp(sco / START_SCORE)) * tanh(env)
    else      : self.section.color[0] += (255 - 255 / exp(sco / START_SCORE)) * tanh(-env)
    for index, value in enumerate(self.section.color):
        self.section.color[index] = round(value)

BOARD_RECT = pg.Rect(0,0,0,0)
BOARD_RECT.size = (700,700)
BOARD_RECT.center = spr.SCREEN_SIZE/2

MAINTAIN_LEVEL_SCO = 80
MAINTAIN_LEVEL_ENV = 1
MAINTAIN_LEVEL_RATIO = 30

BOARD_SCALE = 20
START_SCORE = 100
START_ENV = -1

RESTORE_SCORE = 0.5
RESTORE_EFFICIENCY = 1.4
DESTROY_SCORE = 0.5
DESTROY_EFFICIENCY = 1.1

DESTROY_SPREAD = 8
RESTORE_SPREAD = 8

ENV_IMPACT = 0.3
ENV_RESILIENCE = 0.03

STRATEGIES = [always_recover,always_destroy,maintain_score,maintain_env,alter_action]
STRATEGY_NUM = [0,120,140,140,0]

################################################################  sprite definition  ################################################################

class Player():
    # - 한 명의 플레이어를 나타내는 클래스
    # - 플레이어 객체가 가지는 속성
    #    1.플레이어의 점수, 환경 점수 - score, environment : float
    #    2.플레이어의 보드상의 위치 - coordinate : tuple
    #    3.플레이어의 전략을 나타내는 값 - strategy : callable
    #    4.플레이어를 화면에 나타내기 위한 스프라이트들과 그 그룹 - 그룹 spr_group과 그 내부의 객체들
    #    5.다음 턴에 무엇을 할시 임시 저장하는 속성 - turn : Bool
    # - 플레이어 객체가 가지는 메서드
    #    1.현재 보드에 있는 다른 플레이어들의 행동을 파악하며 다음 턴을 정하는 함수 - choose_turn(self)
    #    2.위의 함수의 결과를 기반으로 다음 행동을 실행하는 함수 - make_turn(self)
    #    3.점수가 하위권일 시 탈락하면 속성들을 리셋하고 전략을 바꾼 뒤 속성들을 초기화하는 함수 - reset(self)
    #    4.spr_group의 스프라이트들을 출력하는 함수 - draw(self)
    def __init__(self ,coordinate:tuple ,strategy ,parent_board):
        self.score = START_SCORE
        self.environment = START_ENV
        self.coordinate:tuple = coordinate
        self.strategy = strategy
        self.parent_board = parent_board
        self.turn = False

    def load_sprites(self):
        #스프라이트 그룹과 관련된 내용 삽입 예정
        self.spr_group = pg.sprite.Group()

        #스프라이트 1. 보드 위의 사각형을 나타냄
        section_size = np.array(self.parent_board.rect.size)/BOARD_SCALE
        section_pos  = np.array([[section_size[0],0],[0,section_size[1]]]) @ self.coordinate + np.array(self.parent_board.rect.topleft)
        self.section = spr.Rectangle(section_size,topleft=section_pos)
        self.spr_group.add(self.section)

        #스프라이트 2. 자신의 전략을 나타냄
        strategy_name_center = self.section.rect.center
        if self.strategy == always_recover: self.strategy_name = spr.TextBox("R",center = strategy_name_center,anchor = spr.CENTER)
        elif self.strategy == always_destroy: self.strategy_name = spr.TextBox("D",center = strategy_name_center,anchor = spr.CENTER)
        elif self.strategy == maintain_score: self.strategy_name = spr.TextBox("MS",center = strategy_name_center,anchor = spr.CENTER)
        elif self.strategy == maintain_env: self.strategy_name = spr.TextBox("ME",center = strategy_name_center,anchor = spr.CENTER)
        elif self.strategy == alter_action: self.strategy_name = spr.TextBox("rand",center = strategy_name_center,anchor = spr.CENTER)
        self.spr_group.add(self.strategy_name)
    
    def choose_turn(self):
        self.strategy(self)
        

    def make_turn(self):
        if self.turn == True:        #True는 환경 회복, False는 환경 파괴
            for line in self.parent_board.players:
                for player in line:
                    distance = get_dist(player.coordinate,self.coordinate)
                    player.environment += RESTORE_SCORE / RESTORE_SPREAD * exp(-((distance/RESTORE_SPREAD)**2))
                    self.score -= RESTORE_SCORE / RESTORE_SPREAD * exp(-((distance/RESTORE_SPREAD)**2)) / RESTORE_EFFICIENCY
                    
        else:
            for line in self.parent_board.players:
                for player in line:
                    distance = get_dist(player.coordinate,self.coordinate)
                    player.environment -= DESTROY_SCORE / DESTROY_SPREAD * exp(-((distance/DESTROY_SPREAD)**2))
                    self.score += DESTROY_SCORE / DESTROY_SPREAD * exp(-((distance/DESTROY_SPREAD)**2)) * DESTROY_EFFICIENCY
 
    def reset(self ,new_strategy):
        self.score = START_SCORE
        self.environment = START_ENV
        self.strategy = new_strategy

    def draw(self):
        pass

class Board():
    # - 시뮬레이션이 진행되는 보드를 나타내는 클래스
    # - 보드 객체가 가지는 속성
    #    1.보드가 화면에 표시될 위치와 크기를 나타내는 pygame.Rect 객체 : rect
    #    2.보드에 배치되는 플레이어들의 리스트 - players : list
    def __init__(self ,rect:pg.Rect):
        self.rect = rect
        self.players = []

        num_sum = 0
        for value in STRATEGY_NUM:
            num_sum += value
        if num_sum != BOARD_SCALE**2:
            raise ValueError(f"""STRATEGY_NUM의 총합이 BOARD_SCALE의 제곱과 다릅니다.
                             STRATEGY_NUM의 총합:{num_sum}
                             BOARD_SCALE의 제곱:{BOARD_SCALE**2}""")
        for index,strategy in enumerate(STRATEGIES):
            for i in range(STRATEGY_NUM[index]):
                self.players += [Player((0,0),strategy,self)]
        self.players = np.array(self.players)
        np.random.shuffle(self.players)
        self.players = self.players.reshape((BOARD_SCALE,BOARD_SCALE)).tolist()
        for x, line in enumerate(self.players):
            for y, player in enumerate(line):
                player.coordinate = (x,y)
                player.load_sprites()

    def draw(self):
        player:Player
        for line in self.players:
            for player in line:
                player.spr_group.draw(spr.screen)

    def update(self):
        player:Player
        for line in self.players:
            for player in line:
                player.spr_group.update()
        
################################################################    initial setup    ################################################################

#필요한 상수들과, 시작 전 보드 세팅과 같은 작업들을 수행함
title_box = spr.TextBox("시뮬레이션 화면",center = [spr.SCREEN_SIZE[0]/2,20])
board = Board(BOARD_RECT)

drawables_list = [title_box,board]

################################################################   main event loop   ################################################################

clock = pg.time.Clock()

running = True
while running:

    tick = clock.tick(5)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    for line in board.players:
        for player in line:
            score_to_color(player)
            player.choose_turn()
    for line in board.players:
        for player in line:
            player.make_turn()
    for line in board.players:
        for player in line:
            player.score += ENV_IMPACT * player.environment
            player.environment += ENV_RESILIENCE * tanh((player.environment - START_ENV) / 2)
    spr.screen.fill(spr.BG_COLOR)
    for everything in drawables_list:
        everything.update()
        everything.draw()
    spr.flip_screen()