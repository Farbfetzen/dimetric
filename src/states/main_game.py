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
from src.enemy import Enemy
from src.resources import maps, display
from src.coordinate_conversion import map_to_screen


class MainGame(State):
    def __init__(self, map_name):
        super().__init__()
        self.map = maps[map_name]
        self.camera_offset_x = const.SMALL_WINDOW_WIDTH // 2 - const.TILE_WIDTH_HALF
        self.camera_offset_y = const.SMALL_WINDOW_HEIGHT // 2 - const.TILE_HEIGHT_HALF * self.map.height
        self.enemies = []

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_s:
                    self.next_wave()

    def update(self, dt):
        for e in self.enemies:
            e.update(dt)

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))

        # FIXME: The map to screen conversion is still wrong. [0, 0] should be at the top.
        for tile in self.map.tiles:
            target_surface.blit(
                tile.image,
                (tile.x + self.camera_offset_x, tile.y + self.camera_offset_y)
            )

        for e in self.enemies:
            target_surface.blit(
                e.image,
                map_to_screen(
                    e.rect.x, e.rect.y,
                    0, e.offset_y,
                    self.camera_offset_x, self.camera_offset_y
                )
            )

        pygame.draw.circle(
            target_surface,
            (255, 0, 0),
            map_to_screen(0, 0, 0, 0, self.camera_offset_x, self.camera_offset_y),
            2
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

    def next_wave(self):
        self.enemies.append(Enemy("cube", self.map.path))
