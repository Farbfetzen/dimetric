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


from typing import Any, Dict

import pygame


class State:
    def __init__(self) -> None:
        self.done = False

        self.dev_overlay_visible = True
        # These must be defined here and not in constants.py because they need
        # pygame to be initialized for the fonts to work,
        self.dev_font = pygame.font.SysFont("monospace", 18)
        self.dev_line_hight = self.dev_font.get_height()
        self.dev_color = (255, 255, 255)
        self.dev_margin = pygame.Vector2(10, 10)

    def start(self, persistent_state_data: Dict[str, Any]) -> None:
        """Start or resume a state.
        Use the information provided by the previous state to set up
        this state.
        """
        self.done = False

    def close(self) -> dict:
        """Quit or suspend a state.
        Use this for cleanup. Save relevant data in persistent_state_data to
        pass it to the next state. Set next_state_name to "quit" to
        immediately quit the app.
        """
        persistent_state_data = {"next_state_name": "quit"}
        return persistent_state_data

    def process_events(self, events: list) -> None:
        raise NotImplementedError

    def update(self, dt: float) -> None:
        raise NotImplementedError

    def draw(self, target_surface: pygame.Surface) -> None:
        raise NotImplementedError
