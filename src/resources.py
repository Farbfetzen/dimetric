"""Load images, maps, config etc. and make them accessible."""

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
from src.coordinate_conversion import map_to_screen


def _load_images():
    images = {}
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey(const.COLORKEY)
        name = os.path.splitext(filename)[0]
        images[name] = image
    return images


def _build_maps(images):
    maps = {}
    Tile = namedtuple("tile", [
        "type", "image",
        "map_x", "map_y",
        "x", "y"
    ])
    # FIXME: Check if the map stores references to the tile surfaces or
    #     if it makes copies of the surfaces. Because the latter would be
    #     a waste of resources.
    map_obj = namedtuple("map", ["tiles", "width", "height", "path"])
    for filename in os.listdir("maps"):
        with open(os.path.join("maps", filename), "r") as file:
            map_data = json.load(file)
            tiles = []
            for map_y, row in enumerate(map_data["map"]):
                for map_x, i in enumerate(row):
                    tile_name = map_data["palette"][i]
                    image = images[tile_name]
                    x, y = map_to_screen(
                        map_x, map_y,
                        const.TILE_WIDTH - image.get_width(),
                        const.TILE_HEIGHT - image.get_height(),
                        0, 0
                    )
                    tile = Tile(tile_name, image, map_x, map_y, x, y)
                    tiles.append(tile)

            # TODO: construct complete enemy path in separate function
            path = (map_data["path_start"], map_data["path_end"])

            name = os.path.splitext(filename)[0]
            maps[name] = map_obj(
                tiles=tiles,
                width=map_x + 1,
                height=map_y + 1,
                path=path
            )
    return maps


# The display must be created before loading images:
display = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
images = _load_images()
maps = _build_maps(images)
