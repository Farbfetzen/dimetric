"""Camer object controlling coordinate conversions."""

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


# World coordinates should be similar in dimension to screen coordinates. This
# will make movement and collision detection easier because the collision rects
# will live in world coordinates. Maybe make one tile edge 10 or 100 long? it
# should not matter much because of the conversion.


import src.constants as const


class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height

        # Start centered on the world center:
        self.offset_x = const.SMALL_WINDOW_WIDTH // 2 - const.TILE_WIDTH_HALF
        self.offset_y = const.SMALL_WINDOW_HEIGHT // 2 - const.TILE_HEIGHT_HALF * self.world_height

    def world_to_screen(self, world_x, world_y):
        # FIXME: The map is not centered for rectangular maps, e.g. 8 wide, 9 tall.
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

    def scroll_up(self):
        pass

    def scroll_right(self):
        pass

    def scroll_down(self):
        pass

    def scroll_left(self):
        pass
