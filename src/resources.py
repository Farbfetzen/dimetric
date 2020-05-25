"""Load sprites, maps, config etc. and make them accessible."""

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


def _load_sprites():
    sprites = {}
    for filename in os.listdir("sprites"):
        sprite = pygame.image.load(os.path.join("sprites", filename)).convert()
        sprite.set_colorkey(const.COLORKEY)
        name = os.path.splitext(filename)[0]
        sprites[name] = sprite
    return sprites


def _load_maps(sprites):
    maps = {}
    Tile = namedtuple("tile", [
        "type", "surface",
        "map_x", "map_y",
        "x", "y"
    ])
    # FIXME: Check if the map stores references to the tile surfaces or
    #  if it makes copies of the surfaces. Because the latter would be a waste
    #  of resources.
    map_obj = namedtuple("map", ["tiles", "width", "height", "path"])
    for filename in os.listdir("maps"):
        with open(os.path.join("maps", filename), "r") as file:
            map_data = json.load(file)
            tiles = []
            for map_y, row in enumerate(map_data["map"]):
                for map_x, i in enumerate(row):
                    tile_name = map_data["types"][i]
                    sprite = sprites[tile_name]
                    x, y = map_to_screen(
                        map_x, map_y,
                        const.TILE_WIDTH - sprite.get_width(),
                        const.TILE_HEIGHT - sprite.get_height(),
                        0, 0
                    )
                    tile = Tile(tile_name, sprite, map_x, map_y, x, y)
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
sprites = _load_sprites()

maps = _load_maps(sprites)
