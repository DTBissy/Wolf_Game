WIN_WIDTH = 1200
WIN_HEIGHT = 800
PLAYER_HEALTH = 0
PLAYER_LAYER = 5
ENEMYLAYER = 4
ENEMY_SPEED = 2
BLOCK_LAYER = 3
PLAYER_SPEED = 3
DECOR_LAYER = 2
GROUND_LAYER = 1
TILE_SIZE = 32
FPS = 60
RED =(255, 0, 0)
GREEN =(0, 255, 0)
BLACK =(0, 0, 0)
BLUE =(0, 0, 255)
WHITE = (255, 255, 255)
# Because the Height is 480 pixels and the TILESZE is 32
# We will divide the two to determine how many rows well have
# Since our Width is 640 and the TILESIZE is 32
# We will have 20 columns for the wall to surround the outer perimiter
TILEMAP = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B................................B...B',
    'B.....P........................E.....B',
    'B..................BB................B',
    'B..................BB......ffffffff..B',
    'BBBBBBBBBBBBBBBBBBBBB..........ffff..B',
    'B..................BB..........ffff..B',
    'B..W...............BB.......S........B',
    'B....................................B',
    'B....................................B',
    'B...................BB...............B',
    'B...................BB...............B',
    'B...................BB...............B',
    'B........E..........BB...............B',
    'B...................BB...........X...B', # Bomb placement here
    'BBBBBBBBBBBBBBBBB...BBBBBBBBBBBBBBBBBB',
    'B..............BB...BB...............B',
    'B...............B...BB...............B',
    'B..........E....B...BB...............B',
    'B...H...............BB...............B',
    'B...................BB...............B',
    'B...............................g....B',
    'B.............................g..g...B',
    'B..................BB................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]
