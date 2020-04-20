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

    display.fill(BACKGROUND_COLOR)
    for map_y, row in enumerate(MAP_DATA):
        for map_x, i in enumerate(row):
            tile = tiles[i]
            display_x = (map_x + map_y) * TILE_WIDTH_HALF + OFFSET_X
            display_y = (map_y - map_x) * TILE_HEIGHT_HALF + OFFSET_Y
            display.blit(tile, (display_x, display_y))

    pygame.display.flip()
