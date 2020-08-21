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

import src.constants as const


class Tile:
    def __init__(self,
                 name, image,
                 world_x, world_y,
                 camera_offset_x=0,  camera_offset_y=0):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.world_x = 0
        self.world_y = 0
        # The difference from the camera_offset in small_display coordinates:
        self.screen_offset_x = 0
        self.screen_offset_y = 0
        # Account for images taller than TILE_HEIGHT, like platforms and such.
        # The -1 is because the base rhombus is const.TILE_HEIGHT + 1 tall.
        self.tile_offset_y = self.rect.height - const.TILE_HEIGHT - 1

        self.update_position(world_x, world_y, camera_offset_x, camera_offset_y)

    def scroll(self, camera_offset_x, camera_offset_y):
        self.rect.midtop = (
            self.screen_offset_x + camera_offset_x,
            self.screen_offset_y + camera_offset_y
        )

    def update_position(self, world_x, world_y, camera_offset_x, camera_offset_y):
        # Update screen and world positions.
        self.world_x = math.floor(world_x)
        self.world_y = math.floor(world_y)
        self.screen_offset_x = (self.world_x - self.world_y) * const.TILE_WIDTH_HALF
        self.screen_offset_y = ((self.world_x + self.world_y) * const.TILE_HEIGHT_HALF
                                - self.tile_offset_y)
        self.scroll(camera_offset_x, camera_offset_y)

    def draw(self, target_surface):
        target_surface.blit(self.image, self.rect)


class World:
    def __init__(self, world_data, name, images):
        self.name = name
        self.tiles = []
        for y, row in enumerate(world_data["map"]):
            self.tiles.append([])
            for x, i in enumerate(row):
                name = world_data["palette"][i]
                tile = Tile(name, images[name], x, y)
                self.tiles[y].append(tile)
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)
        self.check_map_rectangular()
        self.path = []
        self.highlight = None

    def check_map_rectangular(self):
        for row in self.tiles[1:]:
            if len(row) != self.width:
                raise ValueError(f"Map '{self.name}' is not rectangular!")

    def construct_path(self):
        pass

    def scroll(self, camera_offset_x, camera_offset_y):
        for row in self.tiles:
            for tile in row:
                tile.scroll(camera_offset_x, camera_offset_y)

    def highlight(self, x, y):
        pass

    def draw(self, target_surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(target_surface)


# world_data = json.load(file)
# map_ = world_data["map"]
# check_map_rectangular(map_, filename)
# tiles = []
# world_width = len(map_[0])  # towards bottom right
# world_height = len(map_)  # towards bottom left
# for world_y, row in enumerate(map_):
#     for world_x, i in enumerate(row):
#         tile = src.tile_world.Tile(
#             images_[world_data["palette"][i]],
#             world_x, world_y
#         )
#         tiles.append(tile)
# # TODO: construct complete enemy path in separate function
# path = (world_data["path_start"], world_data["path_end"])
