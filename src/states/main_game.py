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

import src.camera
import src.resources as res
from src.states.state import State
from src.enemy import Enemy


class MainGame(State):
    def __init__(self, world_name):
        super().__init__()
        self.world = res.worlds[world_name]
        self.camera = src.camera.Camera(self.world.width, self.world.height)
        self.enemies = []
        self.debug_overlay = False
        self.mouse_pos_world_x = 0
        self.mouse_pos_world_y = 0

        # Debug overlay:
        self.debug_font = pygame.font.SysFont("monospace", 18)
        self.debug_color = (255, 255, 255)
        self.debug_line_height = self.debug_font.get_height()
        self.debug_margin = (10, 10)

    def process_events(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_s:
                    self.next_wave()
                elif event.key == pygame.K_F1:
                    self.debug_overlay = not self.debug_overlay
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # left klick held while moving
                    self.camera.scroll(*event.rel)
                    for tile in self.world.tiles:
                        tile.update_screen_xy(self.camera.offset_x, self.camera.offset_y)

    def update(self, dt):
        for e in self.enemies:
            e.update(dt)

    def draw(self):
        res.small_display.fill((0, 0, 0))

        for tile in self.world.tiles:
            tile.draw(res.small_display)

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

    def draw_debug_overlay(self):
        fps_text = self.debug_font.render(
            f"FPS: {int(res.clock.get_fps())}",
            False,
            self.debug_color
        )
        res.main_display.blit(fps_text, self.debug_margin)

    def next_wave(self):
        self.enemies.append(Enemy("cube", self.world.path))
