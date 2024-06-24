import pygame
import numpy as np
from abc import *

pygame.init()
screen_size = np.array((1366,768))
pygame.display.set_mode(screen_size)
pygame.display.set_caption("Simulation Screen")

class Box(metaclasss = ABCMeta):

    def __init__(self,pos:list,size:list):
        self.pos = np.array(pos)
        self.size = np.array(size)

        self.SubBoxes = []

    @abstractmethod
    def draw(self,pos = None):
        if pos is None:
            pos == self.pos
        pass
    
    def drawALL(self,pos = None):
        if pos is None:
            pos == self.pos
        self.draw(pos)
        SubBox:Box
        for SubBox in self.SubBoxes:
            SubBox.drawALL(pos + SubBox.pos)

class boardBox(Box):

    def __init__(self,pos:list,size:list):
        global board_scale
        super().__init__(pos,size)

class sectionBox(Box):

    def __init__(self,coordinate:list,board_size:np.ndarray):
        size = board_size/board_scale
        pos = np.array([[coordinate[0],0],[0,coordinate[1]]]) @ size
        super().__init__(pos,size)

        
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