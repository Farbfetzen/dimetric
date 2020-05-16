"""Load all the resources like images, maps, etc."""

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
import pygame


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


def load_map(config):
    tiles = []
    tile_offsets = []
    maps = {}
    for filename in os.listdir("maps"):
        with open(os.path.join("maps", filename), "r") as file:
            map_data = json.load(file)
        print(map_data)

        # Wie am besten Speichern? Mach einfach eine Liste mit einfachen
        # Sprite-Objekten. Am Ende kommt zum blitten sowieso alles in eine große
        # Liste und wird nach x und y sortiert.
        # Jedes map-tile kennt seine position auf Karte und Bildschirm,
        # seine Tile-Abmessungen, Offsets und hat eine Referenz zur Surface.
        # Aber eine eigene Klasse wäre overkill. Die machen ja nichts und sind
        # alle gleich. daher wäre namedtuple besser und sparsamer.
        # Wenn die Karte verschoben wird, ändert sich zwar die
        # Bildschirmposition, aber das kann man mit dem Karten-Offset neu
        # berechnen. Muss man sowieso in jedem Frame für die beweglichen Objekte.

        # tile = pygame.image.load(os.path.join("images", filename)).convert()
        # tile.set_colorkey(COLORKEY)
        # tiles.append(tile)
        # tile_offsets.append((
        #     TILE_WIDTH - tile.get_width(),
        #     TILE_HEIGHT - tile.get_height()
        # ))

