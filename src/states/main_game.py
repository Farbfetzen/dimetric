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
        self.mouse_rel = pygame.Vector2()
        self.tile_at_mouse = None

        # Developer overlay:
        self.dev_overlay = False
        self.dev_font = pygame.font.SysFont("monospace", 15)
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
                    self.world.scroll_direction.x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.world.scroll_direction.x += 1
                elif event.key == pygame.K_UP:
                    self.world.scroll_direction.y -= 1
                elif event.key == pygame.K_DOWN:
                    self.world.scroll_direction.y += 1
                elif event.key == pygame.K_F1:
                    self.dev_overlay = not self.dev_overlay
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.world.scroll_direction.x += 1
                elif event.key == pygame.K_RIGHT:
                    self.world.scroll_direction.x -= 1
                elif event.key == pygame.K_UP:
                    self.world.scroll_direction.y += 1
                elif event.key == pygame.K_DOWN:
                    self.world.scroll_direction.y -= 1
            elif event.type == pygame.MOUSEMOTION and event.buttons[2]:
                # buttons[2] is the right mouse button
                self.mouse_rel.update(event.rel)
                self.mouse_rel *= const.ZOOM_FACTOR
                self.world.scroll(self.mouse_rel)

        # Convert mouse position to small_display coordinates:
        pos = pygame.mouse.get_pos()
        self.mouse_pos.x = pos[0] * const.ZOOM_FACTOR
        self.mouse_pos.y = pos[1] * const.ZOOM_FACTOR
        self.mouse_pos_world.update(self.world.small_display_to_world_pos(*self.mouse_pos))

    def update(self, dt):
        self.world.update(dt)
        self.get_tile_at_mouse()
        # for e in self.enemies:
        #     e.update(dt)

    def get_tile_at_mouse(self):
        """Check which tile is at the mouse position. Also checks if
        the mouse is over the raised part of a platform but not its base.
        """
        for dy in range(const.PLATFORM_HEIGHT, -1, -1):
            tile_x, tile_y = self.world.small_display_to_world_pos(
                self.mouse_pos.x,
                self.mouse_pos.y + dy,
                tile=True
            )
            self.tile_at_mouse = self.world.get_tile_at(tile_x, tile_y)
            if (self.tile_at_mouse is not None
                    and self.tile_at_mouse.type == "platform"):
                break  # Ignore tiles behind the platform

    def draw(self):
        res.small_display.fill((0, 0, 0))

        self.world.draw(res.small_display)

        # Draw to small_display before that is scaled up. This is why this
        # line is outside draw_dev_overlay().
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

    def draw_dev_overlay(self):
        fps_text = self.dev_font.render(
            f"FPS: {int(res.clock.get_fps())}",
            False,
            self.dev_color
        )
        res.main_display.blit(fps_text, self.dev_margin)

        if self.tile_at_mouse is None:
            tile_info = "tile at mouse: none"
        else:
            tile_info = (
                f"tile at mouse: {self.tile_at_mouse.type}" +
                f" ({self.tile_at_mouse.world_x}, " +
                f"{self.tile_at_mouse.world_y})"
            )
        mouse_tile_text = self.dev_font.render(
            tile_info,
            False,
            self.dev_color
        )
        res.main_display.blit(
            mouse_tile_text,
            (self.dev_margin.x, self.dev_margin.y * 3)
        )

    # def next_wave(self):
    #     self.enemies.append(Enemy("cube", self.world.path))
