"""Game constants."""

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


MAIN_DISPLAY_WIDTH = 800
MAIN_DISPLAY_HEIGHT = 600
MAIN_DISPLAY_SIZE = (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
ZOOM_FACTOR = 0.5
SMALL_DISPLAY_WIDTH = MAIN_DISPLAY_WIDTH * ZOOM_FACTOR
SMALL_DISPLAY_HEIGHT = MAIN_DISPLAY_HEIGHT * ZOOM_FACTOR
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)

FPS = 60

COLORKEY = (255, 255, 255)
OUTLINE_COLOR = (60, 60, 60)
HIGHLIGHT_COLOR = (255, 128, 0)

TILE_WIDTH = 32
TILE_HEIGHT = 16
TILE_WIDTH_HALF = TILE_WIDTH // 2
TILE_HEIGHT_HALF = TILE_HEIGHT // 2
PLATFORM_HEIGHT = 8

WORLD_SCROLL_SPEED = (TILE_WIDTH * 10, TILE_HEIGHT * 10)
