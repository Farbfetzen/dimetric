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
import collections

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

Tile = collections.namedtuple(
    "Tile",
    ("type", "world_x", "world_y", "display_x", "display_y", "image")
)


class World:
    def __init__(self, world_data, name, images):
        self.name = name
        self.tiles = []
        for y, row in enumerate(world_data["map"]):
            self.tiles.append([])
            for x, i in enumerate(row):
                name = world_data["palette"][i]
                tile = Tile(name, images, x, y)
                self.tiles[y].append(tile)
        self.sidelength = len(self.tiles)
        self.check_map_square()
        self.path = self.construct_path()
        self.highlighted_tile = None

    def check_map_square(self):
        for row in self.tiles:
            if len(row) != self.sidelength:
                raise ValueError(f"Map '{self.name}' is not square!")

    def construct_path(self):
        return None

    def scroll(self, camera_offset):
        for row in self.tiles:
            for tile in row:
                tile.scroll(camera_offset)

    def highlight(self, x, y):
        x = int(x)
        y = int(y)
        if 0 <= x < self.sidelength and 0 <= y < self.sidelength:
            if self.highlighted_tile is None:
                self.highlighted_tile = self.tiles[y][x]
                self.highlighted_tile.toggle_highlight()
            elif (self.highlighted_tile.world_pos.x != x
                  or self.highlighted_tile.world_pos.y != y):
                self.highlighted_tile.toggle_highlight()
                self.highlighted_tile = self.tiles[y][x]
                self.highlighted_tile.toggle_highlight()

    def disable_highlight(self):
        if self.highlighted_tile is not None:
            self.highlighted_tile.toggle_highlight()
            self.highlighted_tile = None

    def draw(self, target_surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(target_surface)

