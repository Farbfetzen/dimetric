"""Load images, worlds, options etc. and make them accessible."""

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
import json
import pygame

from src import constants
from src import world


images = {}
worlds = {}
options = {}
default_options = {
    "controls": {
        "scroll_left": "left",
        "scroll_right": "right",
        "scroll_up": "up",
        "scroll_down": "down",
        "mouse_scroll_button_index": 2,
        "dev": "f1"
    }
}


def load_images():
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename)).convert()
        image.set_colorkey(constants.COLORKEY)
        name = os.path.splitext(filename)[0]
        images[name] = image


def load_worlds():
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            world_data = json.load(file)
            worlds[world_data["name"]] = world.World(world_data, images)


def load_options():
    if os.path.isfile("options.json"):
        with open("options.json", "r") as file:
            opt = json.load(file)
    else:
        save_options(default_options)
        opt = default_options
    options.update(opt)


def save_options(opt=None):
    if opt is None:
        opt = options
    with open("options.json", "w") as file:
        json.dump(opt, file, indent=4, sort_keys=True)
