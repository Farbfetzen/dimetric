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

import src.constants as const


class Tile:
    def __init__(self, name, image, world_x, world_y, screen_x, screen_y):
        self.name = name
        self.image = image
        self.world_x = world_x
        self.world_y = world_y
        self.screen_x = screen_x
        self.screen_y = screen_y


def _load_images():
    images = {}
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey(const.COLORKEY)
        name = os.path.splitext(filename)[0]
        images[name] = image
    return images


def _build_worlds(images):
    worlds = {}
    # FIXME: Check if the world stores references to the tile surfaces or
    #     if it makes copies of the surfaces. Because the latter would be
    #     a waste of resources.
    world_obj = namedtuple("world", ["tiles", "width", "height", "path"])
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            world_data = json.load(file)
            tiles = []
            for world_y, row in enumerate(world_data["map"]):
                for world_x, i in enumerate(row):
                    tile_name = world_data["palette"][i]
                    x, y = world_to_screen(
                        world_x, world_y,
                        const.TILE_WIDTH - image.get_width() + 1,
                        const.TILE_HEIGHT - image.get_height() + 1
                    )
                    tile = Tile(tile_name, images[tile_name], world_x, world_y, x, y)
                    tiles.append(tile)

                    # FIXME: Is this correct? (0, 0) should translate to (-1, -1)
                    #     and not (-2, -1) because that would be one pixel too far
                    #     to the right. So this is why there are "+1" offsets above.
                    # print(world_x, world_y, x, y)

            # TODO: construct complete enemy path in separate function
            path = (world_data["path_start"], world_data["path_end"])

            name = os.path.splitext(filename)[0]
            worlds[name] = world_obj(
                tiles=tiles,
                width=world_x + 1,
                height=world_y + 1,
                path=path
            )
    return worlds


# The display must be created before loading images:
display = pygame.display.set_mode(const.WINDOW_SIZE)
small_display = pygame.Surface(const.SMALL_WINDOW_SIZE)

images = _load_images()
worlds = _build_worlds(images)
