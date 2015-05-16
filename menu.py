import sys
import pygame
import led

from threading import Thread

from gameloader import GameLoader
from constants import *
from displayers import TextDisplayer



class Menu(object):
    def __init__(self, display_device=None):
        self.speed = 30
        self.display_device = display_device
        self.pixel_surface = None
        self.clock = pygame.time.Clock()
        self.displays = []
        self.games = None
        self.menu_index = 0

    def init_displays(self):
        pygame.init()
        pygame.display.set_mode()
        display_size = (90,20)
        if self.display_device is not None:
            self.displays.append(led.teensy.TeensyDisplay(self.display_device))
        self.displays.append(led.sim.SimDisplay(display_size))
        self.displays.append(led.dsclient.DisplayServerClientDisplay('localhost', 8123))
        self.pixel_surface = pygame.Surface(display_size)

    def load_games(self):
        gameloader = GameLoader()
        t = Thread(target=gameloader.load_games)
        t.start()

        display_text = TextDisplayer(self.pixel_surface)
        while not gameloader.games_loaded:
            display_text.display_text("Loading ...")
            self.update_displays()
        self.games = gameloader.games


    def display_menu(self):
        first = True
        while True:
            if first or self.check_keyboard_event():
                game = self.games[self.menu_index]
                TextDisplayer(self.pixel_surface).display_text(game.name)
                self.update_displays()
                first = False

    def update_displays(self):
        for display in self.displays:
            display.update(self.pixel_surface)
        self.clock.tick(30)

    def check_keyboard_event(self):
        event_received = False
        for event in pygame.event.get():
            event_received = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == KEY_LEFT:
                    self.menu_index -= 1
                    if self.menu_index < 0:
                        self.menu_index = len(self.games)-1
                elif event.key == KEY_RIGHT:
                    self.menu_index += 1
                    if self.menu_index > len(self.games)-1:
                        self.menu_index = 0
        return event_received


def main():
    if sys.argv.__len__() > 1:
        menu = Menu(sys.argv[1])
    else:
        menu = Menu()
    menu.init_displays()
    menu.load_games()
    menu.display_menu()

if __name__ == "__main__":
    main()
