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
import src.tile


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
            world_width = len(map_[0])  # towards bottom right
            world_height = len(map_)  # towards bottom left
            camera = src.camera.Camera(world_width, world_height)
            for world_y, row in enumerate(map_):
                for world_x, i in enumerate(row):
                    tile_type = world_data["palette"][i]
                    tile = src.tile.Tile(
                        world_data["palette"][i], images_[tile_type],
                        world_x, world_y,
                        camera.offset_x, camera.offset_y
                    )
                    tiles.append(tile)
            # TODO: construct complete enemy path in separate function
            path = (world_data["path_start"], world_data["path_end"])

            name = os.path.splitext(filename)[0]
            worlds_[name] = world_obj(
                tiles=tiles,
                width=world_width,
                height=world_height,
                path=path
            )
    return worlds_


# The display must be created before loading images:
main_display = pygame.display.set_mode(const.WINDOW_SIZE)
small_display = pygame.Surface(const.SMALL_WINDOW_SIZE)
clock = pygame.time.Clock()

images = _load_images()
worlds = _build_worlds(images)
