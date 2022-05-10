import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# notation
FIELD_NUMBERS = [
    [None, 1,   None, 2,    None, 3,    None, 4],
    [5, None,   6, None,    7, None,    8, None],
    [None, 9,   None, 10,   None, 11,   None, 12],
    [13, None,  14, None,   15, None,   16, None],
    [None, 17,  None, 18,   None, 19,   None, 20],
    [21, None,  22, None,   23, None,   24, None],
    [None, 25,  None, 26,   None, 27,   None, 28],
    [29, None,  30, None,   31, None,   32, None]
]

# first validation
PAWN_VALUES_ONE = [None, 1.8, 1.6, 1.4, 1.4, 1.4, 1.2, 1]

# second validation
PAWN_VALUES_TWO = [
    [None, None,    None, None,     None, None,     None, None],
    [1.9, None,     1.8, None,      1.8, None,      1.8, None],
    [None, 1.7,     None, 1.7,      None, 1.7,      None, 1.8],
    [1.7, None,     1.5, None,      1.5, None,      1.5, None],
    [None, 1.45,    None, 1.45,     None, 1.45,     None, 1.55],
    [1.45, None,    1.35, None,     1.35, None,     1.35, None],
    [None, 1.15,    None, 1.15,     None, 1.15,     None, 1.25],
    [1, None,       1, None,        1, None,        1, None],
]

# king validation
KING_VALUES = [
    [None, 3,   None, 3.5,  None, 3,     None, 3],
    [3, None,   3.5, None,  3.5, None,   3, None],
    [None, 3.5, None, 4,    None, 4,    None, 3],
    [3.5, None, 4, None,    4, None,    3.5, None],
    [None, 3.5, None, 4,    None, 4,    None, 3.5],
    [3, None,   4, None,    4, None,    3.5, None],
    [None, 3,   None, 3.5,  None, 3.5,  None, 3],
    [3, None,   3, None,    3.5, None,  3, None],
]

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

DRAW = 'draw'
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
