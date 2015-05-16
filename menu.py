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
        self.game_index = 0
        self.menu_sections = []
        self.menu_section_dict = {}
        self.menu_section_index = 1

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
        amount_of_dots = 1
        time_counter = 0
        while not gameloader.games_loaded:
            cancel_loading = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        cancel_loading = True
            if cancel_loading:
                gameloader.stopp = True
            display_text.display_loading(amount_of_dots)
            time_counter += 1
            if time_counter >= 14:
                amount_of_dots += 1
                if amount_of_dots > 15:
                    amount_of_dots = 1
                time_counter = 0
            self.update_displays()
        self.games = gameloader.games

    def init_menus(self):
        system_entries = ['Quit', 'Version']
        system_section = MenuSection('system', system_entries)

        games_section = MenuSection('games', self.games)
        self.menu_sections.append(system_section)
        self.menu_sections.append(games_section)

        self.menu_section_dict['system'] = 0
        self.menu_section_dict['games'] = 1


    def display_menu(self):
        first = True
        while True:
            if first or self.check_keyboard_event():
                if self.menu_section_index == self.menu_section_dict['system']:
                    self.display_system_menu()
                elif self.menu_section_index == self.menu_section_dict['games']:
                    self.display_games()

                self.update_displays()
                first = False

    def display_games(self):
        games_menu = self.menu_sections[self.menu_section_dict['games']]
        TextDisplayer(self.pixel_surface).display_text(games_menu.selected_entry().name, games_menu.selected_entry().theme_color)

    def display_game_info(self):
        TextDisplayer(self.pixel_surface).display_text("game info")

    def display_system_menu(self):
        system_menu = self.menu_sections[self.menu_section_dict['system']]
        TextDisplayer(self.pixel_surface).display_text(system_menu.selected_entry())

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
                if self.menu_sections[self.menu_section_index].name == 'system':
                        self.check_events_for_system_menu(event)
                elif self.menu_sections[self.menu_section_index].name == 'games':
                        self.check_events_for_games_menu(event)

                self.check_events_for_all(event)

        return event_received

    def check_events_for_system_menu(self, event):
        pass

    def check_events_for_games_menu(self, event):
        games_menu = self.menu_sections[self.menu_section_dict['games']]
        if event.key == KEY_LEFT:
            games_menu.decrement()
            print games_menu.index
        elif event.key == KEY_RIGHT:
            games_menu.increment()
            print games_menu.index

    def check_events_for_game_info_menu(self, event):
        pass

    def check_events_for_all(self, event):
        if event.key == KEY_DOWN:
            self.menu_section_index -= 1
            if self.menu_section_index < 0:
                self.menu_section_index = len(self.menu_sections)-1
        elif event.key == KEY_UP:
            self.menu_section_index += 1
            if self.menu_section_index > len(self.menu_sections)-1:
                self.menu_section_index = 0

    def get_menu_from_name(self, name):
        return self.menu_sections[self.menu_section_dict[name]]

class MenuSection(object):
    def __init__(self, name, entries):
        self.entries = entries
        self.index = 0
        self.name = name

    def increment(self):
        self.index += 1
        if self.index > len(self.entries)-1:
            self.index = 0

    def decrement(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.entries)-1

    def selected_entry(self):
        return self.entries[self.index]


def main():
    if sys.argv.__len__() > 1:
        menu = Menu(sys.argv[1])
    else:
        menu = Menu()
    menu.init_displays()
    menu.load_games()
    menu.init_menus()
    menu.display_menu()

if __name__ == "__main__":
    main()
