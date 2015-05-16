import sys
import pygame
import led
import time

# from pygame.locals import *
from threading import Thread
from git import Repo


class Menu(object):
    def __init__(self, display_device=None):
        self.speed = 30
        self.display_device = display_device
        self.pixel_surface = None
        self.clock = pygame.time.Clock()
        self.displays = []

    def init_displays(self):
        pygame.init()
        pygame.display.set_mode()
        display_size = (90,20)
        if self.display_device is not None:
            self.displays.append(led.teensy.TeensyDisplay(self.display_device))
        self.displays.append(led.sim.SimDisplay(display_size))
        self.pixel_surface = pygame.Surface(display_size)

    def load_games(self):
        gameloader = GameLoader()
        t = Thread(target=gameloader.load_games)
        t.start()

        display_text = DisplayText(self.pixel_surface)
        while t.is_alive:
            display_text.display_text("Loading ...")
            self.update_displays()

    def update_displays(self):
        for display in self.displays:
            display.update(self.pixel_surface)
        self.clock.tick(30)


class DisplayText(object):
    def __init__(self, pixel_surface):
        self.font = pygame.font.SysFont("Arial", 12)
        self.pixel_surface = pixel_surface

    def display_text(self, text, color="#ffffff"):
        message = self.font.render(text, True, pygame.Color(color))
        self.pixel_surface.fill(pygame.Color(0, 0, 0))
        self.pixel_surface.blit(message, message.get_rect())


class GameLoader(object):
    def __init__(self):
        #self.menu_repo = Repo()

    def load_games(self):
        time.sleep(10)
        # TODO git pull game list
        # TODO for each entry
            # clone --depth=1
            # OR pull if game already exists
            # OR throw away old games

    def refresh_game_list(self):


def main():
    if sys.argv.__len__() > 1:
        menu = Menu(sys.argv[1])
    else:
        menu = Menu()
    menu.init_displays()
    menu.load_games()
    #menu.displayMenu()
    #menu.start_event_loop()

if __name__ == "__main__":
    main()
