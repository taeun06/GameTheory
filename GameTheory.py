import pygame as pg
import numpy as np
from abc import *
import sprites as spr

        
def strategy1():
    pass

def strategy2():
    pass

def strategy3():
    pass

def strategy4():
    pass

board_scale = 10
start_score = 100                                       #플레이어의 시작 돈 
start_env = 0                                           #보드 한 칸의 시작 환경 점수
nature = [[0]*board_scale]*board_scale                  #각 플레이어들의 거주지의 환경 점수 - 삭제 예정

strategies = [strategy1,strategy2,strategy3,strategy4]  #각 전략들의 함수를 이 list 자료에 저장하기
strategy_num = [25,25,25,25]                            #각 전략을 가진 플레이어들의 수를 저장
board = []

spr.init(700,board_scale)

def generate_board():

    global board
    num_sum = 0

    for i in strategy_num:
        num_sum += i

    if num_sum != board_scale**2:
        raise ValueError(f"""strategy_num의 총합이 board_scale의 제곱과 다릅니다.
                             strategy_num의 총합:{num_sum}
                             board_scale의 제곱:{board_scale**2}""")
    
    players = []
    for index,strategy in enumerate(strategies):
        players += [player(strategy)]*strategy_num[index]

    players = np.array(players)
    np.random.shuffle(players)
    players.reshape((board_scale,board_scale))
    board = players.tolist()

################################################################  sprite definition  ################################################################

class player():
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
    #    4.spr_group의 스프라이트들의 내용을 재로딩하는 함수 - render_sprites(self)
    #    5.spr_group의 스프라이트들을 출력하는 함수 - draw(self)
    def __init__(self ,coordinate:tuple ,strategy):
        self.score = start_score
        self.environment = start_env
        self.coordinate:tuple = coordinate
        self.strategy = strategy
        #스프라이트 그룹과 관련된 내용 삽입 예정
    
    def choose_turn(self):
        self.turn = self.strategy()

    def make_turn(self):
        if self.turn == True:                     #True는 환경 회복, False는 환경 파괴
            pass
        else:
            pass

    def reset(self ,new_strategy):
        self.score = start_score
        self.environment = start_env
        self.strategy = new_strategy

    def render_sprites():
        pass

    def draw(self):
        pass
        

################################################################   main event loop   ################################################################

clock = pg.time.Clock()

running = True
while running:

    tick = clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    spr.update_screen(clock.get_fps())
    spr.flip_screen()