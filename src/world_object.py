"""Base class for objects which have a position in world coordinates."""

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


from dataclasses import dataclass

import pygame


@dataclass
class WorldObject:
    type: str
    image: pygame.Surface
    world_pos: pygame.Vector2
    surface_pos: pygame.Vector2
    layer: int = 0

    def __lt__(self, other):
        return ((self.world_pos.x, self.world_pos.y, self.layer) <
                (other.world_pos.x, other.world_pos.y, other.layer))
