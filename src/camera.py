"""Camer object controlling coordinate conversions."""

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


# TODO: method for map to screen conversion
# TODO: method for screen to map conversion
# TODO: variable camera offset when dragging the mouse or using arrow keys

# The camera object will be an attribute of the main_game object.
# Start the map centered on the screen.

# Map coordinates should be similar in dimension to screen coordinates. This
# will make movement and collision detection easier because the collision rects
# will live in map coordinates. Maybe make one tile edge 10 or 100 long? it
# should not matter much because of the conversion.

from src.resources import small_display


class Camera:
    pass
