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
from src import states
from src import button


class MainMenu(states.State):
    def __init__(self):
        super().__init__()

        self.buttons = (
            button.Button(
                "new game",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, 50),
                self.new_game,
            ),
            button.Button(
                "quit",
                (100, 50),
                (constants.SMALL_DISPLAY_WIDTH // 2, 200),
                self.close
            )
        )

    def new_game(self):
        self.persistent_state_data["world_name"] = "test"
        self.close("MainGame")

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event_manager.adjust_mouse(*event.pos)
            for b in self.buttons:
                if b.rect.collidepoint(x, y):
                    b.action()
                    break

    def update(self, dt):
        for b in self.buttons:
            b.update(self.mouse_pos)

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))
        for b in self.buttons:
            target_surface.blit(b.image, b.rect)


