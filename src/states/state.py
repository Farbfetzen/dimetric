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


class State:
    def __init__(self, dev_overlay=None):
        if dev_overlay is None:
            self.dev_overlay = StateDevOverlay(self)
        else:
            self.dev_overlay = dev_overlay(self)
        self.mouse_pos = pygame.Vector2()
        self.is_done = False
        self.persistent_state_data = {}

    def resume(self, persistent_state_data):
        """Resume an already instantiated state.
        Use the information provided by the previous state to modify
        this state.
        """
        self.persistent_state_data = persistent_state_data
        self.dev_overlay.is_visible = persistent_state_data["dev_overlay_visible"]
        self.is_done = False

    def close(self, next_state_name=None):
        """Quit or suspend a state.
        Use this for cleanup. Save relevant data in persistent_state_data to
        pass it to the next state. Set next_state_name to "quit" to
        immediately quit the app.
        """
        if next_state_name is None:
            next_state_name = "quit"
        self.persistent_state_data["next_state_name"] = next_state_name
        self.persistent_state_data["dev_overlay_visible"] = self.dev_overlay.is_visible
        self.is_done = True

    def process_event(self, event, event_manager):
        if event.type == pygame.QUIT:
            self.close()
        elif event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_dev:
                self.dev_overlay.is_visible = not self.dev_overlay.is_visible

    def update(self, dt):
        pass

    def draw(self, target_surface):
        raise NotImplementedError


class StateDevOverlay:
    def __init__(self, state):
        self.state = state
        self.is_visible = True
        self.dev_font = pygame.freetype.SysFont(
            "inconsolata, consolas, monospace",
            19
        )
        self.dev_line_hight = self.dev_font.get_sized_height()
        self.dev_color = (255, 255, 255)
        self.dev_font.fgcolor = self.dev_color
        self.dev_margin = pygame.Vector2(10, 10)

        self.fps_text = ""
        self.fps_surf = None
        self.fps_rect = None

    def update(self, clock):
        new_fps_text = f"FPS: {int(clock.get_fps())}"
        if new_fps_text != self.fps_text:
            self.fps_text = new_fps_text
            self.fps_text, self.fps_rect = self.dev_font.render(self.fps_text)
            self.fps_rect.topleft = self.dev_margin

    def draw(self, target_surface):
        target_surface.blit(self.fps_text, self.fps_rect)
