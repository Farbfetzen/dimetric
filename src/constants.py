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


import os

import pygame


MAIN_DISPLAY_WIDTH = 1200
MAIN_DISPLAY_HEIGHT = 750
MAIN_DISPLAY_SIZE = (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
MAGNIFICATION = 3
# Sizes should be integer multiples of magnification for better results.
assert MAIN_DISPLAY_WIDTH % MAGNIFICATION == 0
assert MAIN_DISPLAY_HEIGHT % MAGNIFICATION == 0
SMALL_DISPLAY_WIDTH = MAIN_DISPLAY_WIDTH // MAGNIFICATION
SMALL_DISPLAY_HEIGHT = MAIN_DISPLAY_HEIGHT // MAGNIFICATION
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)

FPS = 60

OUTLINE_COLOR = (60, 60, 60)
HIGHLIGHT_COLOR = (255, 128, 0)
DEV_COLOR = (255, 255, 255)

TILE_WIDTH = 32
TILE_HEIGHT = 16
TILE_WIDTH_HALF = TILE_WIDTH // 2
TILE_HEIGHT_HALF = TILE_HEIGHT // 2
PLATFORM_HEIGHT = 8

WORLD_SCROLL_SPEED = (TILE_WIDTH * 7, TILE_HEIGHT * 7)

BUTTON_FONT_COLOR = (255, 255, 255)
BUTTON_OUTLINE_COLOR = BUTTON_FONT_COLOR
BUTTON_BACKGROUND_COLOR = (0, 0, 0)
BUTTON_BACKGROUND_COLOR_HOVER = (64, 64, 64)

DEFAULT_OPTIONS = {
    "controls": {
        "scroll left": pygame.key.name(pygame.K_LEFT),
        "scroll right": pygame.key.name(pygame.K_RIGHT),
        "scroll up": pygame.key.name(pygame.K_UP),
        "scroll down": pygame.key.name(pygame.K_DOWN),
        "mouse scroll button index": 2,
        "dev": pygame.key.name(pygame.K_F1)
    }
}

DEV_FONT_PATH = os.path.join("fonts", "Inconsolata-VariableFont.ttf")
DEV_FONT_SIZE = 18
BUTTON_FONT_PATH = os.path.join("fonts", "OpenSans-Bold.ttf")
BUTTON_FONT_SIZE = 15
