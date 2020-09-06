"""Tile and world class."""

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


import math
from collections import namedtuple

import pygame

import src.constants as const


# class Tile:
#     def __init__(self, name, images, x, y):
#         self.name = name
#         self.images = images
#         self.image = images[name]
#         self.is_highlighted = False
#         self.rect = self.image.get_rect()
#         self.world_pos = pygame.Vector2(math.floor(x), math.floor(y))
#         # The difference from the camera_offset in small_display coordinates:
#         self.offset = pygame.Vector2()
#         self.offset.x = (self.world_pos.x - self.world_pos.y) * const.TILE_WIDTH_HALF
#         self.offset.y = (self.world_pos.x + self.world_pos.y) * const.TILE_HEIGHT_HALF
#         # Account for images taller than TILE_HEIGHT, like platforms and such.
#         # The -1 is because the base rhombus is const.TILE_HEIGHT + 1 tall.
#         self.offset.y -= self.rect.height - const.TILE_HEIGHT - 1
#
#     def toggle_highlight(self):
#         self.is_highlighted = not self.is_highlighted
#         if self.is_highlighted:
#             self.image = self.images[self.name + "_highlight"]
#         else:
#             self.image = self.images[self.name]
#
#     def scroll(self, camera_offset):
#         self.rect.midtop = self.offset + camera_offset
#
#     def draw(self, target_surface):
#         target_surface.blit(self.image, self.rect)


class World:
    def __init__(self, world_data, images):
        self.name = world_data["name"]
        self.sidelength = len(world_data["map"])

        # Check if map is square:
        for row in world_data["map"]:
            if len(row) != len(world_data["map"]):
                raise ValueError(f"Map '{self.name}' is not square.")

        # Add a margin of some tile sizes so other stuff fits on the world surface, too.
        margin_x = const.TILE_WIDTH * 2
        margin_y = const.TILE_HEIGHT * 5
        self.surf_width = self.sidelength * const.TILE_WIDTH + margin_x
        self.surf_height = self.sidelength * const.TILE_HEIGHT + margin_y
        self.surface = pygame.Surface((self.surf_width, self.surf_height))

        # Center the map on the world surface. Offset is the position of
        # (0, 0) world coordinates on the world surface.
        self.offset_x = self.surf_width // 2
        self.offset_y = (self.surf_height // 2
                         - self.sidelength * const.TILE_HEIGHT_HALF)

        self.rect = self.surface.get_rect()
        self.rect.center = (const.SMALL_DISPLAY_WIDTH / 2, const.SMALL_DISPLAY_HEIGHT / 2)
        self.surf_pos = pygame.Vector2(self.rect.topleft)  # for scrolling

        self.tiles = []  # Used for blitting
        self.tiles_nested = []  # Useful for finding a tile by world coordinates
        Tile = namedtuple(
            "Tile",
            ("type", "image", "world_x", "world_y", "topleft")
        )
        path_start = None
        path_end = None
        self.path_raw = set()
        for world_y, row in enumerate(world_data["map"]):
            self.tiles_nested.append([])
            for world_x, symbol in enumerate(row):
                tile_type = world_data["palette"][symbol]
                if tile_type == "path":
                    pos = (world_x, world_y)
                    self.path_raw.add(pos)
                    if symbol == "S":
                        path_start = pos
                        self.path_raw.remove(pos)
                    elif symbol == "E":
                        path_end = pos
                image = images[tile_type]
                x, y = self.world_pos_to_world_surf(world_x, world_y)
                x -= image.get_width() / 2
                y -= image.get_height() - const.TILE_HEIGHT
                tile = Tile(tile_type, image, world_x, world_y, (x, y))
                self.tiles_nested[world_y].append(tile)
                self.tiles.append(tile)

        if path_start is None or path_end is None:
            raise ValueError(f"Missing path start or end in map '{self.name}'.")
        self.path = [path_start]
        while self.path_raw:
            x, y = self.path[-1]
            for neighbor in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if neighbor in self.path_raw:
                    self.path.append(neighbor)
                    self.path_raw.remove(neighbor)
                    break
            else:
                raise ValueError(f"Malformed path in map '{self.name}': Neighbor not found.")
        if self.path[-1] != path_end:
            raise ValueError(f"Malformed path in map '{self.name}': Ends at wrong position.")

    def world_pos_to_world_surf(self, world_x, world_y):
        # ATTENTION: Remember to account for the width and height of a sprite
        #   before blitting.
        x = (world_x - world_y) * const.TILE_WIDTH_HALF + self.offset_x
        y = (world_x + world_y) * const.TILE_HEIGHT_HALF + self.offset_y
        return x, y

    def small_display_to_world_pos(self, x, y):
        # Adapted from the code example in wikipedia:
        # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates

        # Remember: Coordinates are floats. If you want to allow negative
        # tile positions then you must use math.floor() and not int().
        # int() rounds towards zero which would introduce an off-by-one error
        # for negative tile positions.

        # Get x and y relative to the topleft corner of the bounding rectangle
        # of the map:
        x = x - self.rect.x - self.offset_x + self.sidelength * const.TILE_WIDTH_HALF
        y = y - self.rect.y - self.offset_y

        virt_x = x / const.TILE_WIDTH
        virt_y = y / const.TILE_HEIGHT
        world_x = virt_y + (virt_x - self.sidelength / 2)
        world_y = virt_y - (virt_x - self.sidelength / 2)
        return world_x, world_y

    def get_at(self, x, y):
        return self.tiles_nested[y][x]

    def scroll(self, rel_x, rel_y):
        # Multiply by ZOOM_FACTOR because the mouse moves in
        # the main display but the map moves in small_display.
        # Use surf_pos to track the floating point possition because
        # rects can only hold integers.
        self.surf_pos.x += rel_x * const.ZOOM_FACTOR
        self.surf_pos.y += rel_y * const.ZOOM_FACTOR
        self.rect.topleft = self.surf_pos

    def draw(self, target_surface):
        blit_list = [(tile.image, tile.topleft) for tile in self.tiles]
        self.surface.blits(blit_list, False)

        target_surface.blit(self.surface, self.rect)
