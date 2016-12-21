import pygame

class Box(object):
    def __init__(self, row, col):
        self.walls = [False, False, False, False] # True if player placed wall
        self.filled = 0 # 1 for p1, 2 for p2
        self.row = row
        self.col = col

    def draw(self, display, box_size, line_width, background_color, line_color, border_color):
        # background
        display.fill(background_color, rect=[self.row*box_size, self.col*box_size, box_size, box_size])
        # lines
        display.fill(line_color, rect=[self.row*box_size, self.col*box_size, box_size, line_width])
        display.fill(line_color, rect=[self.row*box_size, self.col*box_size+(box_size-line_width), box_size, line_width])
        display.fill(line_color, rect=[self.row*box_size, self.col*box_size, line_width, box_size])
        display.fill(line_color, rect=[self.row*box_size+(box_size-line_width), self.col*box_size, line_width, box_size])
        # border
