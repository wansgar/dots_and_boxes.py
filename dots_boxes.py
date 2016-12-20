import pygame
import random

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
LINE_WIDTH = BOX_SIZE//10

WINDOW_SIZE = (DIMENSIONS[0]*BOX_SIZE, DIMENSIONS[1]*BOX_SIZE)
FRAME_RATE = 30

def main():
    """
    Main function
    """
    pygame.init()
    display = pygame.display.set_mode(WINDOW_SIZE)
    display.fill(BACKGOUND_COLOR)
    pygame.display.set_caption("Dots and Boxes")
    clock = pygame.time.Clock()


if __name__ == '__main__':
    main()
