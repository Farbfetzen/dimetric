import pygame

from src.helpers import main_to_small_display_int
from src import constants


class Scene:
    def __init__(self, game, dev_overlay=None):
        self.game = game
        self.target_surface = game.small_display
        if dev_overlay is None:
            self.dev_overlay = DevOverlay(self)
        else:
            self.dev_overlay = dev_overlay(self)
        self.mouse_pos = pygame.Vector2()
        self.buttons = ()

    def start(self):
        # Make sure button image == hover image when starting the scene without
        # moving the mouse. This is necessary because in most scenes the mouse
        # position is only updated during the event loop:
        mouse_x, mouse_y = main_to_small_display_int(*pygame.mouse.get_pos())
        for b in self. buttons:
            if b.collidepoint(mouse_x, mouse_y):
                break

    def close(self, new_scene_name="", remove_self=True, remove_all=False):
        """Quit or suspend a scene. Use this for cleanup."""
        if new_scene_name == "quit":
            self.game.quit()
            return
        if remove_all:
            remove = self.game.active_scenes.copy()
        elif remove_self:
            remove = [self]
        else:
            remove = []
        self.game.change_scenes(remove, new_scene_name)

    def process_event(self, event, event_manager):
        # Return True to prevent the scenes below from receiving this event.
        if event.type == pygame.QUIT:
            self.close("quit")
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_dev:
                self.game.dev_overlay_visible = not self.game.dev_overlay_visible
                return True
        elif ((event.type == pygame.MOUSEMOTION
               or event.type == pygame.MOUSEBUTTONDOWN)
              and self.buttons):
            mouse_x, mouse_y = main_to_small_display_int(*event.pos)
            for b in self.buttons:
                if (b.collidepoint(mouse_x, mouse_y)
                        and event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    b.action()
                    return True

    def update(self, dt):
        # Return True to block updates in scenes below this one.
        self.mouse_pos.update(
            main_to_small_display_int(*pygame.mouse.get_pos())
        )

    def draw(self):
        raise NotImplementedError


class DevOverlay:
    def __init__(self, scene):
        self.scene = scene
        self.target_surface = scene.game.main_display
        self.dev_font = pygame.freetype.Font(
            constants.DEV_FONT_PATH,
            constants.DEV_FONT_SIZE
        )
        self.dev_font.pad = True
        self.dev_font.fgcolor = constants.DEV_COLOR
        self.dev_margin = pygame.Vector2(10, 10)

        self.fps_text = ""
        self.fps_surf = None
        self.fps_rect = None

    def update(self, clock):
        new_fps_text = f"FPS: {int(clock.get_fps())}"
        if new_fps_text != self.fps_text:
            self.fps_text = new_fps_text
            self.fps_surf, self.fps_rect = self.dev_font.render(self.fps_text)
            self.fps_rect.topleft = self.dev_margin

    def draw(self):
        self.target_surface.blit(self.fps_surf, self.fps_rect)
