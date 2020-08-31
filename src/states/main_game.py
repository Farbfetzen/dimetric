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
import src.tile_world
import src.resources as res
from src.states.state import State
from src.enemy import Enemy


class MainGame(State):
    def __init__(self, world_name):
        super().__init__()
        self.world = res.worlds[world_name]
        self.camera = src.camera.Camera(self.world.sidelength)
        self.world.scroll(self.camera.offset)
        self.enemies = []
        self.mouse_pos_world = pygame.Vector2()

        # Developer overlay:
        self.dev_overlay = True
        self.dev_font = pygame.font.SysFont("monospace", 18)
        self.dev_color = (255, 255, 255)
        self.dev_line_height = self.dev_font.get_height()
        self.dev_margin = pygame.Vector2(10, 10)

    def process_events(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_s:
                    self.next_wave()
                elif event.key == pygame.K_F1:
                    self.dev_overlay = not self.dev_overlay
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                self.camera.scroll(*event.rel)
                self.world.scroll(self.camera.offset)

        self.mouse_pos_world.update(
            self.camera.main_display_to_world(*pygame.mouse.get_pos())
        )

    def update(self, dt):
        for e in self.enemies:
            e.update(dt)

        if self.dev_overlay:
            self.world.highlight(*self.mouse_pos_world)
        else:
            self.world.disable_highlight()

    def draw(self):
        res.small_display.fill((0, 0, 0))

        self.world.draw(res.small_display)

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
        # pos = ((0, 0), (self.world.sidelength, self.world.sidelength),
        #        (0, self.world.sidelength), (self.world.sidelength, 0))
        # col = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255))
        # for p, c in zip(pos, col):
        #     pygame.draw.circle(
        #         res.small_display,
        #         c,
        #         self.camera.world_to_screen(pygame.Vector2(p)),
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

    def draw_dev_overlay(self):
        fps_text = self.dev_font.render(
            f"FPS: {int(res.clock.get_fps())}",
            False,
            self.dev_color
        )
        res.main_display.blit(fps_text, self.dev_margin)

        world_pos_text = self.dev_font.render(
            f"mouse world pos: {int(self.mouse_pos_world.x)}, {int(self.mouse_pos_world.y)}",
            False,
            self.dev_color
        )
        res.main_display.blit(
            world_pos_text,
            (self.dev_margin.x, self.dev_margin.y * 3)
        )

    def next_wave(self):
        self.enemies.append(Enemy("cube", self.world.path))
