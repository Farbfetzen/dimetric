"""Options for the game."""

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


options = {}

# TODO: Make an inputmanager that takes the controls from the options and
#  manages input into the game. Should also allow rebinding of actions through
#  an options menu. But hide the dev overlay toggle key from that menu.
default_options = {
    "controls": {
        "scroll_left": pygame.K_LEFT,
        "scroll_right": pygame.K_RIGHT,
        "scroll_up": pygame.K_UP,
        "scroll_down": pygame.K_DOWN,
        "mouse_scroll_button_index": 2
    }
}


def load_options():
    if os.path.isfile("options.json"):
        with open("options.json", "r") as file:
            opt = json.load(file)
        # TODO: Maybe validate the loaded dictionary. Are the keys all there?
        #  Do the values make sense? Are there unexpected Keys? If something
        #  does not fit just overwrite it with the default and log the incident.
        #  This is not that important but would be an interesting exercise.
    else:
        with open("options.json", "w") as file:
            json.dump(default_options, file, indent=4, sort_keys=True)
        opt = default_options
    options.update(opt)
