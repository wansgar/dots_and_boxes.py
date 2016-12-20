import pygame

class Box(object):
    def __init__(self, row, col):
        self.walls = [False, False, False, False] # True if player placed wall
        self.filled = 0 # 1 for p1, 2 for p2

    def draw(display, background_color, line_color, dot_color, border_color):
        
