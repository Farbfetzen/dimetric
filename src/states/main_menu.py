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
from src.states.state import State


class MainMenu(State):
    def __init__(self):
        super().__init__()

        # TODO: Make a button class. This here is just quick and dirty.
        self.start_rect = pygame.Rect(0, 0, 100, 50)
        self.start_surf = pygame.Surface(self.start_rect.size)
        self.start_surf.fill((0, 0, 0))
        pygame.draw.rect(self.start_surf, self.dev_color, self.start_rect, 1)
        start_text = self.dev_font.render("new game", False, self.dev_color)
        start_text_rect = start_text.get_rect()
        start_text_rect.center = self.start_rect.center
        self.start_surf.blit(start_text, start_text_rect)
        self.start_rect.center = constants.SMALL_DISPLAY_WIDTH // 2, 50

        self.quit_rect = pygame.Rect(0, 0, 100, 50)
        self.quit_surf = pygame.Surface(self.quit_rect.size)
        self.quit_surf.fill((0, 0, 0))
        pygame.draw.rect(self.quit_surf, self.dev_color, self.quit_rect, 1)
        quit_text = self.dev_font.render("quit", False, self.dev_color)
        quit_text_rect = quit_text.get_rect()
        quit_text_rect.center = self.quit_rect.center
        self.quit_surf.blit(quit_text, quit_text_rect)
        self.quit_rect.center = constants.SMALL_DISPLAY_WIDTH // 2, 200

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event_manager.adjust_mouse(*event.pos)
            if self.start_rect.collidepoint(x, y):
                self.persistent_state_data["world_name"] = "test"
                self.close("MainGame")
            elif self.quit_rect.collidepoint(x, y):
                self.close()

    def update(self, dt):
        pass

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))
        target_surface.blit(self.start_surf, self.start_rect)
        target_surface.blit(self.quit_surf, self.quit_rect)


