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


from math import floor

import pygame

import src.world
import src.constants as const
import src.resources as res
from src.states.state import State
from src.enemy import Enemy


class MainGame(State):
    def __init__(self, world_name):
        super().__init__()
        self.world = res.worlds[world_name]
        # self.enemies = []
        self.mouse_pos = pygame.Vector2()
        self.mouse_pos_world = pygame.Vector2()

        # Developer overlay:
        self.dev_overlay = False
        self.dev_font = pygame.font.SysFont("monospace", 18)
        self.dev_color = (255, 255, 255)
        self.dev_line_height = self.dev_font.get_height()
        self.dev_margin = pygame.Vector2(10, 10)

    def process_events(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                # elif event.key == pygame.K_s:
                #     self.next_wave()
                elif event.key == pygame.K_LEFT:
                    self.world.scrolling_x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.world.scrolling_x += 1
                elif event.key == pygame.K_UP:
                    self.world.scrolling_y -= 1
                elif event.key == pygame.K_DOWN:
                    self.world.scrolling_y += 1
                elif event.key == pygame.K_F1:
                    self.dev_overlay = not self.dev_overlay
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.world.scrolling_x += 1
                elif event.key == pygame.K_RIGHT:
                    self.world.scrolling_x -= 1
                elif event.key == pygame.K_UP:
                    self.world.scrolling_y += 1
                elif event.key == pygame.K_DOWN:
                    self.world.scrolling_y -= 1
            elif event.type == pygame.MOUSEMOTION and event.buttons[2]:
                # buttons[2] is the right mouse button
                self.world.scroll(event.rel, mouse=True)

        # Convert mouse position to small_display coordinates:
        pos = pygame.mouse.get_pos()
        self.mouse_pos.x = pos[0] * const.ZOOM_FACTOR
        self.mouse_pos.y = pos[1] * const.ZOOM_FACTOR
        self.mouse_pos_world.update(self.world.small_display_to_world_pos(*self.mouse_pos))

    def update(self, dt):
        self.world.update(dt)
        # for e in self.enemies:
        #     e.update(dt)

    def draw(self):
        res.small_display.fill((0, 0, 0))

        self.world.draw(res.small_display)

        if self.dev_overlay:
            pygame.draw.rect(res.small_display, self.dev_color, self.world.rect, 1)

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

    def draw_dev_overlay(self):
        fps_text = self.dev_font.render(
            f"FPS: {int(res.clock.get_fps())}",
            False,
            self.dev_color
        )
        res.main_display.blit(fps_text, self.dev_margin)

        mouse_pos_tile_x = floor(self.mouse_pos_world.x)
        mouse_pos_tile_y = floor(self.mouse_pos_world.y)
        world_pos_text = self.dev_font.render(
            f"mouse world pos: {mouse_pos_tile_x}, {mouse_pos_tile_y}",
            False,
            self.dev_color
        )
        res.main_display.blit(
            world_pos_text,
            (self.dev_margin.x, self.dev_margin.y * 3)
        )

        tile_at_mouse = self.world.get_tile_at(mouse_pos_tile_x, mouse_pos_tile_y)
        mouse_tile_text = self.dev_font.render(
            f"tile at mouse: {tile_at_mouse}",
            False,
            self.dev_color
        )
        res.main_display.blit(
            mouse_tile_text,
            (self.dev_margin.x, self.dev_margin.y * 5)
        )

    # def next_wave(self):
    #     self.enemies.append(Enemy("cube", self.world.path))
