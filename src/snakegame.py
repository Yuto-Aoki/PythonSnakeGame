import math
import random
import pygame
import random

Width = 500   # 画面幅
Height = 500  # 画面高さ

Cols = 25
Rows = 20

class Cube():
    """
    Snakeの各体やFruitのオブジェクト
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
            if event.type == pygame.QUIT:
                pygame.font.init()
                screen = pygame.display.set_mode((200, 100))
                pygame.display.set_caption("Continue?")
                yes = pygame.Rect(30, 30, 50, 50)  # creates a rect object
                no = pygame.Rect(100, 30, 70, 50)  # creates a rect object
                font = pygame.font.SysFont(None, 25)
    
                #STEP2.テキストの設定
                text1 = font.render("Yes", True, (0,0,0))
                text2 = font.render("No", True, (0,0,0))
                while True:
                    screen.fill((0,0,0))  #画面を黒で塗りつぶす
            
                    pygame.draw.rect(screen, (255, 0, 0), yes)
                    pygame.draw.rect(screen, (0, 255, 0), no)

                    screen.blit(text1, (40, 45))
                    screen.blit(text2, (105,45))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if yes.collidepoint(event.pos):
                                print("red button was pressed")
                                pygame.quit()
                                exit()
                            if no.collidepoint(event.pos):
                                print("green button was pressed")
                                break
                
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
        
    def addTail(self):
        """
        Fruitをとった際にSnakeの末尾にCubeを追加する
        """
        tail = self.body[-1]
        tail_x, tail_y = tail.x, tail.y

        # 右に進んでいるときは左に追加
        if tail_x == 1 and tail_y == 0:
            self.body.append(Cube((tail.pos[0]- 1, tail.pos[1]), x=tail_x, y=tail_y))
        # 上に進んでいるときは下に追加
        elif tail_x == 0 and tail_y == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), x=tail_x, y=tail_y))
        # 左に進んでいるときは右に追加
        elif tail_x == -1 and tail_y == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), x=tail_x, y=tail_y))
        # 下に進んでいるときは上に追加 
        elif tail_x == 0 and tail_y == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), x=tail_x, y=tail_y))

        
    def draw(self, surface):
        """
        各Cubeを描画
        """
        for cube in self.body:
            cube.draw(surface)

class Game():
    """
    Game開始時に設定
    """
    def __init__(self):
        pygame.display.set_caption("Snake Game!!")
        self.surface = pygame.display.set_mode((Width, Height))
        self.snake = Snake(pos=(10,10), color=(255,0,0)) # Snakeの初期値、色を決定
        self.snake.addTail()                             # Snakeは最初2つのCubeを持っていることにする
        self.clock = pygame.time.Clock()
        self.fruit = Cube(self.randomFruit(Rows, self.snake), color=(0,255,0)) # フルーツの色を決定、場所はランダム
    
    def drawGrid(self, width, rows, surface):
        """
        Grid線を描画
        """
        sizeBtwn = width // rows
        x = 0
        y = 0
        for line in range(rows):
            x = x + sizeBtwn
            y = y +sizeBtwn

            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
            pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))
    
    def randomFruit(self, rows, snake):
        """
        ランダムにフルーツを決定
        """
        positions = snake.body

        while True:
            x = random.randrange(1, rows-1)
            y = random.randrange(1, rows-1)
            if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
                continue
            else:
                break
        return (x, y)

    def allDraw(self):
        """
        全ての描画処理
        """
        self.surface.fill((0,0,0))
        self.drawGrid(Width, Rows, self.surface) # Grid線描画
        self.snake.draw(self.surface)            # Snake描画
        self.fruit.draw(self.surface)            # Fruit描画
        pygame.display.update()
    
    def play(self):
        best_score = 0
        while True:
            pygame.time.delay(50)
            self.clock.tick(10)
            self.snake.move()
            headPos = self.snake.head.pos
            if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
                print("Score:", len(self.snake.body))
                best_score = max(len(self.snake.body), best_score)
                print("Best Score:", best_score)
                self.snake.reset((10, 10))

            if self.snake.body[0].pos == self.fruit.pos:
                self.snake.addTail()
                self.fruit = Cube(self.randomFruit(Rows, self.snake), color=(0,255,0))
                
            for x in range(len(self.snake.body)):
                if self.snake.body[x].pos in list(map(lambda z: z.pos, self.snake.body[x+1:])):
                    print("Score:", len(self.snake.body))
                    best_score = max(len(self.snake.body), best_score)
                    print("Best Score:", best_score)
                    self.snake.reset((10,10))
                    break
                        
            self.allDraw()
        

if __name__ == "__main__":
    game = Game()
    game.play()