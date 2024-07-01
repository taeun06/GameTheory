import pygame
import numpy as np
from abc import *

import sprites
        
def strategy1():
    pass

def strategy2():
    pass

def strategy3():
    pass

def strategy4():
    pass

board_scale = 10
start_money = 100                                       #플레이어의 시작 돈 
nature = [[0]*board_scale]*board_scale                  #각 플레이어들의 거주지의 환경 점수
strategies = [strategy1,strategy2,strategy3,strategy4]  #각 전략들의 함수를 이 list 자료에 저장하기
strategy_num = [25,25,25,25]                            #각 전략을 가진 플레이어들의 수를 저장
board = []

class player():

    def __init__(self, strategy):
        self.strategy = strategy
        self.money = start_money

    def eliminate(self):
        self.strategy = None
        self.money = start_money

    def make_turn(self):
        if self.strategy() == True:                     #True는 자연 회복, False는 자연 파괴
            pass
        else:
            pass

def next_turn():
    pass                                                #환경 점수에 비례해서 그 위 플레이어 점수가 변함

def generate_board():

    global board
    num_sum = 0

    for i in strategy_num:
        num_sum += i

    if num_sum != board_scale**2:
        raise ValueError(f"""strategy_num의 총합은 board_scale의 제곱과 같아야 합니다.
                             strategy_num의 총합:{num_sum}
                             board_scale의 제곱:{board_scale**2}""")
    
    players = []
    for index,strategy in enumerate(strategies):
        players += [player(strategy)]*strategy_num[index]

    players = np.array(players)
    np.random.shuffle(players)
    players.reshape((board_scale,board_scale))
    board = players.tolist()