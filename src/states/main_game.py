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
from src.enemy import Enemy
from src.resources import worlds, display
import src.camera


class MainGame(State):
    def __init__(self, world_name):
        super().__init__()
        self.world = worlds[world_name]
        self.camera = src.camera.Camera(self.world.width, self.world.height)
        self.enemies = []

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_s:
                    self.next_wave()
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # left klick held while moving
                    self.camera.scroll(*event.rel)
                    for tile in self.world.tiles:
                        tile.update_screen_xy(self.camera.offset_x, self.camera.offset_y)

    def update(self, dt):
        for e in self.enemies:
            e.update(dt)

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))

        for tile in self.world.tiles:
            tile.draw(target_surface)

        # for e in self.enemies:
        #     target_surface.blit(
        #         e.image,
        #         world_to_screen(
        #             e.rect.x, e.rect.y,
        #             0, e.offset_y,
        #             self.camera_offset_x, self.camera_offset_y
        #         )
        #     )

        # DEBUG:
        # pos = ((0, 0), (self.world.width, self.world.height),
        #        (0, self.world.height), (self.world.width, 0))
        # col = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255))
        # for p, c in zip(pos, col):
        #     pygame.draw.circle(
        #         target_surface,
        #         c,
        #         self.camera.world_to_screen(p[0], p[1]),
        #         2
        #     )
        # ---

        # # Highlight the outline of a tile when the mouse is over the world.
        # # TODO: highlight the top of the platform
        # # TODO: snap to grid when mouse is over the raised part of a platform, not
        # #   only over the base.
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_world_pos = screen_to_world(*mouse_pos)
        # if any(0 > pos or pos > len(world_data) - 1 for pos in mouse_world_pos):
        #     tile = tiles[2]
        #     rect = tile.get_rect(center=mouse_pos)
        #     display.blit(tiles[2], rect)
        # else:
        #     display.blit(
        #         tiles[2],
        #         world_to_screen(
        #             mouse_world_pos[0],
        #             mouse_world_pos[1],
        #             *tile_offsets[2]
        #         )
        #     )

    def next_wave(self):
        self.enemies.append(Enemy("cube", self.world.path))
