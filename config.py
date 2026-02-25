# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60

# Color
GREY = (20,20,20)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Board
BOARD_X = 100
BOARD_Y = 50
BOARD_WIDTH = 300
BOARD_HEIGHT = 600
SIDE = BOARD_WIDTH//10

COLUMN: int = 10
ROWS = 20

EMPTY_GRID = []
EMPTY_ROW = [0 for _ in range(COLUMN)]

for _ in range(ROWS):
    EMPTY_GRID.append([])
    for _ in range(COLUMN):
        EMPTY_GRID[-1].append(0)

# Shape Data
tetris_data = {
    'O': [[[1,1],[1,1]], (0, 200, 200)],
    'I': [[[1,1,1,1]],[[1],[1],[1],[1]], (230, 200, 40)],
    'T': [[[0,1,0],[1,1,1]],[[1,0],[1,1],[1,0]],[[1,1,1],[0,1,0]],[[0,1],[1,1],[0,1]], (150, 0, 200)],
    'Z': [[[1,1,0],[0,1,1]], [[0,1],[1,1],[1,0]], (0, 200, 0)],
    'S': [[[0,1,1],[1,1,0]],[[1,0],[1,1],[0,1]],(200, 0, 0)],
    'J': [[[1,0,0],[1,1,1]], [[1,1],[1,0],[1,0]], [[1,1,1],[0,0,1]], [[0,1],[0,1],[1,1]], (25, 100, 200)],
    'L': [[[0,0,1],[1,1,1]],[[1,0],[1,0],[1,1]], [[1,1,1],[1,0,0]], [[1,1],[0,1],[0,1]], (220, 140, 0)]
}

BLOCK_KEYS = list(tetris_data.keys())

LINE_COMBO = {
    0 : ['', 0],
    1 : ["Single +100", 100],
    2 : ["Double +300", 300],
    3 : ["Triple +600", 600],
    4 : ["Tetris +800", 800]
}
