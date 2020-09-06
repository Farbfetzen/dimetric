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

import src.camera
import src.constants as const
import src.world


def _load_images():
    images_ = {}
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey(const.COLORKEY)
        name = os.path.splitext(filename)[0]
        images_[name] = image
        images_[name + "_highlight"] = _highlight_image(image)
    return images_


def _highlight_image(image):
    """Replace the grey outline with orange to highlight a tile."""
    highlighted = image.copy()
    pygame.transform.threshold(
        highlighted,
        image,
        const.OUTLINE_COLOR,
        set_color=const.HIGHLIGHT_COLOR,
        inverse_set=True
    )
    return highlighted


def _build_worlds(images_):
    worlds_ = {}
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            name = os.path.splitext(filename)[0]
            world_data = json.load(file)
            # Check if map is square:
            for row in world_data["map"]:
                if len(row) != len(world_data["map"]):
                    raise ValueError(f"Map '{name}' is not square!")
            worlds_[name] = src.world.World(world_data, name, images_)
    return worlds_


# The display must be created before loading images:
main_display = pygame.display.set_mode(const.MAIN_DISPLAY_SIZE)
small_display = pygame.Surface(const.SMALL_DISPLAY_SIZE)
clock = pygame.time.Clock()

images = _load_images()
worlds = _build_worlds(images)
