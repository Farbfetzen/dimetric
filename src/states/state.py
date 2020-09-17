"""Game state super class."""

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


class State:
    def __init__(self):
        self.done = False

        self.dev_overlay_visible = True
        self.dev_font = pygame.font.SysFont("monospace", 18)
        self.dev_line_hight = self.dev_font.get_height()
        self.dev_color = (255, 255, 255)
        self.dev_margin = pygame.Vector2(10, 10)

    def resume(self, persistent_state_data):
        """Resume an already instantiated state.
        Use the information provided by the previous state to modify
        this state.
        """
        self.done = False

    def close(self):
        """Quit or suspend a state.
        Use this for cleanup. Save relevant data in persistent_state_data to
        pass it to the next state. Set next_state_name to "quit" to
        immediately quit the app.
        """
        persistent_state_data = {"next_state_name": "quit"}
        return persistent_state_data

    def process_events(self, events):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def draw(self, target_surface):
        raise NotImplementedError
