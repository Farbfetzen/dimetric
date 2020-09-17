"""Manage the inputs for the game."""

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


import enum

import pygame

from src import options


class Actions(enum.Enum):
    SCROLL_LEFT = enum.auto()
    SCROLL_RIGHT = enum.auto()
    SCROLL_UP= enum.auto()
    SCROLL_DOWN= enum.auto()


# Goal: Reduce repetion across game states.
# But don't make it needlessly complicated.
# Another benefit would be the possibility to get the events once and then
#   give them to all active game states, if I ever decide to enable multiple
#   concurrently active states.

class InputManager:
    def __init__(self):
        self.events = []
        # TODO: Get the keys from the options.

    def update(self):
        self.events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                # ...
                pass
            # ...

        # 1. Iterate over the pygame events.
        # 2. For each event check if it corresponds to one of the controls in the options.
        # 3. If it does, add it to a list. Remember to clear this list before each frame.
        # 4. A game states goes over all events in that list, checks if the event is relevant, and acts accordingly.
        # Maybe use an enum (auto) for the events? Just some type that can be easily compared.
        # Inside the main_game state:
        # for event in events:
        #     if event == inputs.SCROLL_LEFT:
        #         # scroll the map left
        # where inputs.SCROLL_LEFT would be an enum.
        # Also handle the mouse: position, rel, buttons (mousebuttondown and during mousemotion)
        #
        # This would also be a good place to apply the magnification to the
        # mouse coordinates and movement. Otherwise this has to be done in
        # every game state.
        return self.events
