"""Manage the inputs and events for the game."""

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


import pygame

from src import constants
from src import options


# TODO: import the controls from the options and make them easily available to
#  the game states so each state can check of one of its relevant events
#  was triggered.

class EventManager:
    def __init__(self):
        self.events = []
        self.mouse_pos = pygame.Vector2()  # Always update, never replace!

        # TODO: Get the keys from the options.

    def update(self):
        self.events = pygame.event.get()
        self.mouse_pos.update(pygame.mouse.get_pos())
        self.mouse_pos //= constants.MAGNIFICATION
