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
        controls = resources.options["controls"]
        self.k_escape = pygame.K_ESCAPE
        self.k_scroll_left = pygame.key.key_code(controls["scroll_left"])
        self.k_scroll_right = pygame.key.key_code(controls["scroll_right"])
        self.k_scroll_up = pygame.key.key_code(controls["scroll_up"])
        self.k_scroll_down = pygame.key.key_code(controls["scroll_down"])
        self.mouse_map_scroll_button_index = controls["mouse_scroll_button_index"]
        self.k_dev = pygame.key.key_code(controls["dev"])

    def process_events(self, state):
        # Looping through the events here and sending them to the game states
        # may make it easier to implement multiple concurrently active states
        # in the future. In that case this method would accept a list of states
        # and send each event to all states. If one state found it useful then
        # the other states should not get the event.
        state.mouse_pos.update(self.adjust_mouse(*pygame.mouse.get_pos()))
        for event in pygame.event.get():
            state.process_event(event, self)

    @staticmethod
    def adjust_mouse(x, y):
        """ Convert mouse position and relative movement to
        small_display coordinates.
        """
        return x / constants.MAGNIFICATION, y / constants.MAGNIFICATION
