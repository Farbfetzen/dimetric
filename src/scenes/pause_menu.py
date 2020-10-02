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


from src.scenes.scene import Scene
from src.button import Button
from src import constants


class PauseMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # Copy the small display so that the main game is visible
        # in the background:
        self.surface = pygame.Surface(constants.SMALL_DISPLAY_SIZE, pygame.SRCALPHA)

        self.rect = pygame.Rect(
            0,
            0,
            constants.SMALL_DISPLAY_WIDTH // 3,
            constants.SMALL_DISPLAY_HEIGHT // 2
        )
        self.rect.center = self.surface.get_rect().center
        radius = 10
        pygame.draw.rect(self.surface, (0, 0, 0), self.rect, border_radius=radius)
        pygame.draw.rect(self.surface, (250, 250, 250), self.rect, 1, border_radius=radius)

        self.buttons = (
            Button(
                "Resume",
                (50, 25),
                (self.rect.centerx, self.rect.y + 25),
                self.resume_game
            ),
            Button(
                "Quit",
                (50, 25),
                (self.rect.centerx, self.rect.bottom - 25),
                self.goto_main_menu
            )
            # TODO: add button for option menu
        )

    def process_event(self, event, event_manager):
        block = super().process_event(event, event_manager)
        if block:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.resume_game()
                return True

    def update(self, dt):
        super().update(dt)
        return True

    def draw(self):
        for b in self.buttons:
            self.surface.blit(b.image, b.rect)
        self.target_surface.blit(self.surface, (0, 0))

    def resume_game(self):
        self.close()

    def goto_main_menu(self):
        # TODO: Warn that unsaved changes will be lost. Ask if user wants to
        #  save them.
        self.close("main menu", remove_all=True)
