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


import src.constants as const


class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height

        # The camera offset is the top of the base of the topmost tile.
        # The world starts displayed centered on the screen.
        self.offset_x = (const.SMALL_WINDOW_WIDTH // 2
                         - (self.world_width - self.world_height) / 2
                         * const.TILE_WIDTH_HALF)
        self.offset_y = (const.SMALL_WINDOW_HEIGHT // 2
                         - (self.world_width + self.world_height) / 2
                         * const.TILE_HEIGHT_HALF)

    def world_to_screen(self, world_x, world_y):
        screen_x = (world_x - world_y) * const.TILE_WIDTH_HALF + self.offset_x
        screen_y = (world_x + world_y) * const.TILE_HEIGHT_HALF + self.offset_y
        return screen_x, screen_y

    def screen_to_world(self):
        # # Adapted from the code example in wikipedia:
        # # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates
        # virt_x = (screen_x - (OFFSET_X - (len(world_data) - 1) * TILE_WIDTH_HALF)) / TILE_WIDTH
        # virt_y = (screen_y - OFFSET_Y) / TILE_HEIGHT
        # world_x = floor(virt_y + (virt_x - len(world_data[0]) / 2))
        # world_y = floor(virt_y - (virt_x - len(world_data) / 2))
        # # Coordinates are floats. Use int() to get the tile position in the world data.
        # # Strictly speaking it should be rounded down but int() rounds towards zero.
        # # Rounding down will result in the correct coordinates even if
        # # the world coordinates are negative.
        # return world_x, world_y
        pass

    def scroll(self, rel_x, rel_y):
        # Multiply by WINDOW_SIZE_FACTOR because the mouse moves in
        # the main display but the map moves in small_display.
        self.offset_x += rel_x * const.WINDOW_SIZE_FACTOR
        self.offset_y += rel_y * const.WINDOW_SIZE_FACTOR

    def scroll_up(self):
        pass

    def scroll_right(self):
        pass

    def scroll_down(self):
        pass

    def scroll_left(self):
        pass
