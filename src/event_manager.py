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
from src import resources


class EventManager:
    def __init__(self):
        self.events = []
        self.mouse_pos = pygame.Vector2()  # Always update, never replace.

        controls = resources.options["controls"]
        self.k_escape = pygame.K_ESCAPE
        self.k_scroll_left = pygame.key.key_code(controls["scroll_left"])
        self.k_scroll_right = pygame.key.key_code(controls["scroll_right"])
        self.k_scroll_up = pygame.key.key_code(controls["scroll_up"])
        self.k_scroll_down = pygame.key.key_code(controls["scroll_down"])
        self.mouse_scroll_button_index = controls["mouse_scroll_button_index"]
        self.k_dev = pygame.key.key_code(controls["dev"])

    def update(self):
        self.events = pygame.event.get()
        self.mouse_pos.update(pygame.mouse.get_pos())
        self.mouse_pos //= constants.MAGNIFICATION
