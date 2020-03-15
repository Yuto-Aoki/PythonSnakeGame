import math
import random
import pygame
import random

Width = 500
Height = 500

Cols = 25
Rows = 20

class Cube():
    """
    Snakeの各体のオブジェクト
    """
    def __init__(self, start, x=1, y=0, color=(255,0,0)):
        self.rows = 20
        self.w = 500
        self.pos = start # (x, y)
        self.x = x
        self.y = y
        self.color = color
    
    def move(self, x, y):
        self.x = x       # new x
        self.y = y       # new y
        self.pos = (self.pos[0] + self.x, self.pos[1] + self.y)
    
    def draw(self, surface):
        dis = self.w // self.rows
        x, y = self.pos
        pygame.draw.rect(surface, self.color, (x * dis + 1, y * dis + 1, dis - 2, dis - 2))

class Snake():
    def __init__(self, pos, color):
        self.head = Cube(pos)   #頭の位置
        self.color = color
        self.body = [self.head] # 体、最初に頭を追加
        self.turns = {}
        self.x = 0
        self.y = 1
    
    def reset(self, pos):
        """
        Gameoverなどでリセットする際に呼び出される
        """
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x = 0
        self.y = 1

    def move(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed() # keyは押したままにする
            
            for key in keys:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:       # 左に進む
                    self.x = -1
                    self.y = 0
                elif keys[pygame.K_UP] or keys[pygame.K_w]:       # 上に進む
                    self.x = 0
                    self.y = -1
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:    # 右に進む
                    self.x = 1
                    self.y = 0
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:     # 下に進む
                    self.x = 0
                    self.y = 1
                self.turns[self.head.pos[:]] = [self.x, self.y]
    
        for i, cube in enumerate(self.body):
            posision = cube.pos[:]
            if posision in self.turns:    # 曲がる動作をしていたら
                turn = self.turns[posision]
                cube.move(x=turn[0], y=turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(posision)
            else:
                cube.move(x=cube.x, y=cube.y)
        
        def add(self):
            """
            Fruitをとった際にSnakeの末尾にCubeを追加する
            """
            tail = self.body[-1]
            tail_x, tail_y = tail.x, tail.y

            # 右に進んでいるときは左に追加
            if tail_x == 1 and tail_y == 0:
                self.body.append(Cube((tail.pos[0]- 1, tail.pos[1])))
            # 上に進んでいるときは下に追加
            elif tail_x == 0 and tail_y == -1:
                self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
            # 左に進んでいるときは右に追加
            elif tail_x == -1 and tail_y == 0:
                self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
            # 下に進んでいるときは上に追加 
            elif tail_x == 0 and tail_y == 1:
                self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))


if __name__ == "__main__":
    cube = Cube((10, 10))
    win = pygame.display.set_mode((Width,Height))
    win.fill((0,0,0)) 
    cube.draw(win)