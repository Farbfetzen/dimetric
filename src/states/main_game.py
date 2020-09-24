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

from src import constants
from src import resources
from src import states
from src import enemy


class MainGame(states.State):
    def __init__(self, world_name):
        super().__init__()
        self.world = resources.worlds[world_name]
        # self.enemies = []
        self.mouse_pos_world = pygame.Vector2()
        self.mouse_rel = pygame.Vector2()
        self.mouse_dy = tuple(enumerate((constants.PLATFORM_HEIGHT, 0)))
        self.tile_at_mouse = None

    def process_event(self, event, event_manager):
        super().process_event(event, event_manager)
        if event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_escape:
                self.close("MainMenu")
            # elif event.key == self.event_manager.k_next_wave:
            #     self.next_wave()
            elif event.key == event_manager.k_scroll_left:
                self.world.scroll_direction.x -= 1
            elif event.key == event_manager.k_scroll_right:
                self.world.scroll_direction.x += 1
            elif event.key == event_manager.k_scroll_up:
                self.world.scroll_direction.y -= 1
            elif event.key == event_manager.k_scroll_down:
                self.world.scroll_direction.y += 1
        elif event.type == pygame.KEYUP:
            if event.key == event_manager.k_scroll_left:
                self.world.scroll_direction.x += 1
            elif event.key == event_manager.k_scroll_right:
                self.world.scroll_direction.x -= 1
            elif event.key == event_manager.k_scroll_up:
                self.world.scroll_direction.y += 1
            elif event.key == event_manager.k_scroll_down:
                self.world.scroll_direction.y -= 1
        elif (event.type == pygame.MOUSEMOTION
              and event.buttons[event_manager.mouse_map_scroll_button_index]):
            self.mouse_rel.update(event_manager.adjust_mouse(*event.rel))
            self.world.scroll(self.mouse_rel)

    def update(self, dt):
        self.mouse_pos_world.update(
            self.world.small_display_to_world_pos(*self.mouse_pos)
        )
        self.world.update(dt)
        self.get_tile_at_mouse()
        self.highlight_tile_at_mouse()
        # for e in self.enemies:
        #     e.update(dt)

    def get_tile_at_mouse(self):
        # I want to detect a platform only when the mouse is over the raised
        # part. The sides and base don't matter. I hope this will simplify
        # snapping the towers to the platforms.
        tiles = [None, None]
        for i, dy in self.mouse_dy:
            tile_pos_x, tile_pos_y = self.world.small_display_to_tile_pos(
                self.mouse_pos.x,
                self.mouse_pos.y + dy
            )
            tiles[i] = self.world.get_tile_at(tile_pos_x, tile_pos_y)
        if tiles[0] is not None and tiles[0].type == "platform":
            self.tile_at_mouse = tiles[0]
        elif tiles[1] is not None and tiles[1].type == "path":
            self.tile_at_mouse = tiles[1]
        else:
            self.tile_at_mouse = None

    def highlight_tile_at_mouse(self):
        if self.tile_at_mouse is None:
            self.world.highlight.layer = -1
            return
        self.world.highlight.layer = 1
        self.world.highlight.world_pos.update(self.tile_at_mouse.world_pos)
        self.world.highlight.surface_pos.update(self.tile_at_mouse.surface_pos)

    def draw(self, target_surface):
        target_surface.fill((0, 0, 0))
        self.world.draw(target_surface)

        # for e in self.enemies:
        #     target_surface.blit(
        #         e.image,
        #         world_to_screen(
        #             e.rect.x, e.rect.y,
        #             0, e.offset_y,
        #             self.camera_offset_x, self.camera_offset_y
        #         )
        #     )

    def draw_dev_overlay(self, target_surface, clock):
        super().draw_dev_overlay(target_surface, clock)

        # FIXME: Rendering is rather slow. Reuse the surfaces, use render()
        #  instead of render_to(), and only render a new text if the info
        #  has changed.
        if self.tile_at_mouse is None:
            tile_info = "tile at mouse: none"
        else:
            tile_info = (
                f"tile at mouse: {self.tile_at_mouse.type}" +
                f" ({self.tile_at_mouse.world_pos.x:.0f}, " +
                f"{self.tile_at_mouse.world_pos.y:.0f})"
            )
        self.dev_font.render_to(
            target_surface,
            (self.dev_margin.x, self.dev_margin.y * 3),
            tile_info
        )

        x, y = self.mouse_pos_world
        self.dev_font.render_to(
            target_surface,
            (self.dev_margin.x, self.dev_margin.y * 5),
            f"mouse position in world: ({x:.1f}, {y:.1f})"
        )

        pygame.draw.rect(
            target_surface,
            self.dev_color,
            pygame.Rect([r * constants.MAGNIFICATION for r in self.world.rect]),
            1
        )

    # def next_wave(self):
    #     self.enemies.append(Enemy("cube", self.world.path))
