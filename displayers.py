import pygame

class TextDisplayer(object):
    def __init__(self, pixel_surface):
        self.font = pygame.font.SysFont("Arial", 12)
        self.pixel_surface = pixel_surface

    def clear_display(self):
        self.pixel_surface.fill(pygame.Color(0, 0, 0))

    def display_text(self, text, color="#ffffff"):
        message = self.font.render(text, True, pygame.Color(str(color)))
        self.pixel_surface.blit(message, message.get_rect())

    def display_loading(self, point_amount):
        self.clear_display()
        text = "Loading "+point_amount*"."
        self.display_text(text)

    def display_menu_entry(self, text, color="#ffffff", left_entry_color="#ffffff", right_entry_color="#ffffff"):
        self.clear_display()
        #pygame.draw.polygon(self.pixel_surface, pygame.Color(left_entry_color), [[15, 5], [15, 15], [5, 10]], 1)
        self.display_text(text, color)
        # TODO display right arrow
