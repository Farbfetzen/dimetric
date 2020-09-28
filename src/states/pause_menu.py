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
from src.button import Button
from src import constants


class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)

        self.rect = pygame.Rect(
            0,
            0,
            constants.SMALL_DISPLAY_WIDTH // 3,
            constants.SMALL_DISPLAY_HEIGHT // 2
        )
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, (255, 255, 255), self.rect, 1)

        self.buttons = (
            Button(
                "Resume",
                (50, 25),
                (self.rect.centerx, 25),
                self.resume_game
            ),
            Button(
                "Quit",
                (50, 25),
                (self.rect.centerx, self.rect.height - 25),
                self.close
            )
        )

        self.rect.center = (
            constants.SMALL_DISPLAY_WIDTH // 2,
            constants.SMALL_DISPLAY_HEIGHT // 2
        )
        for b in self.buttons:
            b.rect.x += self.rect.x
            b.rect.y += self.rect.y

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.resume_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event_manager.adjust_mouse(*event.pos)
            for b in self.buttons:
                if b.rect.collidepoint(x, y):
                    b.action()
                    break

    def update(self, dt):
        for b in self.buttons:
            b.update(self.mouse_pos)

    def draw(self, target_surface):
        for b in self.buttons:
            self.surface.blit(b.image, b.blit_pos)
        target_surface.blit(self.surface, self.rect)

    def resume_game(self):
        self.close("main game")
