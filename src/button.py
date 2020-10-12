import pygame

from src import constants


class Button:
    def __init__(self, text, size, position, action):
        self.action = action
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = position
        self.idle_image = pygame.Surface(size, pygame.SRCALPHA)
        self.hover_image = self.idle_image.copy()
        self.image_rect = self.idle_image.get_rect()
        self.radius = 7
        pygame.draw.rect(
            self.idle_image,
            constants.BUTTON_BACKGROUND_COLOR,
            self.image_rect,
            border_radius=self.radius
        )
        pygame.draw.rect(
            self.idle_image,
            constants.BUTTON_OUTLINE_COLOR,
            self.image_rect,
            1,
            border_radius=self.radius
        )
        pygame.draw.rect(
            self.hover_image,
            constants.BUTTON_BACKGROUND_COLOR_HOVER,
            self.image_rect,
            border_radius=self.radius
        )
        pygame.draw.rect(
            self.hover_image,
            constants.BUTTON_OUTLINE_COLOR,
            self.image_rect,
            1,
            border_radius=self.radius
        )
        self.image = self.idle_image
        self.mask = pygame.mask.from_surface(self.image)
        self.font = pygame.freetype.Font(
            constants.BUTTON_FONT_PATH,
            constants.BUTTON_FONT_SIZE
        )
        self.font.pad = True
        self.font.fgcolor = constants.BUTTON_FONT_COLOR
        self.text_rect = pygame.Rect(0, 0, 0, 0)
        self.update_text(text)

    def update_text(self, text):
        # First erase the previous text:
        pygame.draw.rect(
            self.idle_image,
            constants.BUTTON_BACKGROUND_COLOR,
            self.text_rect
        )
        pygame.draw.rect(
            self.hover_image,
            constants.BUTTON_BACKGROUND_COLOR_HOVER,
            self.text_rect
        )

        text_surf, self.text_rect = self.font.render(text)
        self.text_rect.center = self.image_rect.center
        self.idle_image.blit(text_surf, self.text_rect)
        self.hover_image.blit(text_surf, self.text_rect)

    def collidepoint(self, x, y):
        if self.rect.collidepoint(x, y):
            # Only collide if the point is inside the rounded corners:
            if self.mask.get_at((x - self.rect.x, y - self.rect.y)):
                self.image = self.hover_image
                return True
        self.image = self.idle_image
        return False
