"""Main loop."""

# Copyright (C) 2020  Sebastian Henz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from math import floor
import pygame


def run():
    pygame.init()
    display = pygame.display.set_mode((640, 480))
    display_rect = display.get_rect()
    clock = pygame.time.Clock()



    OFFSET_X = display_rect.centerx - TILE_WIDTH_HALF
    OFFSET_Y = display_rect.centery - TILE_HEIGHT_HALF * len(map_data)

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[2]:  # right mouse button
                    OFFSET_X += event.rel[0]
                    OFFSET_Y += event.rel[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(screen_to_map(*event.pos))

        pressed = pygame.key.get_pressed()
        map_scroll_distance = MAP_SCROLL_SPEED * dt
        if pressed[pygame.K_w]:
            OFFSET_Y -= map_scroll_distance
        if pressed[pygame.K_a]:
            OFFSET_X -= map_scroll_distance
        if pressed[pygame.K_s]:
            OFFSET_Y += map_scroll_distance
        if pressed[pygame.K_d]:
            OFFSET_X += map_scroll_distance

        display.fill(BACKGROUND_COLOR)
        for map_y, row in enumerate(map_data):
            for map_x, i in enumerate(row):
                tile = tiles[i]
                display.blit(tile, map_to_screen(map_x, map_y, *tile_offsets[i]))

        # pygame.draw.circle(display, pygame.Color("red"), (OFFSET_X, OFFSET_Y), 1)
        # pygame.draw.circle(display, pygame.Color("orange"), display_rect.center, 1)

        # Highlight the outline of a tile when the mouse is over the map.
        # TODO: highlight the top of the platform
        # TODO: snap to grid when mouse is over the raised part of a platform, not
        #   only over the base.
        mouse_pos = pygame.mouse.get_pos()
        mouse_map_pos = screen_to_map(*mouse_pos)
        if any(0 > pos or pos > len(map_data) - 1 for pos in mouse_map_pos):
            tile = tiles[2]
            rect = tile.get_rect(center=mouse_pos)
            display.blit(tiles[2], rect)
        else:
            display.blit(
                tiles[2],
                map_to_screen(
                    mouse_map_pos[0],
                    mouse_map_pos[1],
                    *tile_offsets[2]
                )
            )

        pygame.display.flip()


def map_to_screen(map_x, map_y, offset_x, offset_y):
    screen_x = (map_x - map_y) * TILE_WIDTH_HALF + OFFSET_X + offset_x
    screen_y = (map_x + map_y) * TILE_HEIGHT_HALF + OFFSET_Y + offset_y
    return screen_x, screen_y


def screen_to_map(screen_x, screen_y):
    # Adapted from the code example in wikipedia:
    # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates
    virt_x = (screen_x - (OFFSET_X - (len(map_data) - 1) * TILE_WIDTH_HALF)) / TILE_WIDTH
    virt_y = (screen_y - OFFSET_Y) / TILE_HEIGHT
    map_x = floor(virt_y + (virt_x - len(map_data[0]) / 2))
    map_y = floor(virt_y - (virt_x - len(map_data) / 2))
    # Coordinates are floats. Use int() to get the tile position in the map data.
    # Strictly speaking it should be rounded down but int() rounds towards zero.
    # Rounding down will result in the correct coordinates even if
    # the map coordinates are negative.
    return map_x, map_y
