import math
import random
import pygame
import random

Width = 500
Height = 500

Cols = 25
Rows = 20

class Cube():
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.rows = 20
        self.w = 500
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color