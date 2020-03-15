import math
import random
import pygame
import random

Width = 500
Height = 500

Cols = 25
Rows = 20

class Cube():
    def __init__(self, start, x=1, y=0, color=(255,0,0)):
        self.rows = 20
        self.w = 500
        self.pos = start
        self.x = x
        self.y = y
        self.color = color
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.pos[0] + self.x, self.pos[1] + self.y)