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

import os

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
TILE_WIDTH = 64
TILE_HEIGHT = 32
TILE_WIDTH_HALF = TILE_WIDTH // 2
TILE_HEIGHT_HALF = TILE_HEIGHT // 2

tiles = []
tile_offsets = []
for filename in ("platform.png", "red.png"):
    tile = pygame.image.load(os.path.join("images", filename)).convert()
    tile.set_colorkey(COLORKEY)
    tiles.append(tile)
    tile_offsets.append((
        TILE_WIDTH - tile.get_width(),
        TILE_HEIGHT - tile.get_height()
    ))

map_data = [
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
# Important: index the map with MAP_DATA[y][x] like a matrix.

OFFSET_X = display.get_rect().width // 2 - TILE_WIDTH_HALF * len(map_data[0])
OFFSET_Y = display.get_rect().height // 2 - TILE_HEIGHT_HALF

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                OFFSET_Y -= TILE_HEIGHT
            elif event.key == pygame.K_a:
                OFFSET_X -= TILE_WIDTH
            elif event.key == pygame.K_s:
                OFFSET_Y += TILE_HEIGHT
            elif event.key == pygame.K_d:
                OFFSET_X += TILE_WIDTH
            elif event.key == pygame.K_e:
                map_data = rotate_clockwise(map_data)
            elif event.key == pygame.K_q:
                map_data = rotate_counterclockwise(map_data)

    display.fill(BACKGROUND_COLOR)
    for map_y, row in enumerate(map_data):
        for map_x, i in reversed(list(enumerate(row))):
            # reversed() so that tiles are drawn back to front
            tile = tiles[i]
            tile_offset_x, tile_offset_y = tile_offsets[i]
            display_x = (map_x + map_y) * TILE_WIDTH_HALF + OFFSET_X + tile_offset_x
            display_y = (map_y - map_x) * TILE_HEIGHT_HALF + OFFSET_Y + tile_offset_y
            display.blit(tile, (display_x, display_y))

    pygame.display.flip()
