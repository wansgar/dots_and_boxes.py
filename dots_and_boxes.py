import pygame
import random

# Colors
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180,180,180)
LIGHT_GRAY = (220,220,220)

BACKGROUND_COLOR = GRAY
LINE_COLOR = LIGHT_GRAY
FILLED_LINE_COLOR = BLACK
DOT_COLOR = BLACK
BOX_COLOR = WHITE

# Global consts
BOARD_WIDTH = 5 # only for initial value
DOT_BOX_RATIO = (1/6)
DISPLAY_WIDTH = 500
MENU_HEIGHT = int(DISPLAY_WIDTH*(1/7))
DISPLAY_HEIGHT = DISPLAY_WIDTH + MENU_HEIGHT
DISPLAY_DIMENSIONS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
FONT = "Arial"


class Graphics():
    def __init__(self, display_dimensions):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(display_dimensions)
        pygame.display.set_caption("Dots and Boxes")


class SquareButton():
    rect_design = None
    def __init__(self, x, y, width, action, background_color = None,
        border_color = None, design_color = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = width
        self.action = action
        self.border_width = int((1/9)*width)
        if border_color:
            self.border_color = border_color
        else:
            self.border_color = BLACK
        if background_color:
            self.background_color = background_color
        if design_color:
            self.design_color = design_color
        else:
            self.design_color = BLACK
    def draw_base(self, display):
        inner_width = self.width-2*self.border_width
        inner_height = self.height-2*self.border_width
        # draw outlines
        display.fill(self.border_color,
            rect=[self.x, self.y, self.width, self.border_width])
        display.fill(self.border_color,
            rect=[self.x, self.y+self.border_width,
            self.border_width, inner_height])
        display.fill(self.border_color,
            rect=[self.x+self.width-self.border_width, self.y+self.border_width,
            self.border_width, inner_height])
        display.fill(self.border_color,
            rect=[self.x, self.y+self.height-self.border_width,
            self.width, self.border_width])
        # draw background
        if self.background_color:
            display.fill(self.background_color,
                rect = [self.x+self.border_width, self.y+self.border_width,
                inner_width, inner_height])
    def draw(self, display):
        self.draw_base(display)

class Menu():
    side_padding = int((1/5)*DISPLAY_WIDTH)
    button_width = DISPLAY_WIDTH - 2*side_padding
    button_height = int((1/5)*DISPLAY_HEIGHT)
    button_padding = int((1/7)*button_height)
    FONT_SIZE = int((3/10)*button_height)
    FONT_FAMILY = "Arial"
    FONT_COLOR = BLACK
    class MenuButton(SquareButton):
        def __init__(self,x,y,width,height,text,action, parameter, background_color = None,
            border_color = None, font_family = None, font_color = None, font_size = None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.action = action
            self.action_parameter = parameter
            self.border_width = int((1/9)*self.height)
            if border_color:
                self.border_color = border_color
            else:
                self.border_color = LINE_COLOR
            if background_color:
                self.background_color = background_color
            else:
                self.background_color = BOX_COLOR
            if font_color:
                self.font_color = font_color
            else:
                self.font_color = Menu.FONT_COLOR
            if font_family:
                self.font_family = font_family
            else:
                self.font_family = Menu.FONT_FAMILY
            if font_size:
                self.font_size = font_size
            else:
                self.font_size = Menu.FONT_SIZE
            self.font = pygame.font.SysFont(self.font_family, self.font_size)

        def draw(self, display):
            self.draw_base(display)
            # draw text onto middle of button
            text_surface = self.font.render(self.text, 1, self.font_color)
            rect = text_surface.get_rect()
            x = self.x + int((self.width - rect.width) / 2)
            y = self.y + int((self.height - rect.height) / 2)
            display.blit(text_surface, (x, y))


    def __init__(self, g, menu_items):
        self.g = g
        self.display = g.display
        self.clock = g.clock
        self.menu_items = []
        number_menu_items = len(menu_items)
        pos = [self.side_padding, int((DISPLAY_HEIGHT-number_menu_items*(self.button_height + self.button_padding-1))/2)] # origin position
        for name, action, parameter in menu_items:
            self.menu_items.append(self.MenuButton(pos[0], pos[1], self.button_width, self.button_height, name, action, parameter))
            pos[1] += self.button_height + self.button_padding
        self.running = False

    def draw(self, display):
        for item in self.menu_items:
            item.draw(display)

    def back(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if self.running == False: break
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back()
                        break
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for item in self.menu_items:
                        if (pos[0] >= item.x and pos[0] <= item.x + item.width
                        and pos[1] >= item.y and pos[1] <= item.y + item.height):
                            if item.action:
                                if item.action_parameter:
                                    item.action(item.action_parameter)
                                else:
                                    item.action()
            self.display.fill(BACKGROUND_COLOR)
            self.draw(self.display)
            pygame.display.update()
            self.clock.tick(30)



class ResetButton(SquareButton):
    def draw(self, display):
        self.draw_base(display)
        inner_width = self.width - 2*self.border_width
        inner_origin = (self.x+self.border_width, self.y+self.border_width)
        seventh = int((1/7)*inner_width)
        inside_inner = inner_width - 2*seventh # don't worry 'bout it
        arrowhead_width = int((3/14)*inner_width)
        arrowhead_elevation = int((arrowhead_width)/4)-1
        # draw arrow
        display.fill(self.design_color,
            rect=[inner_origin[0]+seventh, inner_origin[1]+3*seventh,
                seventh, inside_inner-2*seventh])
        display.fill(self.design_color,
            rect=[inner_origin[0]+2*seventh, inner_origin[1]+inside_inner,
                inside_inner-2*seventh, seventh])
        display.fill(self.design_color,
            rect=[inner_origin[0]+inside_inner, inner_origin[1]+seventh,
                seventh, inside_inner])
        display.fill(self.design_color,
            rect=[inner_origin[0]+inside_inner-seventh, inner_origin[1]+seventh,
                seventh, seventh])
        # draw arrow head
        height = arrowhead_width
        arrowhead_origin = [inner_origin[0]+inside_inner-seventh-1,
            inner_origin[1]+seventh - arrowhead_elevation]
        for i in range(arrowhead_width):
            display.fill(self.design_color,
                rect = [arrowhead_origin[0], arrowhead_origin[1],
                    1, height])
            arrowhead_origin[0] -= 1
            arrowhead_origin[1] += 1
            height -= 2

class MenuIconButton(SquareButton):
    def draw(self, display):
        self.draw_base(display)
        inner_width = self.width - 2*self.border_width
        inner_origin = (self.x+self.border_width, self.y+self.border_width)
        # draw the three bars
        # inner_width divided into 7ths to create three bars symmetrically
        display.fill(self.design_color,
            rect = [int(inner_origin[0]+(1/7)*inner_width), int(inner_origin[1]+(1/7)*inner_width),
            inner_width-2*self.border_width, int((1/7)*inner_width)])
        display.fill(self.design_color,
            rect = [int(inner_origin[0]+(1/7)*inner_width), int(inner_origin[1]+(3/7)*inner_width),
            inner_width-2*self.border_width, int((1/7)*inner_width)])
        display.fill(self.design_color,
            rect = [int(inner_origin[0]+(1/7)*inner_width), int(inner_origin[1]+(5/7)*inner_width),
            inner_width-2*self.border_width, int((1/7)*inner_width)])

class Box():
    def __init__(self, board, row, col):
        self.board = board
        self.width = self.board.box_width
        self.height = self.board.box_width
        self.r = row
        self.c = col
        self.color = BOX_COLOR
    def __str__(self):
        return "Box"
    def get_lines(self):
        board = self.board
        return (board[self.r-1][self.c], board[self.r][self.c+1], board[self.r+1][self.c], board[self.r][self.c-1])

class Line():
    def __init__(self, board, row, col, horizontal = True):
        self.board = board
        if horizontal:
            self.is_horizontal = True
            self.width = self.board.box_width
            self.height = self.board.dot_width
        else:
            self.is_horizontal = False
            self.width = self.board.dot_width
            self.height = self.board.box_width
        self.r = row
        self.c = col
        self.filled = False
        self.base_color = LINE_COLOR
    def __str__(self):
        return "Line"
    @property
    def color(self):
        """
        if line is selected: returns global color for line highlighting
        """
        if self.filled:
            return FILLED_LINE_COLOR
        else:
            return self.base_color

    def get_boxes(self):
        """
        returns tuple of the Line's neighbouring boxes if there are any,
        otherwise returns empty tuple
        """
        board = self.board
        out = []
        if self.is_horizontal:
            if self.r != 0: out.append(board[self.r-1][self.c])
            if self.r < len(board)-1: out.append(board[self.r+1][self.c])
        else:
            if self.c != 0: out.append(board[self.r][self.c-1])
            if self.c < len(board)-1: out.append(board[self.r][self.c+1])
        return tuple(out)

class Dot():
    def __init__(self, board, row, col):
        self.board = board
        self.r = row
        self.c = col
        self.width = self.board.dot_width
        self.height = self.board.dot_width
        self.color = DOT_COLOR
    def __str__(self):
        return "Dot"

class Board():
    def __init__(self, width):
        self.w = width
        a = (DOT_BOX_RATIO*(self.w + 1) + self.w)
        b = (DISPLAY_WIDTH//a)*a
        self.origin = ((DISPLAY_WIDTH - b)//2,
            (DISPLAY_WIDTH - b)//2 + MENU_HEIGHT)
        self.menu_origin = (self.origin[0], self.origin[0])
        self.dot_width = int((DOT_BOX_RATIO/a)*b)
        self.box_width = int((b/a))
        self.board = self.new_board(width)

    @property
    def width(self):
        return self.w
    @width.setter
    def width(self, value):
        """
        if width is set: reinitializes the board with new width
        """
        self.__init__(value)

    def __str__(self):
        """
        returns string representation of board, appropriate for terminal output
        """
        stboard = ""
        for row in self.board:
            strow = str(row[0])
            for c in row[1:]:
                strow += " " + str(c)
            stboard += strow + "\n"
        stboard = stboard[:-1]
        return stboard

    # the following magic functions make class Board act as the list board
    def __len__(self):
        return self.board.__len__()

    def __getitem__(self,key):
        return self.board.__getitem__(key)

    def __iter__(self):
        return self.board.__iter__()
    def draw(self,display):
        """
        draws the board to pygame display
        """
        pos = self.origin
        for row in self:
            for i, o in enumerate(row):
                display.fill(o.color, rect=[pos[0], pos[1], o.width, o.height])
                if i == len(row)-1:
                    pos = (self.origin[0], pos[1]+o.height)
                else:
                    pos = (pos[0]+o.width, pos[1])

    def get_object_at_pos(self,pos):
        """
        returns object situated at postion (r,c)
        """
        c_pos = self.origin # current position in iteration
        for row in self:
            for i, o in enumerate(row):
                if (c_pos[0] <= pos[0] and pos[0] < c_pos[0] + o.width and
                c_pos[1] <= pos[1] and pos[1] < c_pos[1] + o.height): # pos is in obj
                    return o
                if i == len(row)-1:
                    c_pos = (self.origin[0], c_pos[1]+o.height)
                else:
                    c_pos = (c_pos[0]+o.width, c_pos[1])

    def new_board(self, width):
        """
        returns a board with given width
        """
        board = []
        r = 0
        c = 0
        for a in range(width):
            row1 = []
            row2 = []
            r = 2*a
            for b in range(width):
                c = 2*b
                row1.append(Dot(self, r,c))
                row1.append(Line(self, r,c+1))
                row2.append(Line(self, r+1, c, False)) # False means vertical
                row2.append(Box(self, r+1,c+1))
            c += 2
            row1.append(Dot(self, r,c))
            row2.append(Line(self, r+1, c, False))
            board.append(row1)
            board.append(row2)
        row = []
        r += 2
        for i in range(width):
            c = 2*i
            row.append(Dot(self, r,c))
            row.append(Line(self, r,c+1))
        row.append(Dot(self, r,c+2))
        board.append(row)
        return board

    def reset(self):
        """
        initializes with current width
        """
        self.__init__(self.width)

class Player():
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.score = 0

class Multiplayer():
    def __init__(self, g, width): # g passed for graphics
        self.g = g
        self.display = g.display
        self.clock = g.clock
        self.players = [Player("Blue", (0,0,255)), Player("Red", (255,0,0))]
        self.current_player = self.players[0]
        self.board = Board(width)
        self.upper_menu = [
        MenuIconButton(self.board.menu_origin[0], self.board.menu_origin[1],
            self.board.origin[1]-2*self.board.menu_origin[1], self.quit_to_menu, WHITE),
        ResetButton(DISPLAY_WIDTH-self.board.menu_origin[0]-(self.board.origin[1]-2*self.board.menu_origin[1]), self.board.menu_origin[1],
            self.board.origin[1]-2*self.board.menu_origin[1], self.reset, WHITE)
        ]
        self.highlighted_object = None

    def pos_in_object(self, pos, obj):
        """
        returns if given position is inside borders of object
        -> bool
        """
        if (pos[0] >= obj.x and pos[0] <= obj.x+obj.width
            and pos[1] >= obj.y and pos[1] <= obj.y+obj.height): return True
        else: return False

    def reset(self):
        """
        inisializes with current graphics and width
        """
        self.__init__(self.g, self.board.width)

    def quit_to_menu(self):
        self.board.reset()
        self.running = False

    def run(self, width):
        """
        runs menu with user interaction, pygame GUI
        """
        self.__init__(self.g, width)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if self.running == False:
                    break
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.board.reset()
                        self.running = False
                        break
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_object = self.board.get_object_at_pos(pos)
                    if clicked_object:
                        #print("click: (",pos,clicked_object, clicked_object.r, clicked_object.c,")") # DEBUG
                        if type(clicked_object) == Line:
                            # line is filled
                            clicked_object.filled = True
                            # check if box is last line filled
                            boxes = clicked_object.get_boxes()
                            filled_boxes = []
                            for box in boxes:
                                lines = box.get_lines()
                                filled_counter = 0 # how many lines are filled in box
                                for line in lines:
                                    if line.filled: filled_counter += 1
                                if filled_counter == len(lines): filled_boxes.append(box)
                            if filled_boxes: # if any filled boxes
                                # fill boxes with color
                                for box in filled_boxes:
                                    self.current_player.score += 1
                                    box.color = self.current_player.color
                                # check win condition
                                total_score = 0
                                for player in self.players:
                                    total_score += player.score
                                if total_score == self.board.width**2:
                                    # game done
                                    # DEBUG
                                    print("WIN: ( ",end="")
                                    for player in self.players:
                                        box_percentage = (player.score/(self.board.width**2))*100
                                        print(player.score, " (", "%.1f" % box_percentage, " %)", end=" ")
                                    print(")")
                            else:
                                # next player's turn if no boxes filled
                                self.current_player = self.players[(
                                    self.players.index(self.current_player) + 1) % len(self.players)]
                    else:
                        for o in self.upper_menu:
                            if self.pos_in_object(pos,o):
                                if o.action: o.action()
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    new_highlighted_object = self.board.get_object_at_pos(pos)
                    if new_highlighted_object != self.highlighted_object:
                        if type(self.highlighted_object) == Line:
                            self.highlighted_object.base_color = LINE_COLOR
                        if type(new_highlighted_object) == Line:
                            new_highlighted_object.base_color = self.current_player.color
                        self.highlighted_object = new_highlighted_object


            self.display.fill(BACKGROUND_COLOR)
            self.board.draw(self.display)
            for item in self.upper_menu:
                item.draw(self.display)
            pygame.display.update()
            self.clock.tick(30)

class Singleplayer(Multiplayer):
    def __init__(self, g, width):
        self.g = g
        self.display = g.display
        self.clock = g.clock
        if random.randint(0,1) == 0:
            self.players = [AI("AI", BLUE), Player("Player", RED)]
        else:
            self.players = [Player("Player", BLUE), AI("AI", RED)]
        self.current_player = self.players[0]
        self.board = Board(width)
        self.upper_menu = [
        MenuIconButton(self.board.menu_origin[0], self.board.menu_origin[1],
            self.board.origin[1]-2*self.board.menu_origin[1], self.quit_to_menu, WHITE),
        ResetButton(DISPLAY_WIDTH-self.board.menu_origin[0]-(self.board.origin[1]-2*self.board.menu_origin[1]), self.board.menu_origin[1],
            self.board.origin[1]-2*self.board.menu_origin[1], self.reset, WHITE)
        ]
        self.highlighted_object = None

class AI():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0
    def move(board):
        pass

def quit_game():
    pygame.quit()
    quit()

def main():
    g = Graphics(DISPLAY_DIMENSIONS)
    sp = Singleplayer(g, BOARD_WIDTH)
    mp = Multiplayer(g, BOARD_WIDTH)
    mp_menu = Menu(g,(
        ("Small", mp.run, 3), # name, action_function, function_parameter
        ("Medium", mp.run, 5),
        ("Large", mp.run, 7),
        ("Back", lambda:None, None)
    ))
    mp_menu.menu_items[-1].action = mp_menu.back # weird but works - "Back" menu button
    sp_menu = Menu(g,(
        ("Small", sp.run, 3),
        ("Medium", sp.run, 5),
        ("Large", sp.run, 7),
        ("Back", lambda:None, None)
    ))
    sp_menu.menu_items[-1].action = sp_menu.back
    menu = Menu(g, (
        ("Singleplayer", sp_menu.run, None),
        ("Multiplayer", mp_menu.run, None),
        ("Quit", quit_game, None)
    ))
    menu.run()


if __name__ == "__main__":
    main()
    pygame.quit()
    quit()
