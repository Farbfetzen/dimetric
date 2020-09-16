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

from src import settings
from src import world


images = {}
worlds = {}


def load_images():
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey(settings.COLORKEY)
        name = os.path.splitext(filename)[0]
        images[name] = image


def load_worlds():
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            world_data = json.load(file)
            worlds[world_data["name"]] = world.World(world_data, images)
