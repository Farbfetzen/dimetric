import pygame


pygame.init()

display = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

COLORKEY = (255, 255, 255)
tiles = []
for filename in ("green.png", "red.png"):
    tile = pygame.image.load(filename).convert()
    tile.set_colorkey(COLORKEY)
    tiles.append(tile)

MAP_DATA = [
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0]
]
# Important: index the map with MAP_DATA[y][x] like a matrix.

TILE_WIDTH_HALF = 32
TILE_HEIGHT_HALF = 16
OFFSET_X = display.get_rect().width // 2 - TILE_WIDTH_HALF * len(MAP_DATA[0])
OFFSET_Y = display.get_rect().height // 2 - TILE_HEIGHT_HALF

for map_y, row in enumerate(MAP_DATA):
    for map_x, i in enumerate(row):
        tile = tiles[i]
        display_x = (map_x + map_y) * TILE_WIDTH_HALF + OFFSET_X
        display_y = (map_y - map_x) * TILE_HEIGHT_HALF + OFFSET_Y
        display.blit(tile, (display_x, display_y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    pygame.display.flip()
