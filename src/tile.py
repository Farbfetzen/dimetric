"""Tile class."""

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


import math

import src.constants as const


class Tile:
    def __init__(self, image,
                 world_x, world_y,
                 camera_offset_x=0,  camera_offset_y=0):
        self.image = image
        self.rect = self.image.get_rect()
        self.world_x = 0
        self.world_y = 0
        # The difference from the camera_offset in small_display coordinates:
        self.screen_offset_x = 0
        self.screen_offset_y = 0
        # Account for images taller than TILE_HEIGHT, like platforms and such.
        # The -1 is because the base rhombus is const.TILE_HEIGHT + 1 tall.
        self.tile_offset_y = self.rect.height - const.TILE_HEIGHT - 1

        self.update_position(world_x, world_y, camera_offset_x, camera_offset_y)

    def update_screen_position(self, camera_offset_x, camera_offset_y):
        self.rect.midtop = (
            self.screen_offset_x + camera_offset_x,
            self.screen_offset_y + camera_offset_y
        )

    def update_position(self, world_x, world_y, camera_offset_x, camera_offset_y):
        # Update screen and world positions.
        self.world_x = math.floor(world_x)
        self.world_y = math.floor(world_y)
        self.screen_offset_x = (self.world_x - self.world_y) * const.TILE_WIDTH_HALF
        self.screen_offset_y = ((self.world_x + self.world_y) * const.TILE_HEIGHT_HALF
                                - self.tile_offset_y)
        self.update_screen_position(camera_offset_x, camera_offset_y)

    def draw(self, target_surface):
        target_surface.blit(self.image, self.rect)
