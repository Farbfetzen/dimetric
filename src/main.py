"""Main loop."""

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


import json
import os
from collections import namedtuple
import pygame

from src.coordinate_conversion import map_to_screen
import src.constants as const
from src.states.main_game import MainGame


def load_sprites():
    sprites = {}
    for filename in os.listdir("sprites"):
        sprite = pygame.image.load(os.path.join("sprites", filename)).convert()
        sprite.set_colorkey(const.COLORKEY)
        name = os.path.splitext(filename)[0]
        sprites[name] = sprite
    return sprites


def load_maps(sprites):
    maps = {}
    Tile = namedtuple("tile", [
        "type", "surface",
        "map_x", "map_y",
        "x", "y"
    ])
    map_obj = namedtuple("map", ["tiles", "width", "height"])
    for filename in os.listdir("maps"):
        with open(os.path.join("maps", filename), "r") as file:
            map_data = json.load(file)
            map_data["IDs"] = {int(k): v for k, v in map_data["IDs"].items()}
            tiles = []
            for map_y, row in enumerate(map_data["map"]):
                for map_x, i in enumerate(row):
                    tile_name = map_data["IDs"][i]
                    sprite = sprites[tile_name]
                    x, y = map_to_screen(
                        map_x, map_y,
                        const.TILE_WIDTH - sprite.get_width(),
                        const.TILE_HEIGHT - sprite.get_height(),
                        0, 0
                    )
                    tile = Tile(tile_name, sprite, map_x, map_y, x, y)
                    tiles.append(tile)
            name = os.path.splitext(filename)[0]
            maps[name] = map_obj(tiles=tiles, width=map_x + 1, height=map_y + 1)
    return maps


def run():
    pygame.init()
    display = pygame.display.set_mode(
        (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
    )

    sprites = load_sprites()
    maps = load_maps(sprites)
    data = {
        "sprites": sprites,
        "maps": maps
    }

    states = {"MainGame": MainGame(data, "test")}
    state = states["MainGame"]

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(const.FPS)

        if pygame.event.get(pygame.QUIT):
            break
        else:
            state.process_events()

        if state.done:
            persistent_state_data = state.close()
            next_state_name = persistent_state_data["next_state_name"]
            if next_state_name == "quit":
                break
            state = states[next_state_name]
            state.start(persistent_state_data)

        state.update(dt)

        state.draw(display)
        pygame.display.flip()
