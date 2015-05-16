import pygame

class TextDisplayer(object):
    def __init__(self, pixel_surface):
        self.font = pygame.font.SysFont("Arial", 12)
        self.pixel_surface = pixel_surface

    def display_text(self, text, color="#ffffff"):
        message = self.font.render(text, True, pygame.Color(color))
        self.pixel_surface.fill(pygame.Color(0, 0, 0))
        self.pixel_surface.blit(message, message.get_rect())

    def display_loading(self, point_amount):
        text = "Loading "+point_amount*"."
        self.display_text(text)

