"""Camera object controlling coordinate conversions."""

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


# TODO: World coordinates should be similar in dimension to screen coordinates.
#  This will make movement and collision detection easier because the collision
#  rects will live in world coordinates. Maybe make one tile edge 10 or 100 long?
#  It should not matter much because of the conversion.


import pygame

import src.constants as const


class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height

        # The camera offset is the top of the base of the topmost tile.
        # The world starts displayed centered on the screen.
        # ATTENTION: The camera operates on the small_display! Remember that
        # when handling mouse input.
        offset_x = (const.SMALL_WINDOW_WIDTH // 2
                    - (self.world_width - self.world_height) / 2
                    * const.TILE_WIDTH_HALF)
        offset_y = (const.SMALL_WINDOW_HEIGHT // 2
                    - (self.world_width + self.world_height) / 2
                    * const.TILE_HEIGHT_HALF)
        self.offset = pygame.Vector2(offset_x, offset_y)

    def world_to_screen(self, world_pos):
        screen_x = (world_pos.x - world_pos.y) * const.TILE_WIDTH_HALF + self.offset.x
        screen_y = (world_pos.x + world_pos.y) * const.TILE_HEIGHT_HALF + self.offset.y
        return pygame.Vector2(screen_x, screen_y)

    def main_display_to_world(self, mouse_x, mouse_y):
        # Adapted from the code example in wikipedia:
        # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates
        # x and y are multiplied with WINDOW_SIZE_FACTOR because they are
        # main_display coordinates and must be converted to small_display coordinates.
        virt_x = ((mouse_x * const.WINDOW_SIZE_FACTOR
                   - (self.offset.x - self.world_width * const.TILE_WIDTH_HALF))
                  / const.TILE_WIDTH)
        virt_y = (mouse_y * const.WINDOW_SIZE_FACTOR - self.offset.y) / const.TILE_HEIGHT
        world_x = virt_y + (virt_x - self.world_width / 2)
        world_y = virt_y - (virt_x - self.world_height / 2)
        # Coordinates are floats. Use math.floor() to get the tile position.
        return pygame.Vector2(world_x, world_y)

    def scroll(self, rel_x, rel_y):
        # Multiply by WINDOW_SIZE_FACTOR because the mouse moves in
        # the main display but the map moves in small_display.
        self.offset.x += rel_x * const.WINDOW_SIZE_FACTOR
        self.offset.y += rel_y * const.WINDOW_SIZE_FACTOR

    def scroll_up(self):
        pass

    def scroll_right(self):
        pass

    def scroll_down(self):
        pass

    def scroll_left(self):
        pass
