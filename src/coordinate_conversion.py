"""Translate between map coordinates and pixel coordinates."""

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


from src.constants import TILE_WIDTH_HALF, TILE_HEIGHT_HALF


def map_to_screen(map_x, map_y,
                  offset_x=0, offset_y=0,
                  camera_offset_x=0, camera_offset_y=0):
    x = (map_x - map_y) * TILE_WIDTH_HALF + offset_x + camera_offset_x
    y = (map_x + map_y) * TILE_HEIGHT_HALF + offset_y + camera_offset_y
    return x, y


# def screen_to_map(screen_x, screen_y):
#     # Adapted from the code example in wikipedia:
#     # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates
#     virt_x = (screen_x - (OFFSET_X - (len(map_data) - 1) * TILE_WIDTH_HALF)) / TILE_WIDTH
#     virt_y = (screen_y - OFFSET_Y) / TILE_HEIGHT
#     map_x = floor(virt_y + (virt_x - len(map_data[0]) / 2))
#     map_y = floor(virt_y - (virt_x - len(map_data) / 2))
#     # Coordinates are floats. Use int() to get the tile position in the map data.
#     # Strictly speaking it should be rounded down but int() rounds towards zero.
#     # Rounding down will result in the correct coordinates even if
#     # the map coordinates are negative.
#     return map_x, map_y
