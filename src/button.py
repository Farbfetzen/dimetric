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


class Button:
    def __init__(self, text, size, position, action, align="centered"):
        # FIXME: Lots of magic numbers and constants in this init.
        self.action = action
        self.rect = pygame.Rect((0, 0), size)
        self.idle_image = pygame.Surface(size)
        self.idle_image.fill((0, 0, 0))
        self.hover_image = self.idle_image.copy()
        self.hover_image.fill((64, 64, 64))
        pygame.draw.rect(self.idle_image, (255, 255, 255), self.rect, 1)
        pygame.draw.rect(self.hover_image, (255, 255, 255), self.rect, 1)
        self.image = self.idle_image

        font = pygame.freetype.SysFont("sans", 15, bold=True)
        text_surf, text_rect = font.render(text, (255, 255, 255))
        text_rect.center = self.rect.center
        self.idle_image.blit(text_surf, text_rect)
        self.hover_image.blit(text_surf, text_rect)

        if align == "centered":
            self.rect.center = position
        elif align == "topleft":
            self.rect.topleft = position
        else:
            raise ValueError("Align must be either 'centered' or 'topleft'.")

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos.x, mouse_pos.y):
            self.image = self.hover_image
        else:
            self.image = self.idle_image
