"""Run this file to run the game."""

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


# Must be set before importing Pygame:
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_CENTERED"] = "1"


# Must be done before loading resources like sprites and sounds:
import pygame
import src.constants as const
pygame.init()
display = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))


import src.main
src.main.run(display)
