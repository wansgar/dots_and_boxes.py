import pygame
import random

from box import Box

# COLORS
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (192,192,192)

# GAME
BACKGOUND_COLOR = WHITE
P1_COLOR = BLUE
P2_COLOR = RED
DOT_COLOR = BLACK
LINE_COLOR = BLACK
BORDER_COLOR = GRAY

DIMENSIONS = (10, 10)
BOX_SIZE = 50
LINE_WIDTH = BOX_SIZE//15

WINDOW_SIZE = (DIMENSIONS[0]*BOX_SIZE, DIMENSIONS[1]*BOX_SIZE)
FRAME_RATE = 30

def main():
    """
    Main function
    """
    pygame.init()
    display = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.Surface(WINDOW_SIZE)
    background.fill(BACKGOUND_COLOR)
    display.blit(background, (0,0)) # (Surface, pos)
    pygame.display.set_caption("Dots and Boxes")
    clock = pygame.time.Clock()

    grid = [[Box(r,c) for c in range(DIMENSIONS[1])] for r in range(DIMENSIONS[0])]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        draw_grid(display, grid)
        clock.tick(FRAME_RATE)

def draw_grid(display, grid):
    """
    Draws grid to display
    """
    display.fill(BACKGOUND_COLOR)
    for row in grid:
        for box in row:
            box.draw(display, BOX_SIZE, LINE_WIDTH, BACKGOUND_COLOR, LINE_COLOR, BORDER_COLOR)
    pygame.display.update()

if __name__ == '__main__':
    main()
