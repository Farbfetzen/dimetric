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

from src.states.state import State
from src import button


class OptionsMenu(State):
    def __init__(self, game):
        super().__init__(game)

        # TODO: Create text fields and input fields which allow users to
        #  modify keybindings.
        self.buttons = ()

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.close("main menu")

    def update(self, dt):
        for b in self.buttons:
            b.update(self.mouse_pos)

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))
        for b in self.buttons:
            target_surface.blit(b.image, b.rect)
