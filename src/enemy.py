"""Enemies."""

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

from src.resources import images


class Enemy:
    def __init__(self, enemy_type, path):
        self.type = enemy_type
        self.path = path
        self.image = images[self.type]

        # FIXME: Achtung, ich muss hier unterscheiden zwischen width und height
        #     in world space und screen space! Das Rect ist für Kollisionen im
        #     world space gedacht. Das heißt ich muss sehr genau aufpassen, wie
        #     ich die Sachen benennen und zwischen world und screen umrechne.

        width, height = self.image.get_size()
        height_dimetric = width // 2
        self.offset_y = height_dimetric - height
        # Rect in world space, used for collision detection, not for blitting.
        self.rect = pygame.Rect(-1, -1, width, height_dimetric)
        print(self.rect)
        self.rect.center = path[0]

        self.hitpoints = 100
        self.speed = 1
        self.direction = [1, 0]  # [x, y]

        print(path[0])
        print(self.rect.center)
        print(self.rect)

    def update(self, dt):
        pass
