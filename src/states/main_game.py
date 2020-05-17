"""Main game state"""

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

from src.states.state import State
import src.constants as const


class MainGame(State):
    def __init__(self, data, map_name):
        super().__init__(data)
        self.map = data["maps"][map_name]

        self.camera_offset_x = const.WINDOW_WIDTH // 2 - const.TILE_WIDTH_HALF
        self.camera_offset_y = const.WINDOW_HEIGHT // 2 - const.TILE_HEIGHT_HALF * self.map.height

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True

    def draw(self, dest_surface):
        dest_surface.fill((0, 0, 0))

        for tile in self.map.tiles:
            dest_surface.blit(
                tile.surface,
                (tile.x + self.camera_offset_x, tile.y + self.camera_offset_y)
            )

        # # Highlight the outline of a tile when the mouse is over the map.
        # # TODO: highlight the top of the platform
        # # TODO: snap to grid when mouse is over the raised part of a platform, not
        # #   only over the base.
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_map_pos = screen_to_map(*mouse_pos)
        # if any(0 > pos or pos > len(map_data) - 1 for pos in mouse_map_pos):
        #     tile = tiles[2]
        #     rect = tile.get_rect(center=mouse_pos)
        #     display.blit(tiles[2], rect)
        # else:
        #     display.blit(
        #         tiles[2],
        #         map_to_screen(
        #             mouse_map_pos[0],
        #             mouse_map_pos[1],
        #             *tile_offsets[2]
        #         )
        #     )
