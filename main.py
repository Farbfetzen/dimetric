"""Copyright (C) 2020  Sebastian Henz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import pygame


def rotate_clockwise(world):
    world = list(zip(*world[::-1]))
    world = [list(column) for column in world]
    return world


def rotate_counterclockwise(world):
    world = list(zip(*world))[::-1]
    world = [list(column) for column in world]
    return world


pygame.init()

display = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

BACKGROUND_COLOR = (0, 0, 0)
COLORKEY = (255, 255, 255)
tiles = []
for filename in ("green.png", "red.png"):
    tile = pygame.image.load(filename).convert()
    tile.set_colorkey(COLORKEY)
    tiles.append(tile)

map_data = [
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0]
]
# Important: index the map with MAP_DATA[y][x] like a matrix.

TILE_WIDTH_HALF = 32
TILE_HEIGHT_HALF = 16
OFFSET_X = display.get_rect().width // 2 - TILE_WIDTH_HALF * len(map_data[0])
OFFSET_Y = display.get_rect().height // 2 - TILE_HEIGHT_HALF

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                OFFSET_Y -= TILE_HEIGHT_HALF
            elif event.key == pygame.K_a:
                OFFSET_X -= TILE_WIDTH_HALF
            elif event.key == pygame.K_s:
                OFFSET_Y += TILE_HEIGHT_HALF
            elif event.key == pygame.K_d:
                OFFSET_X += TILE_WIDTH_HALF
            elif event.key == pygame.K_e:
                map_data = rotate_clockwise(map_data)
            elif event.key == pygame.K_q:
                map_data = rotate_counterclockwise(map_data)

    display.fill(BACKGROUND_COLOR)
    for map_y, row in enumerate(map_data):
        for map_x, i in enumerate(row):
            tile = tiles[i]
            display_x = (map_x + map_y) * TILE_WIDTH_HALF + OFFSET_X
            display_y = (map_y - map_x) * TILE_HEIGHT_HALF + OFFSET_Y
            display.blit(tile, (display_x, display_y))

    pygame.display.flip()
