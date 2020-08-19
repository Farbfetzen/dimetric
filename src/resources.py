"""Load images, worlds, config etc. and make them accessible."""

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

import os
import pygame
import json
from collections import namedtuple

import src.camera
import src.constants as const


class Tile:
    def __init__(self,
                 type_, image,
                 offset_x, offset_y,
                 world_x, world_y,
                 camera_offset_x, camera_offset_y):
        self.type = type_
        self.image = image
        # offset_* = difference between the rhombus of the tile base and image:
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.world_x = world_x
        self.world_y = world_y
        self.screen_x = 0
        self.screen_y = 0

        self.a = (self.world_x - self.world_y) * const.TILE_WIDTH_HALF + self.offset_x
        self.b = (self.world_x + self.world_y) * const.TILE_HEIGHT_HALF + self.offset_y

        self.update_screen_xy(camera_offset_x, camera_offset_y)

    def update_screen_xy(self, camera_offset_x, camera_offset_y):
        self.screen_x = self.a + camera_offset_x
        self.screen_y = self.b + camera_offset_y


def _load_images():
    images_ = {}
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey(const.COLORKEY)
        name = os.path.splitext(filename)[0]
        images_[name] = image
    return images_


def check_map_rectangular(map_, name):
    length = len(map_[0])
    for row in map_[1:]:
        if len(row) != length:
            raise ValueError(f"Map '{name}' is not rectangular!")


def _build_worlds(images_):
    worlds_ = {}
    # FIXME: Check if the world stores references to the tile surfaces or
    #     if it makes copies of the surfaces. Because the latter would be
    #     a waste of resources.
    world_obj = namedtuple("world", ["tiles", "width", "height", "path"])
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            world_data = json.load(file)
            map_ = world_data["map"]
            check_map_rectangular(map_, filename)
            tiles = []
            camera = src.camera.Camera(len(map_), len(map_[0]))
            for world_y, row in enumerate(map_):
                for world_x, i in enumerate(row):
                    tile_type = world_data["palette"][i]
                    tile_image = images_[tile_type]
                    tile = Tile(
                        tile_type, images_[tile_type],
                        const.TILE_WIDTH - tile_image.get_width() + 1,
                        const.TILE_HEIGHT - tile_image.get_height() + 1,
                        world_x, world_y,
                        camera.offset_x, camera.offset_y
                    )
                    tiles.append(tile)

                    # FIXME: Is this correct? (0, 0) should translate to (-1, -1)
                    #     and not (-2, -1) because that would be one pixel too far
                    #     to the right. So this is why there are "+1" offsets above.
                    # print(world_x, world_y, x, y)

            # TODO: construct complete enemy path in separate function
            path = (world_data["path_start"], world_data["path_end"])

            name = os.path.splitext(filename)[0]
            worlds_[name] = world_obj(
                tiles=tiles,
                width=world_x + 1,
                height=world_y + 1,
                path=path
            )
    return worlds_


# The display must be created before loading images:
display = pygame.display.set_mode(const.WINDOW_SIZE)
small_display = pygame.Surface(const.SMALL_WINDOW_SIZE)

images = _load_images()
worlds = _build_worlds(images)
